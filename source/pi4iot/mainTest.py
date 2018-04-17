import time

count = 0

while 1:
    if count > 10:
        break
    print('count:{}'.format(count))
    count += 1
    time.sleep(1)
    