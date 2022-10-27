# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_pubsub_publish]
import base64
import json
import os
import psycopg2
from google.cloud import pubsub_v1

# Initialize DB connection parameters
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# Create a DB connection
#host = '/cloudsql/{}'.format(db_connection_name)
#cnx = psycopg2.connect(dbname=db_name, user=db_user,
#          password=db_password, host=host)

# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()

# Triggered from a message on a Cloud Pub/Sub topic.
def pubsub_sql(event, context):
    # Print out the data from Pub/Sub, to prove that it worked
    #print(event['data'])
    print("Message from PubSub - Topic: glau-topic")
    message = base64.b64decode(event['data'])
    print(message)
    data = message.decode('utf-8')
    print(data)
    parsed_json=json.loads(data)
    print(parsed_json)
    print(parsed_json['data'])
    operation=parsed_json['data']['message']['data']
    print(parsed_json['data']['message']['data'])
    
    match operation:
        case 'hset':
            print("The operation is hset")
        case 'set':
            print("The operattion is set")
        case other:
            print("No match found")    



