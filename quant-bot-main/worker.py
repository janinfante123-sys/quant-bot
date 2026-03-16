from engine.loop import run
from engine.state import BotState

print("🚀 WORKER STARTED")

state = BotState()
run(state)
