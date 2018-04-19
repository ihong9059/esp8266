import network
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="sejuAp_0", authmode=network.AUTH_WPA_WPA2_PSK,
password="123456789a")
