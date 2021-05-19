from flask import Flask, request, session, render_template, send_file, flash, redirect, url_for, json, jsonify
from Secrets import captcha_public, captcha_secret
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import requests

# configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
db = SQLAlchemy(app)
app.secret_key = "sup" # For security safty change this
ADMIN_TOKEN = "admin123" # For security safty change this


# classes
class auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.Text(12), unique=True, nullable=False)
    password = db.Column(db.Text(50), nullable=False)
    admin = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'| {self.uname}, Admin={self.admin}, id= {str(self.id)} |'


class storage(db.Model):
    Sid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    data = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'{self.name} id= ' + str(self.Sid)


class recaptcha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(12), unique=True)
    session_token_status = db.Column(db.String)

    def __repr__(self):
        return f'{str(self.session_token)}'
        


def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    secret = captcha_secret
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


@app.route('/recaptcha/verify/<string:token>', methods=['GET', 'POST'])
def captcha(token):

    sitekey = captcha_public
    token_checker = recaptcha.query.all()

    try:

        if request.method == "POST":

            captcha_response = request.form['g-recaptcha-response']

            if is_human(captcha_response):
                
                status = "Verification successful. You may now close this window."
                new_session_token = recaptcha(session_token=token, session_token_status = 'Successed')
                db.session.add(new_session_token)
                db.session.commit()
                
            else:

                status = "Sorry! Please Check Im not a robot again."

            flash(status)

    except:
        flash ('This token in not valid or has already been used, please request new token.')

    return render_template("captcha.html", sitekey=sitekey)


@app.route('/recaptcha/check/<string:token>', methods=['GET', 'POST'])
def protected(token):

    find_token = recaptcha.query.filter_by(session_token=token).first()
    if find_token:
        status = 'Verfication successed'
    else:
        status = 'Verfication failed'
    
    return (status)



if __name__ == "__main__":
    app.run(debug=True)
    