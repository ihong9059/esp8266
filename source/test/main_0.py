import network, machine
def wifiAp():
    import ubinascii
    ap_if = network.WLAN(network.AP_IF)
    essid = b"UTTEC-%s" % ubinascii.hexlify(ap_if.config("mac")[-3:])
    ap_if.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=b"123456789a")
