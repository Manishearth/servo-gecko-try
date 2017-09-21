from flask import Flask, request, jsonify, Response
from threading import Lock
import subprocess
import json
import os

app = Flask(__name__)

config = {}
lock = Lock()

def ensure_init():
    if not os.path.isdir(config['servo-clone']['folder']):
        proc = subprocess.Popen(["git", "clone", config['servo-clone']['remote'], config['servo-clone']['folder']])
        proc.wait()
    for clone in config['gecko-clones']:
        if not os.path.isdir(config['gecko-clones'][clone]['folder']):
            proc = subprocess.Popen(["hg", "clone", config['gecko-clones'][clone]['remote'], config['gecko-clones'][clone]['folder']])
            proc.wait()



def handle_pull(pull, branch):
    if branch not in config["gecko-clones"]:
        return ("{}", 400)
    selfdir = os.path.dirname(__file__)

    with lock:
        proc = subprocess.Popen(["bash", os.path.join(selfdir, "run.sh"),
                                 "%d" % pull, config['servo-clone']['folder'],
                                 config['gecko-clones'][branch]['folder']],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            return ("Error applying patch.\n\n\nStdout:\n\n{}\n\n\nStderr:\n\n{}".format(stdout, stderr), 500)
        if stdout:
            for line in stdout.split('\n'):
                if line.startswith("remote:   https://treeherder.mozilla.org/"):
                    return resp(line.replace("remote:   ", ""), 200)
        return ("(no try url found)", 200)


@app.route('/homu', methods = ['POST'])
def homu():
    post = request.get_json()
    pr = post['pull']
    extra_data = post['extra_data']
    branch = 'mozilla-central'
    if extra_data == "autoland":
        branch = "autoland"
    text,status = handle_pull(pr, branch)
    if status == 200:
        return Response(response=text, status=200, mimetype="text/plain")
    else:
        return Response(response=":broken_heart: error pushing to try", status=200, mimetype="text/plain")


@app.route('/<int:pull>', defaults={'branch': 'mozilla-central'})
@app.route('/<int:pull>/<branch>')
def flask_pull(pull, branch):
    text,status = handle_pull(pull, branch)
    return Response(response=text, status=status, mimetype="text/plain")

@app.route('/')
def index():
    return "Hi from servo-gecko-try!"

def main():
    global config
    with open('config.json') as f:
        config = json.loads(f.read())
    ensure_init()
    app.run(host=config["host"], port=config["port"])

if __name__ == "__main__":
    main()
