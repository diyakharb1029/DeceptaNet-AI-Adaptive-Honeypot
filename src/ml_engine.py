# ai_module.py

attack_keywords = [
    "rm", "chmod", "wget", "curl", "nmap",
    "passwd", "sudo", "ssh", "mv", "netcat",
    "python3", "nc", "perl", "scp"
]


def detect_attack(command: str) -> str:
    """
    Returns 'attack' if command contains dangerous keywords,
    otherwise 'normal'.
    """
    cmd = command.lower()

    for keyword in attack_keywords:
        if keyword in cmd:
            return "attack"
    return "normal"
