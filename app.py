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
    # print(request.json)
    new_event = request.json
    with open('events.json', 'r', encoding='utf-8') as f:
        # read the file
        events = json.load(f)
    if new_event:
        flag = new_event['flag']
        date = new_event['date']
        target_event = new_event['event']

        if flag == 'add':
            if date not in events:
                events[date] = [target_event]
            else:
                events[date].append(target_event)

        elif flag == 'delete':
            if target_event in events[date]:
                events.remove(target_event)
            else:
                return jsonify({"message": "Event not found"}), 400
            
        else:
            return jsonify({"message": "Invalid flag"}), 400

    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    return jsonify(events), 200

if __name__ == '__main__':
    app.run(debug=True)
