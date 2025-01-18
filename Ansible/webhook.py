from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print(f"Received webhook data", flush=True)
    webhook_data = request.get_json()

    if webhook_data:
        repository_name = webhook_data.get('repository', {}).get('name', 'Unknown repository')
        pusher_name = webhook_data.get('pusher', {}).get('name', 'Unknown pusher')
        commit_id = webhook_data.get('head_commit', {}).get('id', 'Unknown id')
        commit_added = webhook_data.get('head_commit', {}).get('added', 'Unknown')
        commit_removed = webhook_data.get('head_commit', {}).get('removed', 'Unknown')
        commit_modified = webhook_data.get('head_commit', {}).get('modified', 'Unknown')

        new_entry = {
            'repository_name': repository_name,
            'pusher_name': pusher_name,
            'commit_id': commit_id,
            'added_in_commit': commit_added,
            'removed_in_commit': commit_removed,
            'modified_in_commit': commit_modified
        }

        # Append data to the JSON file
        try:
            with open('/home/webhook_data.json', 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Ensure data is a list and append the new entry
        if not isinstance(data, list):
            data = [data]
        data.append(new_entry)

        with open('/home/webhook_data.json', 'w') as f:
            json.dump(data, f, indent=4)
        return 'Webhook received and filtered data saved', 200

    return 'No data', 400

@app.route('/show', methods=['GET'])
def show():
    try:
        with open('/home/webhook_data.json', 'r') as f:
            data = json.load(f)

            # Ensure data is a list
            if not isinstance(data, list):
                data = [data]

            html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Webhook Data</title>
                <style>
                    table {
                        width: 80%;
                        margin: 20px auto;
                        border-collapse: collapse;
                    }
                    th, td {
                        padding: 10px;
                        text-align: left;
                        border: 1px solid #ddd;
                    }
                    th {
                        background-color: #f4f4f4;
                    }
                    tr:nth-child(even) {
                        background-color: #f9f9f9;
                    }
                </style>
            </head>
            <body>
                <h1 style="text-align: center;">Webhook Data</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Repository</th>
                            <th>Pusher</th>
                            <th>Commit ID</th>
                            <th>Added</th>
                            <th>Removed</th>
                            <th>Modified</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in data %}
                        <tr>
                            <td>{{ item.repository_name }}</td>
                            <td>{{ item.pusher_name }}</td>
                            <td>{{ item.commit_id }}</td>
                            <td>{{ item.added_in_commit }}</td>
                            <td>{{ item.removed_in_commit }}</td>
                            <td>{{ item.modified_in_commit }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </body>
            </html>
            """
            return render_template_string(html_template, data=data), 200
    except FileNotFoundError:
        return 'No webhook data saved', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
