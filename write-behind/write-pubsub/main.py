# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import os
import redis
import time
import json
from flask import Flask
from google.cloud import pubsub_v1

app = Flask(__name__)

# Configure the following environment variables via app.yaml
app.config['PUBSUB_TOPIC'] = os.environ['PUBSUB_TOPIC']
app.config['GOOGLE_CLOUD_PROJECT'] = os.environ['GOOGLE_CLOUD_PROJECT']
app.config['REDIS_HOST'] = os.environ['REDIS_HOST']
app.config['REDIS_PORT'] = os.environ['REDIS_PORT']
app.config['REDIS_PASSWORD'] = os.environ['REDIS_PASSWORD']

redis_client = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'],
                   password=app.config['REDIS_PASSWORD'], decode_responses=True)


# Subcribe to all keyspaces changes (KEA)
pubsub = redis_client.pubsub()  
pubsub.psubscribe('__keyspace@0__:*')

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(app.config['GOOGLE_CLOUD_PROJECT'], app.config['PUBSUB_TOPIC'])


# Keyspace notification detection loop
while True:
    message = pubsub.get_message()
    time.sleep(0.5)
    if message is None:
       continue

    message_json = json.dumps({
        'data': {'message': message},
    })
    message_bytes = message_json.encode('utf-8')
    print(message_bytes)    

    # Publishes a message
    try:
        future = publisher.publish(topic_path, message_bytes)
        print("FUTURE => " + future.result())  # Verify the publish succeeded
    except Exception as e:
        print(e)


@app.route('/')
def main():
    return 'dummy!'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

