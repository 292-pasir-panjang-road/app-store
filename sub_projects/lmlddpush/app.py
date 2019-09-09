from flask import Flask
from flask_restful import Resource, Api

import requests
import atexit
import json
import time
from datetime import datetime
from apscheduler.scheduler import Scheduler

app = Flask(__name__)

APP_KEY = "2815647836"
APP_SECRET = "52fcbb03a2ec45d54fd5c4b40a9582ba"
ACCESS_TOKEN = "2.00UICb9GmcKYED184c921789UvEILB"
WEIBO_API_TIME_FORMAT = "%a %b %d %H:%M:%S %z %Y"

REQUEST_URL = "https://api.weibo.com/2/statuses/home_timeline.json"


cron = Scheduler(daemon=True)
cron.start()


# Run once per hour, get the statuses posted in past hour and send to grp
@cron.interval_schedule(hours=1)
def job_function():
    statuses_to_send = get_timeline()
    if not statuses_to_send:
        return
    processed_statuses = [process_status(status) for status in statuses_to_send]
    for status_text in processed_statuses:
        send_msg(status_text)


# Send message to grp
def send_msg(status_text):
    # TODO: send to grp


# Process a status json obj to formatted text
def process_status(status):
    content = status['text']
    timestr = status['created_at']
    created_timestamp = datetime.strptime(timestr, WEIBO_API_TIME_FORMAT)
    formatted_timestr = datetime.strftime(created_timestamp, '%Y/%m/%d, %A, %H:%M:%S')
    return formatted_timestr + '\n' + content


# Get statuses in past hour
def get_timeline():
    url = REQUEST_URL
    get_params = {"access_token": ACCESS_TOKEN}
    response = requests.get(url, params=get_params)
    if (response.status_code != 200):
        # TODO: handle
        return

    response_json = json.loads(response.text)
    statuses = response_json['statuses']

    statuses_new = []
    for status in statuses:
        timestr = status['created_at']
        created_timestamp = datetime.strptime(timestr, WEIBO_API_TIME_FORMAT)
        created_secs = time.mktime(created_timestamp.timetuple())
        time_diff = time.time() - created_secs
        if (time_diff <= 3600):
            statuses_new.append(status)
        else:
            break
    
    return statuses_new
        



atexit.register(lambda: cron.shutdown(wait=False))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8000")
