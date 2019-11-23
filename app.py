from flask import Flask, send_from_directory, request
from flask_mail import Mail, Message

import os

app = Flask(__name__, static_folder='webpage')
mail = Mail(app)

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')


# Serve static page
@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    if name and email:
        try:
            mail.send(
                Message(
                    body="RSVP from {name} at {email}.",
                    recipients=app.config['MAIL_USERNAME'],
                    subject="RSVP from {name}"
                )
            )
            return send_from_directory(app.static_folder, 'success.html')
        except:
            return send_from_directory(app.static_folder, 'failure.html')
    return send_from_directory(app.static_folder, 'failure.html')

if __name__ == '__main__':
    app.run()