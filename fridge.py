from ConfigParser import SafeConfigParser
import os
import time
import datetime
from nanpy import (ArduinoApi, SerialManager, DallasTemperature)
from alarms import sound, instapush

settings = SafeConfigParser()
settings.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))

# Load settings
device = settings.get('Arduino', 'SERIAL_PORT')
pin_sound = settings.getint('Arduino', 'PIN_SOUND')
pin_temp = settings.getint('Arduino', 'PIN_TEMPERATURE')
app_id = settings.get('Instapush', 'INSTAPUSH_APP_ID')
app_secret = settings.get('Instapush', 'INSTAPUSH_APP_SECRET')
event_id = settings.get('Instapush', 'INSTAPUSH_EVENT_NAME')
threshold = settings.getfloat('Fridge', 'THRESHOLD')
notify_every_x_seconds = settings.getfloat('Fridge', 'NOTIFY_EVERY_X_SECONDS')
write_log_every_x_measurements = 50

# Startup arduino connection
connection = SerialManager(device=device)
connection.open()
arduino = ArduinoApi(connection=connection)
temperature_sensors = DallasTemperature(connection=connection, pin=pin_temp)
temperature_sensors.setResolution(12)


# Mute sound by default
arduino.pinMode(pin_sound, arduino.OUTPUT)
arduino.digitalWrite(pin_sound, 0)

# Initial values
last_alert = time.time()
threshold_reached = False
write_log_counter = 0

while True:
    temperature_sensors.requestTemperatures()
    temp = temperature_sensors.getTempC(0)  # Fetches the temperature on the first DS18B20 found on the pin.

    print temp

    if temp < -100 or temp == 0:
        # Bad reading, lets skip this result.
        continue

    if (temp >= threshold):
        if not threshold_reached:
            # Just reached the threshold, fire push alert
            threshold_reached = True
            last_alert = threshold_exceeded_time = time.time()
            message = "Diepvries: %s graden" % str(temp)
            print "Sending push: " + message
            instapush.send_push(app_id, app_secret, event_id, message)
        else:
            arduino.digitalWrite(pin_sound, 1)
            time.sleep(2)
            arduino.digitalWrite(pin_sound, 0)

            # Check if enough time has passed to send another alert.
            now = time.time()
            diff = now - last_alert
            if diff >= notify_every_x_seconds:
                # Send another alert
                last_alert = time.time()
                message = "Huidige temp diepvries: %s graden." % str(temp)
                print "Sending push: " + message
                instapush.send_push(app_id, app_secret, event_id, message)
    else:
        if threshold_reached:
            # Threshold not reached (anymore).
            threshold_reached = False
            # Lets notify we're back on track.
            message = "Diepvries terug in orde: %s graden." % str(temp)
            print "Sending push: " + message
            instapush.send_push(app_id, app_secret, event_id, message)

    if write_log_counter == 0:
        f = open('log.txt', 'a')
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y/%m/%d %H:%M")
        outstring = str(timestamp) + "  " + str(temp) + " C " + str(temp * 1.8 + 32) + " F" + "\n"
        f.write(outstring)
        f.close()
        write_log_counter = write_log_every_x_measurements

    write_log_counter -= 1
    time.sleep(2)
