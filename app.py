from flask import Flask, render_template, request, redirect, jsonify  # type: ignore
import os

API_KEY = "newnss-secret-key-with-flask-2025"

app = Flask(__name__)

@app.route('/')
def home():
    if not os.path.exists('battery_log.txt'):
        return render_template("form.html", logs=[], voltages=[], timestamps=[])

    with open('battery_log.txt', 'r', encoding="utf-8") as file:
        logs = file.readlines()

    voltages = []
    timestamps = []

    for line in logs:
        parts = line.split("--")
        if len(parts) >= 2:
            try:
                voltage_str = parts[1].strip().replace("V", "")
                voltage = float(voltage_str)
                voltages.append(voltage)
                timestamps.append(parts[0].strip())
            except:
                pass

    return render_template("form.html", logs=logs, voltages=voltages, timestamps=timestamps)

@app.route('/add', methods=['POST'])
def add_log():
    name = request.form["name"]
    battery = float(request.form["battery"])

    if battery > 3.7:
        status = "🔋 Fully charged"
    elif battery > 3.2:
        status = "🟡 Battery ok"
    else:
        status = "⚠️ Battery low!"

    with open('battery_log.txt', 'a', encoding="utf-8") as file:
        file.write(f"{name} - {battery}V - {status} — ✅ Added from web\n")
    
    return redirect('/')

@app.route("/api/logs", methods=['POST'])
def api_log():
    auth_key = request.headers.get("x-api-key")

    if auth_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401


    data = request.get_json()
    name = data.get("name")
    battery = float(data.get("battery"))

    # if not name or not isinstance(battery, (int, float)):
    #     return jsonify({"error": "Invalid input"}), 400

    if battery > 3.7:
        status = "🔋 Fully charged"
    elif battery > 3.2:
        status = "🟡 Battery ok"
    else:
        status = "⚠️ Battery low!"

    with open('battery_log.txt', 'a', encoding="utf-8") as file:
        file.write(f"{name} -- {battery}V -- {status} — ✅ Added from API\n")

    return jsonify({"message": "Data received successfully"}), 200

if __name__ == '__main__':
    app.run()