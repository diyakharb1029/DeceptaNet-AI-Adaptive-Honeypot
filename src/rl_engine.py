# rl_module.py

import random
import json
import os
from datetime import datetime

Q_FILE = "qtable.json"# Log RL learning update
try:
    with open("logs.txt", "a") as lf:
        lf.write(
            f"[{datetime.now()}] [RL] Updated state={state} action={action} → {Q[state][action]:.3f}\n"
        )
except:
    pass

# Default Q-table if no file exists yet
DEFAULT_Q = {
    "0": [0.5, 0.5],   # state 0 = normal
    "1": [0.5, 0.5]    # state 1 = attack
}

alpha = 0.6    # learning rate
gamma = 0.8    # discount factor
epsilon = 0.2  # exploration rate


def _load_q():
    """Load Q-table from qtable.json or create a new one."""
    if os.path.exists(Q_FILE):
        try:
            with open(Q_FILE, "r") as f:
                data = json.load(f)
                # Ensure both states exist
                for k in ["0", "1"]:
                    if k not in data:
                        data[k] = DEFAULT_Q[k]
                return data
        except Exception:
            # If file is corrupted, reset to default
            return DEFAULT_Q.copy()
    else:
        # Create new file with default values
        with open(Q_FILE, "w") as f:
            json.dump(DEFAULT_Q, f)
        return DEFAULT_Q.copy()


def _save_q(Q):
    """Persist Q-table to qtable.json."""
    try:
        with open(Q_FILE, "w") as f:
            json.dump(Q, f)
    except Exception:
        # In worst case, ignore write errors to avoid crashing honeypot
        pass


# Global Q-table in memory
Q = _load_q()


def choose_action(state: str) -> int:
    """
    Epsilon-greedy action selection.
    state: "0" (normal) or "1" (attack)
    returns: 0 (low deception) or 1 (high deception)
    """
    # Exploration
    if random.random() < epsilon:
        return random.choice([0, 1])

    # Exploitation: choose action with highest Q-value
    values = Q.get(state, DEFAULT_Q[state])
    max_val = max(values)
    # Return index of max value -> 0 or 1
    return values.index(max_val)


def update_q(state: str, action: int, reward: float):

    if state not in Q:
        Q[state] = DEFAULT_Q[state][:]

    current = Q[state][action]
    best_next = max(Q[state])
    target = reward + gamma * best_next
    new_value = current + alpha * (target - current)
    Q[state][action] = new_value

    # Log RL learning update
    try:
        with open("logs.txt", "a") as lf:
            lf.write(
                f"[{datetime.now()}] [RL] Updated state={state} action={action} → {Q[state][action]:.3f}\n"
            )
    except:
        pass

    # persist updates so Streamlit UI can see RL learning in real-time
    _save_q(Q)
