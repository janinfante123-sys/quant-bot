from flask import Flask, render_template
from engine.state import BotState
from engine.loop import run
import threading
import os

app = Flask(__name__)
state = BotState()

# 🔴 IMPORTANTE: arrancar el bot también en producción (gunicorn)
def start_bot_once():
    if not hasattr(app, "bot_started"):
        app.bot_started = True
        t = threading.Thread(target=run, args=(state,), daemon=True)
        t.start()
        print("🚀 BOT THREAD STARTED")

start_bot_once()

@app.route("/")
def dashboard():
    return render_template("dashboard.html", state=state)
