# vfs_module.py

import os


class VirtualFileSystem:
    """
    Minimal fake Linux filesystem for the honeypot.
    """

    def __init__(self):
        # Nested dict = directories; strings = file contents
        self.fs = {
            "": {  # root "/"
                "home": {
                    "deceptanet": {
                        "README.txt": (
                            "DeceptaNet Honeypot Node\n"
                            "Confidential – For internal security research only.\n"
                        ),
                        "config.yml": (
                            "server:\n"
                            "  env: production\n"
                            "  role: deception-node\n"
                            "db:\n"
                            "  host: 10.0.0.5\n"
                            "  user: root\n"
                            "  pass: ********\n"
                        ),
                        "secrets.txt": (
                            "DB_PASSWORD=p@ssw0rd\n"
                            "API_KEY=DECEPTA-FAKE-KEY-123\n"
                        ),
                    }
                },
                "var": {
                    "log": {
                        "auth.log": "[sample] sshd: Failed password for root from 185.23.10.5\n",
                        "syslog": "[sample] systemd[1]: Started DeceptaNet service.\n",
                    }
                },
                "etc": {
                    "passwd": (
                        "root:x:0:0:root:/root:/bin/bash\n"
                        "decepta:x:1001:1001::/home/decepta:/bin/bash\n"
                    )
                }
            }
        }
        self.cwd = "/home/deceptanet"

    # --------- path utilities ---------

    def _norm(self, path: str) -> str:
        if not path:
            return self.cwd
        if not path.startswith("/"):
            path = os.path.join(self.cwd, path)

        parts = []
        for p in path.split("/"):
            if p in ("", "."):
                continue
            if p == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(p)

        return "/" + "/".join(parts)

    def _walk(self, path: str):
        """
        Walk into self.fs using a normalized path, returns (node, last_name)
        """
        normalized = self._norm(path)
        parts = [p for p in normalized.split("/") if p]

        node = self.fs[""]
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                return node, part
            if part not in node or not isinstance(node[part], dict):
                raise FileNotFoundError(normalized)
            node = node[part]

        # root
        return node, ""

    # --------- basic shell-like operations ---------

    def pwd(self) -> str:
        return self.cwd

    def ls(self, path: str | None = None) -> str:
        base_path = self._norm(path or self.cwd)
        node, last = self._walk(base_path)

        if last:
            # expecting directory
            if last not in node or not isinstance(node[last], dict):
                raise NotADirectoryError(base_path)
            node = node[last]

        entries = sorted(node.keys())
        return "  ".join(entries) + ("\n" if entries else "\n(empty)\n")

    def cd(self, path: str) -> str:
        target = self._norm(path)
        node, last = self._walk(target)

        if last:  # not root
            if last not in node or not isinstance(node[last], dict):
                raise NotADirectoryError(target)

        self.cwd = target
        return self.cwd

    def cat(self, path: str) -> str:
        base_path = self._norm(path)
        node, last = self._walk(base_path)

        if not last:
            raise IsADirectoryError(base_path)

        if last not in node or isinstance(node[last], dict):
            raise FileNotFoundError(base_path)

        return node[last]


def handle_shell_command(vfs: VirtualFileSystem, command: str) -> tuple[bool, str]:
    """
    Parse simple shell commands: pwd, ls, cd, cat, clear.
    Returns (handled, output).
    """
    parts = command.strip().split()
    if not parts:
        return True, ""

    cmd = parts[0]
    args = parts[1:]

    try:
        if cmd == "pwd":
            return True, vfs.pwd() + "\n"

        elif cmd == "ls":
            path = args[0] if args else None
            return True, vfs.ls(path)

        elif cmd == "cd":
            if not args:
                # default to home
                output = vfs.cd("/home/deceptanet")
            else:
                output = vfs.cd(args[0])
            return True, output + "\n"

        elif cmd == "cat":
            if not args:
                return True, "Usage: cat <file>\n"
            return True, vfs.cat(args[0]) + "\n"

        elif cmd == "clear":
            # terminal clear simulation
            return True, "\n" * 40

        else:
            return False, ""

    except FileNotFoundError:
        return True, f"bash: {command}: No such file or directory\n"
    except NotADirectoryError:
        return True, f"bash: not a directory\n"
    except IsADirectoryError:
        return True, f"bash: is a directory\n"
    except Exception as e:
        return True, f"bash: error: {e}\n"
