import network
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("utsol_tc140", "09090909")
print(sta.ifconfig()[0])
