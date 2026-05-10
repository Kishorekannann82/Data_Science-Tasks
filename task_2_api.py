from flask import Flask,jsonify,request
import joblib
import numpy as np

app=Flask(__name__)

model=joblib.load("model.pkl")
@app.route("/")
def home():
    return "ML Model API is Running"

@app.route("/predict",methods=["POST"])
def predict():
    try:
        data=request.get_json()
        features=np.array(data["features"]).reshape(1,-1)
        prediction=model.predict(features)
        return jsonify({
            "prediction":int(prediction[0])
        })
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),400
    
if __name__=="__main__":
    app.run(debug=True)