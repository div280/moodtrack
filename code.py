from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create database and table
def create_database():
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT,
            reason TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Handle database connection errors
def get_db_connection():
    try:
        conn = sqlite3.connect("mood_tracker.db")
        return conn
    except Exception as e:
        return None

# Log mood endpoint
@app.route('/log_mood', methods=['POST'])
def log_mood():
    try:
        data = request.json
        mood = data.get('mood')
        reason = data.get('reason', None)

        if not mood or not isinstance(mood, str):
            return jsonify({'success': False, 'message': 'Invalid mood format'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mood_entries (mood, reason, timestamp) VALUES (?, ?, ?)", (mood, reason, timestamp))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Mood logged successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Internal server error: {str(e)}'}), 500

# Fetch all mood entries
@app.route('/get_report', methods=['GET'])
def get_report():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500

        cursor = conn.cursor()
        cursor.execute("SELECT mood, reason, timestamp FROM mood_entries ORDER BY timestamp DESC")
        data = cursor.fetchall()
        conn.close()

        entries = [{'mood': mood, 'reason': reason, 'timestamp': timestamp} for mood, reason, timestamp in data]
        return jsonify({'entries': entries})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Internal server error: {str(e)}'}), 500

# Serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
