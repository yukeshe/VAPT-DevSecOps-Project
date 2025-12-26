from flask import Flask,render_template,request
from models import db,User

app=Flask(__name__)
app.secret_key="dev-secret"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///vapt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)



@app.route("/")
def home():
    return "VAPT Test Application Running"

@app.route("/register",methods=["GET" , "POST"])

def register():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        
        user=User(username=username,password=password,email=email,role="user")
        
        db.session.add(user)
        db.session.commit()

        return"User registered"
        
    
    return render_template("register.html")

with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(debug=True)