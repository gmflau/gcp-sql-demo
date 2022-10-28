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
import sqlalchemy
from google.cloud import pubsub_v1

# Initialize DB connection parameters
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
table_name = "car_dealers"
table_field = "id,make,model,year,state"


# PostgreSQL
driver_name = 'postgres+pg8000'
query_string =  dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(db_connection_name)})

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


    table_field_value = (parsed_json['data']['message']['channel']).split(':')[2] + ",'toyota','4runner','2011','CA'"    
    #table_field_value = "2001,'toyota','4runner','2011','CA'"
    print("** table_field_value => " + table_field_value)
    stmt = sqlalchemy.text('insert into {} ({}) values ({})'.format(table_name, table_field, table_field_value))    
    print("** db_password => ")
    print(db_password)
    print("** user => ")
    print(db_user)
    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername=driver_name,
        username=db_user,
        password=db_password,
        database=db_name,
        query=query_string,
      ),
      pool_size=5,
      max_overflow=2,
      pool_timeout=30,
      pool_recycle=1800
    )
    try:
        with db.connect() as conn:
            conn.execute(stmt)
    except Exception as e:
        print('** Error: {}'.format(str(e)))
        return 'Error: {}'.format(str(e))
    return 'ok'
