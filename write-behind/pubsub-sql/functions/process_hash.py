# Copyright 2022 Redis, Inc.
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

import sqlalchemy
import os


table_name = "car_dealers"
table_field = "id,make,model,year,state"

def hset(db, redis_client, msg_json):
    channel = msg_json['data']['message']['channel']
    redis_key = channel.split(':')[1] + ":" + channel.split(':')[2]
    db_key = channel.split(':')[2]
    print('redis_key = {}, db_key = {}'.format(redis_key, db_key))

    # TO DO:  
    # hgetall from Redis from key
    # construct table_field_value accordingly
    redis_res = redis_client.hgetall(redis_key)
    print(redis_res)
    table_field_value = db_key + ",'toyota','4runner','2011','CA'"   
    print("** table_field_value => " + table_field_value)

    stmt = sqlalchemy.text('select count(*) from {} where id={}'.format(table_name, db_key))
    try:
        with db.connect() as conn:
            result = conn.execute(stmt)
            row = result.fetchone()
            print(row[0])
            if row[0] > 0:
               print("** row EXISTS")
               # TO DO: Update SQL
            else:
               print("** new row")
               stmt = sqlalchemy.text('insert into {} ({}) values ({})'.format(table_name, table_field, table_field_value)) 
               conn.execute(stmt)
            return
    except Exception as e:
        print('** Error: {}'.format(str(e)))
        return 'Error: {}'.format(str(e))
    
