import network
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("sejuAp_0", "123456789a")

