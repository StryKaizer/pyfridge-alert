# Code based on videos.cctvcamerapros.com/digital-io-alarm-in-out/send-push-notifications-from-raspberry-pi.html
import pycurl
import json
from StringIO import StringIO

def send_push(app_id, app_secret, event, message):


    buffer = StringIO()
    # use Curl to post to the Instapush API
    c = pycurl.Curl()

    # set Instapush API URL
    c.setopt(c.URL, 'https://api.instapush.im/v1/post')

    # setup custom headers for authentication variables and content type
    c.setopt(c.HTTPHEADER, ['x-instapush-appid: ' + app_id,
                            'x-instapush-appsecret: ' + app_secret,
                            'Content-Type: application/json'])

    # create a dictionary structure for the JSON data to post to Instapush
    json_fields = {}

    # setup JSON values
    json_fields['event'] = event
    json_fields['trackers'] = {}
    json_fields['trackers']['message'] = message

    postfields = json.dumps(json_fields)

    # make sure to send the JSON with post
    c.setopt(c.POSTFIELDS, postfields)

    # set this so we can capture the resposne in our buffer
    c.setopt(c.WRITEFUNCTION, buffer.write)

    # uncomment to see the post that is sent
    # c.setopt(c.VERBOSE, True)
    c.perform()
