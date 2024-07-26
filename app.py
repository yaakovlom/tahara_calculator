from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'calendar.html')

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/api/events', methods=['GET'])
def get_events():
    if os.path.exists('events.json'):
        with open('events.json', 'r', encoding='utf-8') as f:
            events = json.load(f)
    else:
        events = {}
    return jsonify(events)

@app.route('/api/events', methods=['POST'])
def save_events():
    print(request.json)
    events = request.json
    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    return jsonify({"message": "Events saved successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
