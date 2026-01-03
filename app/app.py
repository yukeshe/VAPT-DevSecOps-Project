from flask import Flask,render_template,request,session,redirect,url_for
from models import db,User,Securitylog
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import jwt_required,JWTManager,get_jwt_identity,create_access_token,create_refresh_token
from datetime import timedelta

app=Flask(__name__)
app.secret_key="dev-secret"
app.config["JWT_SECRET_KEY"]="super-secret-key" 
jwt=JWTManager(app)

app.config["JWT_ACCESS_TOKEN_EXPIRES"]=timedelta(minutes=15)

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
    
    user=User.query.get(session["user_id"])
    return render_template("dashboard.html",user=user)

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

@app.route("/profile")

def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user=User.query.get(session["user_id"])

    return render_template("profile.html",user=user)

@app.route("/logs")

def logs():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user=User.query.get(session["user_id"])

    if user.role!='admin':
        return 'Access denied',403

    records=Securitylog.query.order_by(Securitylog.timestamp.desc()).limit(50).all()

    return render_template("logs.html",records=records)

@app.route("/api/login",methods=["POST"])

def api_login():
    data=request.get_json()
    user=User.query.filter_by(username=data["username"]).first()

    if user and check_password_hash(user.password,data["password"]):
        access = create_access_token(identity=str(user.id))
        refresh = create_refresh_token(identity=str(user.id))
        log_event("SUCCESSFUL_LOGIN",user.id)
        return{"access_token":access,"refresh_token":refresh}

    log_event("FAILED_LOGIN")
    return {'msg':'Bad credentials'},401

@app.route("/api/profile")
@jwt_required()

def api_profile():
    user_id=int(get_jwt_identity())
    user=User.query.get(user_id)

    return {'username':user.username,'email':user.email,'role':user.role}


@app.route("/app/refresh",methods=['POST'])
@jwt_required(refresh=True)

def refresh():
    uid=get_jwt_identity()
    new_access=create_access_token(identity=uid)
    log_event("TOKEN_REFRESH",uid)
    return{"access_token":new_access}

@app.route("/api/admin",methods=["POST"])
@jwt_required()

def api_admin():
    uid=get_jwt_identity()
    user=User.query.get(uid)

    if user.role!="admin":
        log_event("FORBIDDEN_ADMIN_ACCESS",uid)
        return{"msg":"Forbidden"},403   
    
    return {"msg":"Admin data"}

def log_event(event,user_id=None):
    ip=request.remote_addr
    sec_log=Securitylog(event_type=event,user_id=user_id,ip_address=ip)
    db.session.add(sec_log)
    db.session.commit()

if __name__=="__main__":
    app.run(debug=True)