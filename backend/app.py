from flask import Flask, request, jsonify
from flask_cors import CORS

from database import *
from otp_service import *
from email_service import *
from fingerprint_service import *
from hardware_service import *
import uuid

app = Flask(__name__)
CORS(app)

init_db()
init_mail(app)


@app.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    conn = get_db()
    cursor = conn.cursor()

    # check if email already exists
    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({
            "message": "User already exists"
        }), 400

    cursor.execute(
        "INSERT INTO users(name,email,password) VALUES (?,?,?)",
        (name,email,password)
    )

    conn.commit()

    return jsonify({
        "message": "User registered successfully"
    })

@app.route("/login", methods=["POST"])
def login():

    data = request.json
    email = data["email"]
    password = data["password"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401


@app.route("/verify-otp", methods=["POST"])
def verify():

    data = request.json
    email = data["email"]
    otp = data["otp"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM otps WHERE email=? AND otp=?",
        (email,otp)
    )

    result = cursor.fetchone()

    if result:

        unlock_door()

        return jsonify({"message":"Door unlocked"})

    return jsonify({"message":"Invalid OTP"})


@app.route("/add-fingerprint", methods=["POST"])
def add_fp():

    data = request.json
    user_id = data["user_id"]
    fingerprint_id = data["fingerprint_id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO fingerprints(user_id,fingerprint_id) VALUES (?,?)",
        (user_id,fingerprint_id)
    )

    conn.commit()

    return jsonify({"message":"Fingerprint added"})

@app.route("/remove-fingerprint", methods=["POST"])
def remove_fp():

    data = request.json
    fingerprint_id = data["fingerprint_id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM fingerprints WHERE fingerprint_id=?",
        (fingerprint_id,)
    )

    conn.commit()

    return jsonify({"message":"Fingerprint removed"})
@app.route("/verify-otp-hardware", methods=["POST"])
def verify_otp_hardware():

    data = request.json
    otp = data["otp"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM otps WHERE otp=?", (otp,))
    result = cursor.fetchone()

    if result:
        send_email(result[0], "Door Unlock", "Door opened successfully")
        return jsonify({"status":"ok"})
    else:
        return jsonify({"status":"invalid"})
import random

@app.route("/fingerprint-detected", methods=["POST"])
def fingerprint_detected():

    data = request.json
    fingerprint_id = data["fingerprint_id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM fingerprints WHERE fingerprint_id=?",
        (fingerprint_id,)
    )

    user = cursor.fetchone()

    if not user:
        return jsonify({"message":"Fingerprint not recognized"}), 404

    user_id = user[0]

    # generate 4 digit OTP
    otp = str(random.randint(1000,9999))

    cursor.execute(
        "INSERT INTO otps(user_id, otp) VALUES (?,?)",
        (user_id, otp)
    )

    conn.commit()

    return jsonify({
        "message":"Fingerprint verified",
        "otp": otp
    })

@app.route("/verify-otp", methods=["POST"])
def verify_otp():

    data = request.json
    otp = data["otp"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM otps WHERE otp=? ORDER BY id DESC LIMIT 1",
        (otp,)
    )

    result = cursor.fetchone()

    if not result:
        return jsonify({"message":"Invalid OTP"}), 401

    user_id = result[0]

    token = str(uuid.uuid4())

    cursor.execute(
        "INSERT INTO unlock_tokens(user_id,token) VALUES (?,?)",
        (user_id,token)
    )

    conn.commit()

    return jsonify({
        "message":"OTP verified",
        "unlock_token": token
    })

@app.route("/unlock/<token>")
def unlock(token):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM unlock_tokens WHERE token=?",
        (token,)
    )

    result = cursor.fetchone()

    if not result:
        return "Invalid token"

    # SEND COMMAND TO ESP32
    try:
        requests.get("http://192.168.0.45/unlock")
    except:
        print("ESP32 not reachable")

    return "Door unlocked successfully"

app.run(port=5000)