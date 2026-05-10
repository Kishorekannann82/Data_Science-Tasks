

from flask import Flask,jsonify,request

app=Flask(__name__)

@app.route("/")
def home():
    return "Hello World !This is Kishore "

@app.route("/users",methods=["GET"])
def users():
    users=[
        {"id":1,"name":"Kishore"},
        {"id":2,"name":"Ravi"},
        {"id":3,"name":"Suresh"}
    ]
    return jsonify(users)

@app.route("/users/<int:user_id>",methods=["GET"])
def get_user(user_id):
    user={"id":user_id,"name":"Kishore"}
    return jsonify(user)

## Post request to create a new user
@app.route("/users",methods=["POST"])
def create_user():
    data=request.json
    return jsonify({
        "messages":"User Created Sucessfully",
        "user":data
    }),201

@app.route("/users/<int:user_id>",methods=["PUT"])
def updata_user(user_id):
    data=request.json
    return jsonify({
        "message":"User Updated Succcessfully",
        "user_id":user_id,
        "new_user":data
    })
if __name__=="__main__":
    app.run(debug=True)
    