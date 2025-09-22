from pathlib import Path
import ipaddress
import re

WG_CONF = Path("/etc/wireguard/wg0.conf")
SUBNET = ipaddress.ip_network("10.0.0.0/24")

def get_used_ips() -> list[str]:
    """Парсит wg0.conf и возвращает список занятых IP-адресов клиентов"""
    if not WG_CONF.exists():
        raise FileNotFoundError(f"{WG_CONF} not found")

    text = WG_CONF.read_text(encoding="utf-8")
    return re.findall(r"AllowedIPs\s*=\s*([\d\.]+)/32", text)

def get_next_free_ip() -> str:
    """Возвращает первый свободный IP из пула"""
    used = set(get_used_ips())
    for ip in SUBNET.hosts():  # перебираем все адреса в сети
        ip_str = str(ip)
        if ip_str == "10.0.0.1":  # серверный адрес, пропускаем
            continue
        if ip_str not in used:
            return ip_str
    raise RuntimeError("Свободных IP-адресов в пуле не осталось")
