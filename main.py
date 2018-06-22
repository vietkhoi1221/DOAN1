from flask import Flask, render_template,redirect

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    return redirect("http://127.0.0.1:8050", code=302)

if __name__ == "__main__":
    app.run()