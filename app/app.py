from flask import Flask,render_template,request,session,redirect,url_for
from models import db,User
from werkzeug.security import generate_password_hash,check_password_hash


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
        
        hashed_password=generate_password_hash(password)
        user=User(username=username,password=hashed_password,email=email,role="user")
        
        db.session.add(user)
        db.session.commit()

        return"User registered"
        
    
    return render_template("register.html")

@app.route("/login",methods=['GET','POST'])

def login():

    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        user=User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password,password):
            session["user_id"]=user.id
            return redirect(url_for("dashboard"))
        
        else:
            return "Invalid credentials" 
    
    return render_template("login.html")

@app.route("/dashboard")

def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return "Welcome to your dashboard"

with app.app_context():
    db.create_all()

@app.route("/admin")

def admin():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user=User.query.get(session["user_id"])

    if user.role!='admin':
        return "Access denied!! , 403"

    return "Welcom to Admin Panel"

if __name__=="__main__":
    app.run(debug=True)