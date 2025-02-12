from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

MONGO_URL = MongoClient("mongodb+srv://mohamedvaseem:mohamedvaseem@anime-galaxy.7lnts.mongodb.net/")
db = MONGO_URL["portfolio-fb"]
collection = db["feedbacks"]

@app.route("/feedbacks", methods=["POST"])
def feedback():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        feedback_text = data.get('text')
        
        current_time = datetime.now()
        feedback_data = {
            "time": current_time.strftime("%H:%M:%S"),
            "date": current_time.strftime("%Y-%m-%d"),
            "name": name,
            "email": email,
            "feedback": feedback_text
        }
        
        collection.insert_one(feedback_data)
        return jsonify({"message": "Feedback submitted successfully!"}), 201
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/get-fb", methods=["GET"])
def getfb():
    try:
        feedback_list = []
        for fb in collection.find({}, {"_id": 0}):  # Exclude MongoDB's _id field
            feedback_list.append(fb)
        
        return jsonify({"feedback_list": feedback_list}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True);

