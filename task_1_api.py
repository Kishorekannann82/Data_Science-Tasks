from flask import Flask,jsonify,request

app=Flask(__name__)
users=[
    {"id":1,"name":"Kishore"},
    {"id":2,"name":"Sheik"},
    {"id":3,"name":"Hafeel"},
    {"id":4,"name":"Saran"}
]
@app.route("/")
def home():
    return "Hello Family membersssss"

# Get all users
@app.route("/users",methods=["GET"])
def get_users():
    return jsonify(users)

# Create a user
@app.route("/users",methods=["POST"])
def create_user():
    data=request.get_json()
    if not data or "name" not in data:
        return jsonify({"error":"Name is required"}),400
    new_user={
        "id":len((users))+1,
        "name":data["name"]
    }
    users.append(new_user)
    return jsonify({
        "message":"User Created Successfully",
        "user":new_user
    }),201

# Update a user
@app.route("/users/<int:user_id>",methods=["PUT"])
def update_user(user_id):
    data=request.get_json()
    if not data or "name" not in data:
        return jsonify({"error":"name is Requireddd"}),400
    for user in users:
        if user["id"]==user_id:
            user["name"]=data["name"]
            return jsonify({
                "message":"User Updated Successfully",
                "user":user
            })
    return jsonify({"error":"User Not Found"}),404

## delete a user
@app.route("/users/<int:user_id>",methods=["DELETE"])
def delete_users(user_id):
    for user in users:
        if user["id"]==user_id:
            users.remove(user)
            return jsonify({
                "messsage":"Deletede Successfully",
                
            }),200
    return jsonify({"error":"User Not Found"}),404
    
        

if __name__=="__main__":
    app.run(debug=True)
