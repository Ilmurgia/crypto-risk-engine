import json
from pathlib import Path
from datetime import datetime


class StateManager:

    def __init__(self, state_path: str = "state.json"):
        self.state_path = Path(state_path)

    def save_state(self, state: dict):

        state_to_save = state.copy()
        state_to_save["last_update"] = datetime.utcnow().isoformat()

        with open(self.state_path, "w") as f:
            json.dump(state_to_save, f, indent=4)

    def load_state(self):

        if not self.state_path.exists():
            return None

        with open(self.state_path, "r") as f:
            return json.load(f)