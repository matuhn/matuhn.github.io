from flask import Flask, request, url_for, render_template, redirect, make_response
import uuid
from waitress import serve

app = Flask(__name__, static_url_path='')



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    question = request.form.get("q")
    name = save_question(question)
    return render_template("ticket.html" , ticket = question)

@app.route("/check", methods=['GET'])
def questionview():
    question_id = request.args.get("q")
    path = "question/" + question_id 
    f = open(path, "r")
    question = f.read()
    return question

def gen_name():
	return "question/" + uuid.uuid4().hex

def save_question(q):
	name = gen_name()
	f = open(name, 'w')
	f.write(q)
	f.close()
	return name

if __name__ == '__main__':
	serve(app, host='0.0.0.0', port=8012)
