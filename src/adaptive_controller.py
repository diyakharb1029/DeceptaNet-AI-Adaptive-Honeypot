# adaptive_module.py

from rl_module import update_q, choose_action

def adaptive_response(prediction: str, command: str, mode_tag: str = "LOCAL-DEFENSE"):
    """
    Adaptive Response Engine
    Now accepts MODE_TAG so local/enterprise deception can differ if needed.
    """

    # STATE:
    # 0 = normal
    # 1 = attack
    state = "1" if prediction == "attack" else "0"

    # RL decides deception type (0 low, 1 high)
    action = choose_action(state)

    # HIGH DECEPTION PATH
    if action == 1:
        response = f"[{mode_tag}] [RESP] [HIGH-DECEPTION] "
        if prediction == "attack":
            response += f"Security lockdown triggered for: {command}"
        else:
            response += f"Executed with enhanced sandboxing: {command}"
        reward = 1.0

    # LOW DECEPTION PATH
    else:
        response = f"[{mode_tag}] [RESP] [LOW-DECEPTION] Executed: {command}"
        reward = 0.4

    # Update Q-learning agent
    update_q(state, action, reward)

    return response
