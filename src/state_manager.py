import json
from pathlib import Path
from datetime import datetime


class StateManager:

    def __init__(self, state_path: str = "state.json"):
        self.state_path = Path(state_path)

    def load_all(self):
        if not self.state_path.exists():
            return {}
        with open(self.state_path, "r") as f:
            return json.load(f)

    def save_all(self, states: dict):
        states["last_update"] = datetime.utcnow().isoformat()
        with open(self.state_path, "w") as f:
            json.dump(states, f, indent=4)

    def load_state(self):

        if not self.state_path.exists():
            return None

        with open(self.state_path, "r") as f:
            return json.load(f)