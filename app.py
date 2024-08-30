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
    target_event = request.json
    with open('events.json', 'r', encoding='utf-8') as f:
        events = json.load(f)

    if target_event:
        flag = target_event['flag']
        date = target_event['date']
        event_id = int(target_event['event']['id']) if target_event['event']['id'] else None

        if flag == 'add':
            if date not in events:
                target_event['event']['id'] = 1
                events[date] = [target_event['event']]
            else:
                target_event['event']['id'] = events[date][-1]['id'] + 1
                events[date].append(target_event['event'])

        elif flag == 'update':
            event_found = False
            if date in events:
                for i, event in enumerate(events[date]):
                    if event['id'] == event_id:
                        events[date][i] = target_event['event']
                        event_found = True
                        break
            if not event_found:
                return jsonify({"Update events": "Event {} not found".format(target_event)}), 401

        elif flag == 'delete':
            event_found = False
            if date in events:
                for i, event in enumerate(events[date]):
                    print(type(event_id), type(event['id']))
                    if event['id'] == event_id:
                        print("yes")
                        events[date].pop(i)
                        event_found = True
                        break
                    
            if not event_found:
                return jsonify({"Delete events": "Event {} not found".format(target_event)}), 402
            
        else:
            return jsonify({"message": "Invalid flag"}), 400

    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    return jsonify(events), 200

if __name__ == '__main__':
    app.run(debug=True)
