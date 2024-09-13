from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)
mail = Mail(app)

# Database Models
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    goals = db.Column(db.String(250), nullable=True)
    health_score = db.Column(db.Float, nullable=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    activities = db.relationship('Activity', backref='patient', lazy=True)
    location_shares = db.relationship('LocationShare', backref='patient', lazy=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

class LocationShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

# Initialize and create the database
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/goals')
def goals():
    return render_template('goals.html')

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

@app.route('/activities')
def activities():
    return render_template('activities.html')

@app.route('/score')
def score():
    return render_template('score.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/panic')
def panic():
    return render_template('panic.html')

@app.route('/add_goal', methods=['POST'])
def add_goal():
    data = request.json
    patient = Patient.query.filter_by(email=data['email']).first()
    if patient:
        patient.goals = data['goals']
        db.session.commit()
        return jsonify({'message': 'Goal added successfully'})
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/schedule_appointment', methods=['POST'])
def schedule_appointment():
    data = request.json
    patient = Patient.query.filter_by(email=data['email']).first()
    if patient:
        appointment = Appointment(date=datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S'), description=data['description'], patient=patient)
        db.session.add(appointment)
        db.session.commit()
        msg = Message('Appointment Scheduled', sender='noreply@example.com', recipients=[patient.email])
        msg.body = f'Your appointment is scheduled for {data["date"]}.'
        mail.send(msg)
        return jsonify({'message': 'Appointment scheduled and email sent'})
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/emergency_alert', methods=['POST'])
def emergency_alert():
    data = request.json
    patient = Patient.query.filter_by(email=data['email']).first()
    if patient:
        msg = Message('Emergency Alert', sender='noreply@example.com', recipients=[patient.email])
        msg.body = f'Emergency alert: {data["alert_message"]}'
        mail.send(msg)
        return jsonify({'message': 'Emergency alert sent'})
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/add_activity', methods=['POST'])
def add_activity():
    data = request.json
    patient = Patient.query.filter_by(email=data['email']).first()
    if patient:
        activity = Activity(date=datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S'), type=data['type'], value=data['value'], patient=patient)
        db.session.add(activity)
        db.session.commit()
        return jsonify({'message': 'Activity added successfully'})
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/calculate_health_score', methods=['POST'])
def calculate_health_score():
    data = request.json
    patient = Patient.query.filter_by(email=data['email']).first()
    if patient:
        activities = Activity.query.filter_by(patient_id=patient.id).all()
        score = sum([activity.value for activity in activities]) / len(activities) if activities else 0
        patient.health_score = score
        db.session.commit()
        return jsonify({'health_score': score})
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/predict_health_tips', methods=['POST'])
def predict_health_tips():
    data = request.json
    model = RandomForestClassifier()  # Example model, replace with actual model
    patient_data = np.array([data['features']])
    prediction = model.predict(patient_data)
    return jsonify({'predicted_tip': prediction[0]})

@app.route('/share_location', methods=['POST'])
def share_location():
    data = request.json
    patient = Patient.query.filter_by(email=data['email']).first()
    if patient:
        location = LocationShare(latitude=data['latitude'], longitude=data['longitude'], patient=patient)
        db.session.add(location)
        db.session.commit()
        return jsonify({'message': 'Location shared successfully'})
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/panic_button', methods=['POST'])
def panic_button():
    data = request.json
    patient = Patient.query.filter_by(email=data['email']).first()
    if patient:
        msg = Message('Panic Button Alert', sender='noreply@example.com', recipients=[patient.email])
        msg.body = 'A panic button alert was triggered. Immediate attention required.'
        mail.send(msg)
        return jsonify({'message': 'Panic alert sent'})
    return jsonify({'message': 'Patient not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)