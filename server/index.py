from flask import Flask , request , abort ,jsonify ,session
from flask_bcrypt import Bcrypt
from config.appconfig import ApplicationConfig
from database.model import Users , db
from redis import Redis
from flask_session import Session

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
db.init_app(app)
bcrypt = Bcrypt(app)
redis = Redis(host='redis', port =6379)
server_session = Session(app)

@app.get('/')
def hello():
    redis.incr('hits')
    counter = str(redis.get('hits'),'utf-8')
    return f"counter = {counter}"

@app.route('/register', methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    user_exist = Users.query.filter_by(email=email).first() is not None

    if user_exist:
        abort(409)

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = Users(email=email,password=password,password_hash=encrypted_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })

@app.route('/login',methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]
    user_exist = Users.query.filter_by(email=email).first()

    if user_exist is None:
        return jsonify({"error":"Unauthorised"}),401
    
    if not bcrypt.check_password_hash(user_exist.password_hash,password):
        return jsonify({"error":"Unauthorised"}),401   
    

    session['user_id']=user_exist.id 

    return jsonify({
        "id": user_exist.id,
        "email": user_exist.email
    })

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',debug=True,port=5000)