# Copyright 2022 Redis, Inc.
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
import datetime
import json
from flask import Flask
from google.cloud import pubsub_v1

# Configure the following environment variables via app.yaml
pubsub_topic = os.environ['PUBSUB_TOPIC']
google_cloud_project = os.environ['GOOGLE_CLOUD_PROJECT']
redis_host = os.environ['REDIS_HOST']
redis_port = os.environ['REDIS_PORT']
redis_password = os.environ['REDIS_PASSWORD']


def process():
    # Subcribe to all keyspaces changes (KEA)
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port,
                   password=redis_password, decode_responses=True)
    ps = redis_client.pubsub()
    ps.psubscribe('__keyspace@0__:*')

    publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
    publisher = pubsub_v1.PublisherClient(publisher_options=publisher_options)

    topic_path = publisher.topic_path(google_cloud_project, pubsub_topic)

    for message in ps.listen():
        print("Insdie for loop")
        if message is None:
           continue

        message_json = json.dumps({
            'data': {'message': message},
        })
        message_bytes = message_json.encode('utf-8')
        print(message_bytes)
        ordering_key = "write-behind"

        # Publishes a message
        try:
            future = publisher.publish(topic_path, data=message_bytes, ordering_key=ordering_key)
            print("FUTURE => " + future.result())  # Verify the publish succeeded
        except Exception as e:
            print(e)


if __name__ == "__main__":
    process()


