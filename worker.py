from engine.state import BotState
from engine.loop import run

state = BotState()

print("🚀 WORKER STARTED")

run(state)
