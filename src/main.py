import socket
import threading
from datetime import datetime

from ai_module import detect_attack
from adaptive_module import adaptive_response
from vfs_module import VirtualFileSystem, handle_shell_command  # if you use VFS
from config import MODE, ENTERPRISE_NAME  # 👈 NEW

from config import MODE

# Map config mode to log tag
MODE_TAG = "LOCAL-DEFENSE" if MODE == "LOCAL" else "ENTERPRISE-ECOM"

# Decide how to label this node in the logs / banner
MODE_UPPER = MODE.upper()

if MODE_UPPER == "LOCAL":
    DEPLOYMENT_LABEL = "LOCAL-DEFENSE"
    NODE_NAME = "local-honeypot-node"
else:
    DEPLOYMENT_LABEL = "ENTERPRISE-ECOM"
    NODE_NAME = "ecom-decoy-node-1"



LOG_FILE = "logs.txt"


def log(entry: str):
    """
    Writes logs with timestamps AND deployment label into logs.txt.
    Example:
    [2025-12-06 18:10:12] [LOCAL-DEFENSE] [+] Connection from ('127.0.0.1', 54012)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{DEPLOYMENT_LABEL}] {entry}\n")


def generate_banner() -> bytes:
    """
    Fake SSH banner that changes text depending on deployment mode.
    """
    if MODE_UPPER == "LOCAL":
        env_line = "DeceptaNet Local Defense Node"
    else:
        env_line = f"DeceptaNet Enterprise Decoy – {ENTERPRISE_NAME}"

    banner = (
        f"{env_line}\n"
        f"{NODE_NAME} tty1\n"
        "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3\n\n"
        "login: "
    )
    return banner.encode()



def handle_client(client_socket, addr):
    """
    Per-connection handler: virtual shell + AI + RL.
    """
    vfs = VirtualFileSystem()
    log(f"[+] Connection from {addr} on {NODE_NAME}")




    client_socket.send(generate_banner())

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            command = data.decode(errors="ignore").strip()
            if not command:
                client_socket.send(b"> ")
                continue

            log(f"[CMD] {command}")

            # 1) AI classification
            prediction = detect_attack(command)
            log(f"[AI] {prediction}")

            # 2) Try shell simulation (ls, cd, etc.)
            handled, shell_output = handle_shell_command(vfs, command)

            # 3) RL-driven deception response
            response = adaptive_response(
                prediction,
                command,
                MODE_TAG
            )

            # flatten newlines for log readability
            log(f"{response.splitlines()[0]}")  # store only header of RESP

            # 4) Send full response back
            client_socket.send((response + "\n> ").encode())

    except Exception as e:
        log(f"[ERROR] {addr} -> {e}")

    finally:
        log(f"[DISCONNECTED] {addr}")
        client_socket.close()


def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 2222))
    server.listen(10)

    print("[+] DeceptaNet Honeypot running on port 2222...")

    while True:
        client, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(client, addr), daemon=True)
        t.start()


if __name__ == "__main__":
    start_honeypot()
