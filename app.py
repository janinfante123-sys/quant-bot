
from flask import Flask, render_template
from engine.state import BotState
from engine.loop import run
import threading

app = Flask(__name__)
state = BotState()

@app.route("/")
def dashboard():
    return render_template("dashboard.html", state=state)

if __name__ == "__main__":
    threading.Thread(target=run, args=(state,), daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
