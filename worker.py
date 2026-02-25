from engine.state import BotState
from engine.loop import run

state = BotState()

print("🚀 WORKER STARTED", flush=True)

run(state)