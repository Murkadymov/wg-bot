import subprocess

def generate_private_key() -> str:
    return subprocess.check_output(["wg", "genkey"]).decode().strip()

def generate_public_key(private_key: str) -> str:
    return subprocess.run(
        ["wg", "pubkey"],
        input=private_key.encode(),
        capture_output=True,
        check=True
    ).stdout.decode().strip()


