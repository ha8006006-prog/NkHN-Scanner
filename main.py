import socket
import threading
import subprocess
import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP",
    8080: "Proxy"
}

class HNScannerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)

        self.header = Label(
            text="[b]HN Network Scanner[/b]",
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.header)

        self.subnet_input = TextInput(
            text=self.get_local_subnet(),
            multiline=False,
            size_hint_y=None,
            height=45,
            font_size='16sp'
        )
        self.add_widget(self.subnet_input)

        self.scan_btn = Button(
            text="Start Network Scan",
            size_hint_y=None,
            height=55,
            background_color=(0.1, 0.6, 0.9, 1),
            font_size='18sp'
        )
        self.scan_btn.bind(on_press=self.start_scan_thread)
        self.add_widget(self.scan_btn)

        self.scroll = ScrollView()
        self.results_label = Label(
            text="Press 'Start Network Scan' to discover devices...",
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=True
        )
        self.results_label.bind(texture_size=self.results_label.setter('size'))
        self.scroll.add_widget(self.results_label)
        self.add_widget(self.scroll)

    def get_local_subnet(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            prefix = ".".join(local_ip.split(".")[:-1])
            return f"{prefix}."
        except Exception:
            return "192.168.1."

    def start_scan_thread(self, instance):
        self.scan_btn.disabled = True
        self.scan_btn.text = "Scanning..."
        self.results_label.text = "[*] Discovering active devices on your network...\n\n"
        threading.Thread(target=self.run_scan, daemon=True).start()

    def update_ui(self, text):
        self.results_label.text += text

    def finish_scan(self, count):
        self.results_label.text += f"\n[b][+] Scan Complete. Total active devices: {count}[/b]"
        self.scan_btn.disabled = False
        self.scan_btn.text = "Start Network Scan"

    def get_hostname(self, ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return "Unknown Device"

    def check_host(self, ip, active_list):
        open_ports = []
        is_alive = False

        for port, service in COMMON_PORTS.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            if sock.connect_ex((ip, port)) == 0:
                is_alive = True
                open_ports.append(f"{port}({service})")
            sock.close()

        if not is_alive:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            timeout_param = ['-w', '500'] if platform.system().lower() == 'windows' else ['-W', '1']
            cmd = ['ping', param, '1'] + timeout_param + [ip]
            res = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res == 0:
                is_alive = True

        if is_alive:
            hostname = self.get_hostname(ip)
            services_str = ", ".join(open_ports) if open_ports else "No common ports open"
            info = f"[b]IP:[/b] {ip} ({hostname})\n[b]Services:[/b] {services_str}\n" + ("-" * 35) + "\n"
            active_list.append(ip)
            Clock.schedule_once(lambda dt: self.update_ui(info))

    def run_scan(self):
        prefix = self.subnet_input.text.strip()
        if not prefix.endswith("."):
            prefix += "."

        threads = []
        active_devices = []

        for i in range(1, 255):
            ip = f"{prefix}{i}"
            t = threading.Thread(target=self.check_host, args=(ip, active_devices))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        Clock.schedule_once(lambda dt: self.finish_scan(len(active_devices)))

class HNApp(App):
    def build(self):
        self.title = "HN"
        return HNScannerLayout()

if __name__ == "__main__":
    HNApp().run()
