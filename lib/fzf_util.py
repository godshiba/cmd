import shutil
import subprocess


def run_fzf(cmd, lines):
    """Run fzf: items via stdin, selection via stdout, keyboard via /dev/tty."""
    if not shutil.which("fzf"):
        return None

    result = subprocess.run(
        cmd,
        input="\n".join(lines),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    if not result.stdout or not result.stdout.strip():
        return None
    return result.stdout.strip()