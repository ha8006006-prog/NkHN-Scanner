[app]
title = HN
package.name = hnscanner
package.domain = org.hn.network
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Build for both 64-bit and 32-bit Android devices so it works on all phones
android.archs = arm64-v8a, armeabi-v7a

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

[buildozer]
log_level = 2
warn_on_root = 1
