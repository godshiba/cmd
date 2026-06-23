import os
import shutil
import subprocess


def run_fzf(cmd, lines):
    """Run fzf: items via stdin, selection via stdout, keyboard via /dev/tty."""
    if not shutil.which("fzf"):
        return None

    input_data = "\n".join(lines)
    run_cmd = cmd

    if os.environ.get("FINDCMD_FROM_ZLE") and shutil.which("fzf-tmux"):
        run_cmd = ["fzf-tmux", "-d", "85%"] + cmd[1:]

    result = subprocess.run(
        run_cmd,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    if not result.stdout or not result.stdout.strip():
        return None
    return result.stdout.strip()