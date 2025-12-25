from flask import Flask
from models import db

app=Flask(__name__)
app.secret_key="dev-secret"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///vapt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)



@app.route("/")
def home():
    return "VAPT Test Application Running"

with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(debug=True)