from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import logging
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecurekey123"

logging.basicConfig(
    filename="http_server.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

prtg_data_list = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "password123":
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Hatalı giriş! Lütfen tekrar deneyin.", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", prtg_data=reversed(prtg_data_list))

@app.route("/prtg-webhook", methods=["POST"])
def prtg_webhook():
    try:
        content_type = request.headers.get('Content-Type')

        if content_type == 'application/json':
            data = request.get_json()
        elif content_type == 'application/x-www-form-urlencoded':
            raw_data = request.form.to_dict()
            try:
                key = next(iter(raw_data.keys()))
                data = json.loads(key) if key.startswith("{") else raw_data
            except json.JSONDecodeError:
                data = raw_data
        else:
            logging.error(f"Unsupported Content-Type: {content_type}")
            return jsonify({"error": "Unsupported Content-Type"}), 415

        if not data:
            return jsonify({"error": "No data received"}), 400

        logging.info(f"Received PRTG Data: {json.dumps(data, indent=2)}")

        cleaned_data = {
            key: ("N/A" if str(value).startswith("%") else value)
            for key, value in data.items()
        }

        if len(prtg_data_list) >= 100:
            prtg_data_list.pop(0)

        prtg_data_list.append({
            "datetime": cleaned_data.get("datetime", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "sensor": cleaned_data.get("sensor", "N/A"),
            "device": cleaned_data.get("device", "N/A"),
            "status": cleaned_data.get("status", "N/A"),
            "message": cleaned_data.get("message", "No message provided"),
            "priority": cleaned_data.get("priority", "N/A"),
            "lastvalue": cleaned_data.get("lastvalue", "N/A"),
            "lastcheck": cleaned_data.get("lastcheck", "N/A"),
            "group": cleaned_data.get("group", "N/A"),
            "probe": cleaned_data.get("probe", "N/A"),
            "uptime": cleaned_data.get("uptime", "N/A"),
            "downtime": cleaned_data.get("downtime", "N/A"),
        })

        return jsonify({"message": "Data received successfully"}), 200

    except Exception as e:
        logging.error(f"Error processing PRTG Data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
