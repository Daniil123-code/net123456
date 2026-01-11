import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "localhost"
PORT = 8000
DATA_FILE = "tasks.txt"

tasks = []


def load_data():
    global tasks
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                tasks = json.loads(content) if content else []
        except (json.JSONDecodeError, IOError):
            tasks = []


def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
    except IOError:
        pass


class TodoHandler(BaseHTTPRequestHandler):
    def _send_response(self, code, body=None):
        self.send_response(code)
        if body is not None:
            self.send_header("Content-type", "application/json")
        self.end_headers()
        if body is not None:
            self.wfile.write(json.dumps(body, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        if self.path == "/tasks":
            self._send_response(200, tasks)
        else:
            self._send_response(404)

    def do_POST(self):
        if self.path == "/tasks":
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                post_body = self.rfile.read(content_len)
                data = json.loads(post_body.decode("utf-8"))
            except json.JSONDecodeError:
                self._send_response(400)
                return

            new_id = 1
            if tasks:
                new_id = max(t["id"] for t in tasks) + 1

            new_task = {
                "title": data.get("title", ""),
                "priority": data.get("priority", "normal"),
                "isDone": False,
                "id": new_id
            }

            tasks.append(new_task)
            save_data()
            self._send_response(200, new_task)

        elif self.path.startswith("/tasks/") and self.path.endswith("/complete"):
            try:
                # Format: /tasks/{id}/complete
                parts = self.path.split("/")
                task_id = int(parts[2])

                found = False
                for task in tasks:
                    if task["id"] == task_id:
                        task["isDone"] = True
                        found = True
                        break

                if found:
                    save_data()
                    self._send_response(200)  # Empty body
                else:
                    self._send_response(404)
            except (IndexError, ValueError):
                self._send_response(400)
        else:
            self._send_response(404)


if __name__ == "__main__":
    load_data()
    server = HTTPServer((HOST, PORT), TodoHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        save_data()