from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def create_tables():
    """Create database tables if they don't exist."""
    with app.app_context():
        db.create_all()

class Segnalazione(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text, nullable=False)

class ODS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descrizione = db.Column(db.Text, nullable=False)

class Utente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class Preventivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    importo = db.Column(db.Float, nullable=False)


@app.route('/segnalazioni', methods=['GET', 'POST'])
def handle_segnalazioni():
    if request.method == 'POST':
        data = request.get_json()
        seg = Segnalazione(titolo=data.get('titolo'), descrizione=data.get('descrizione'))
        db.session.add(seg)
        db.session.commit()
        return jsonify({'id': seg.id}), 201
    segs = Segnalazione.query.all()
    return jsonify([{'id': s.id, 'titolo': s.titolo, 'descrizione': s.descrizione} for s in segs])

@app.route('/segnalazioni/<int:seg_id>/pdf')
def segnalazione_pdf(seg_id):
    seg = Segnalazione.query.get_or_404(seg_id)
    filename = f'segnalazione_{seg.id}.pdf'
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, f"Segnalazione {seg.id}")
    c.drawString(100, 730, seg.titolo)
    text = c.beginText(100, 710)
    for line in seg.descrizione.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()
    return send_file(filename, as_attachment=True)

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    to_address = data.get('to')
    subject = data.get('subject', 'Test')
    body = data.get('body', '')
    attachment = data.get('attachment')  # path to file

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.environ.get('SMTP_FROM', 'noreply@example.com')
    msg['To'] = to_address
    msg.set_content(body)

    if attachment and os.path.exists(attachment):
        with open(attachment, 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename=os.path.basename(attachment))

    smtp_host = os.environ.get('SMTP_HOST', 'localhost')
    smtp_port = int(os.environ.get('SMTP_PORT', 25))

    with smtplib.SMTP(smtp_host, smtp_port) as s:
        s.send_message(msg)

    return jsonify({'status': 'sent'})

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
