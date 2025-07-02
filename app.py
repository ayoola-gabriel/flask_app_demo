from flask import Flask, render_template, request, redirect, jsonify  # type: ignore
import os
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from datetime import datetime
# from dotenv import load_dotenv  # type: ignore

API_KEY = "newnss-secret-key-with-flask-2025"

app = Flask(__name__)


db_uri = os.getenv("DATABASE_URL", "sqlite:///local.db")


if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BatteryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    project = db.Column(db.String(100))
    voltage = db.Column(db.Float)
    status = db.Column(db.String(50))

    def __repr__(self):
        return f"<{self.project} {self.voltage}V"
    
# -------ROUTES-------
def create_tables():
    db.create_all()

@app.route('/')
def home():
    logs = BatteryLog.query.order_by(BatteryLog.timestamp.desc()).all()
    voltages = [log.voltage for log in logs][::-1]
    timestamps = [log.timestamp.strftime("%H:%M:%S") for log in logs][::-1]
    return render_template("form.html", logs=logs, voltages=voltages, timestamps=timestamps)

@app.route('/add', methods=['POST'])
def add_form():
    return add_entry(request.form["name"],
                     float(request.form["battery"]),
                     source="Form")

@app.route("/api/logs", methods=['POST'])
def api_log():
    auth_key = request.headers.get("x-api-key")

    if auth_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401


    data = request.get_json()
    return add_entry(data["name"],
                     float(data["battery"]),
                     source="API")

def add_entry(name, voltage, source):
     status = ("🔋 Fully charged" if voltage > 3.7 else
              "🟡 Battery ok"    if voltage > 3.2 else
              "⚠️ Battery low!")
     
     db.session.add(BatteryLog(
         project=name,
         voltage=voltage,
         status=status
     ))
     db.session.commit()

     if source == "API":
          return jsonify({"message": "Saved"}), 200
     
     return redirect('/')


@app.route("/debug")
def debug():
    logs = BatteryLog.query.order_by(BatteryLog.timestamp.desc()).all()
    return "<br>".join([f"{log.timestamp} — {log.project} — {log.voltage}V — {log.status}" for log in logs])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)