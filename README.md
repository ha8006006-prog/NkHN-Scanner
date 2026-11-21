# HN Network Scanner 🌐

**HN** is an open-source, cross-platform local network scanner designed to discover connected devices, hostnames, hardware vendors, and active services/open ports across your local network (LAN).

It includes **two versions** to run on every device:
1. **Cross-Platform GUI & Android App (`android_apk_version/`):** Built with Kivy so it runs smoothly on **Android (APK)** (both `arm64-v8a` and `armeabi-v7a` architectures, no root required) as well as **Windows, Linux, and macOS**.
2. **CLI Advanced ARP Scanner (`cli_version/`):** Built with Scapy for fast, deep ARP & MAC vendor scanning on desktop terminals.

## 🚀 Automatic APK Building (GitHub Actions)
This repository includes a `.github/workflows/build_apk.yml` file. When you push this code to GitHub, GitHub will **automatically compile and build the `HN.apk` file** for you in the **Actions** tab!

## 💻 Running on Desktop (Windows / Linux / macOS)
### GUI Version:
```bash
cd android_apk_version
pip install kivy
python main.py
```

### CLI Version:
```bash
cd cli_version
pip install -r requirements.txt
sudo python scanner.py -t 192.168.1.1/24
```

## ⚠️ Disclaimer
This tool is intended strictly for network administration, diagnostics, and educational purposes on networks you own or have explicit permission to manage.

## 📄 License
Licensed under the MIT License - see [LICENSE](LICENSE).
