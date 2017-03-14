from flask import Flask, request, jsonify, Response
from threading import Lock
import subprocess
import json
import os

app = Flask(__name__)

config = {}
lock = Lock()

with open('config.json') as f:
    config = json.loads(f.read())

def resp(text, code):
    return Response(response=text, status=code, mimetype="text/plain")

@app.route('/<int:pull>', defaults={'branch': 'mozilla-central'})
@app.route('/<int:pull>/<branch>')
def pull(pull, branch):
    if branch not in config["gecko-clones"]:
        return resp("{}", 400)
    with lock:
        proc = subprocess.Popen(["bash", "run.sh",
                                 "%d" % pull, config['servo-clone'],
                                 config['gecko-clones'][branch]],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            return resp("Error applying patch.\n\n\nStdout:\n\n%s\n\n\nStderr:\n\n%s" % (stdout, stderr), 500)
        if stdout:
            for line in stdout.split('\n'):
                if line.startswith("remote:   https://treeherder.mozilla.org/"):
                    return resp(line.replace("remote:   ", ""), 200)
        return resp("(no try url found)", 200)

@app.route('/')
def index():
    return "Hi!"

def main():
    app.run(host=config["host"])

if __name__ == "__main__":
    main()
