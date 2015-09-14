import time

threshold_exceeded_time = time.time()
last_alert = time.time()

while True:
    time.sleep(2)
    now = time.time()
    diff = now - last_alert
    if diff > 10:
        last_alert = time.time()
        print "alerting"

    print diff
    print now