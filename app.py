from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["user_data"]
collection = db["users"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        existing = collection.find_one({"email": email})
        if existing:
            msg = "⚠️ Duplicate entry! This email already exists."
        else:
            collection.insert_one({"name": name, "email": email})
            msg = "✅ Data inserted successfully!"

        return render_template("index.html", message=msg)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
