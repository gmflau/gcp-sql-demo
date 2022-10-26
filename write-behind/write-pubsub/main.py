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

redis_host = os.environ.get('REDISHOST', 'redis-14222.mc147-1.us-east1-mz.gcp.cloud.rlrcp.com')
redis_port = int(os.environ.get('REDISPORT', 14222))
redis_pass = os.environ.get('REDISPASSWORD', 'G9HxADlYc4ckq54fhxz5utv2fh8LxkB5')
#redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_pass, charset="utf-8", decode_responses=True)
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_pass, decode_responses=True)

pubsub = redis_client.pubsub()  
pubsub.psubscribe('__keyspace@0__:*')

project_id = "central-beach-194106"
publisher = pubsub_v1.PublisherClient()
topic_id = "glau-topic"
topic_path = publisher.topic_path(project_id, topic_id)

while True:
    message = pubsub.get_message()
    time.sleep(0.01)
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
        print(future.result())  # Verify the publish succeeded
    except Exception as e:
        print(e)


@app.route('/')
def main():
    return 'dummy!'

if __name__ == '__main__':
    app.run(debug=True)
