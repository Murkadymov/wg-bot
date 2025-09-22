from pathlib import Path
import subprocess

CLIENTS_DIR = Path("/etc/wireguard/clients")
SERVER_IP= "77.105.132.226"
SERVER_PUBLIC_KEY = "2SLorn1s7LVdqtsuihcodb10bmWTReVt4LfVxTGKoxU="
WG_CONF = Path("/etc/wireguard/wg0.conf")

def generate_client_conf(user_id: int, private_key: str, client_ip: str) -> Path:
    CLIENTS_DIR.mkdir(parents=True, exist_ok=True)
    conf_path = CLIENTS_DIR / f"{user_id}.conf"

    content = f"""
[Interface]
PrivateKey = {private_key}
Address = {client_ip}/32
DNS = 1.1.1.1

[Peer]
PublicKey = {SERVER_PUBLIC_KEY}
Endpoint = {SERVER_IP}:51820
AllowedIPs = 0.0.0.0/0, ::/0
""".strip()

    conf_path.write_text(content, encoding="utf-8")
    return conf_path


def add_peer(public_key: str, client_ip: str):
    """Добавляет peer только в runtime (пропадёт после рестарта)"""
    subprocess.run(
        ["wg", "set", "wg0", "peer", public_key, "allowed-ips", f"{client_ip}/32"],
        check=True
    )


def add_peer_persistent(public_key: str, client_ip: str):

    subprocess.run(
        ["wg", "set", "wg0", "peer", public_key, "allowed-ips", f"{client_ip}/32"],
        check=True
    )

    if not WG_CONF.exists():
        raise FileNotFoundError(f"{WG_CONF} not found")

    text = WG_CONF.read_text(encoding="utf-8")
    if public_key in text or f"{client_ip}/32" in text:
        raise RuntimeError(f"{public_key} already added")

    with WG_CONF.open("a", encoding="utf-8") as f:
        f.write(
            f"\n[Peer]\nPublicKey = {public_key}\nAllowedIPs = {client_ip}/32\n"
        )
