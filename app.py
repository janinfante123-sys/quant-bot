from flask import Flask, render_template
from engine.state import BotState
from engine.loop import run
import threading

app = Flask(__name__)
state = BotState()

# 🔴 Arrancar bot cuando Gunicorn worker esté listo
@app.before_first_request
def start_bot():
    if not hasattr(app, "bot_started"):
        app.bot_started = True
        thread = threading.Thread(target=run, args=(state,), daemon=True)
        thread.start()
        print("🚀 BOT THREAD STARTED")

@app.route("/")
def dashboard():
    return render_template("dashboard.html", state=state)
