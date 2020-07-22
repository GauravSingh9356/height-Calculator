from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sent_mail import sent_email
from sqlalchemy.sql import func

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://opkdpjmmbmsndz:396673f1bd9b4e7721ab493ffac7a2001058e911c19243bb16e7c70cec535df2@ec2-34-206-252-187.compute-1.amazonaws.com:5432/d30rbc6h4r9jgf?sslmode=require'
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)
    
    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/success', methods=['POST'])
def success():
    if request.method=="POST":
        email=request.form['email']
        height=request.form.get('height')
        if db.session.query(Data).filter(Data.email_==email).count()==0:
            user_data=Data(email, height)
            db.session.add(user_data)
            db.session.commit()
            avg_height=db.session.query(func.avg(Data.height_)).scalar()
            count=db.session.query(Data.height_).count()
            avg_height=round(avg_height, 2)
            sent_email(email, height, avg_height, count)
            return render_template('success.html')
        else:
            return render_template('index.html', text='Seems that we have got data from that email already! ')

if __name__=='__main__':
    app.debug=True
    app.run()