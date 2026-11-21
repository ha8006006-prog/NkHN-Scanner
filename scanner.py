import socket
import argparse
import urllib.request
from scapy.all import ARP, Ether, srp

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    53: "DNS",
    80: "HTTP (Web)",
    443: "HTTPS (Secure Web)",
    445: "SMB (File Sharing)",
    3389: "RDP (Remote Desktop)",
    8080: "HTTP-Proxy"
}

def get_mac_vendor(mac_address):
    """جلب اسم الشركة المصنعة للجهاز بناءً على عنوان MAC"""
    try:
        url = f"https://api.macvendors.com/{mac_address}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.read().decode('utf-8')
    except Exception:
        return "Unknown Vendor"

def scan_ports(ip):
    """فحص المنافذ الشائعة لمعرفة الخدمات النشطة على الجهاز"""
    open_services = []
    for port, service in COMMON_PORTS.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        if sock.connect_ex((ip, port)) == 0:
            open_services.append(f"{port} ({service})")
        sock.close()
    return ", ".join(open_services) if open_services else "None detected"

def scan_network(ip_range):
    """اكتشاف الأجهزة المتصلة على الشبكة باستخدام بروتوكول ARP"""
    print(f"\n[*] Scanning network: {ip_range} ...")
    print("[*] Please wait, discovering devices and active services...\n")
    
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        ip = received.psrc
        mac = received.hwsrc
        vendor = get_mac_vendor(mac)
        services = scan_ports(ip)
        
        devices.append({
            'ip': ip,
            'mac': mac,
            'vendor': vendor,
            'services': services
        })

    return devices

def print_results(devices):
    """عرض النتائج في جدول منسق"""
    print(f"{'IP Address':<16} {'MAC Address':<19} {'Vendor':<25} {'Active Services / Ports'}")
    print("-" * 95)
    for device in devices:
        print(f"{device['ip']:<16} {device['mac']:<19} {device['vendor'][:23]:<25} {device['services']}")
    print(f"\n[+] Total devices found: {len(devices)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HN - Local Network Device & Service Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP range (e.g., 192.168.1.1/24)")
    args = parser.parse_args()

    try:
        discovered_devices = scan_network(args.target)
        print_results(discovered_devices)
    except PermissionError:
        print("\n[!] Error: Please run this script with Administrator / Root privileges (sudo).")
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")
