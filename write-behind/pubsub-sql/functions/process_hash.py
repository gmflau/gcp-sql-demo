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


def hset(db, redis_client, msg_json):
    channel = msg_json['data']['message']['channel']
    redis_key = channel.split(':')[1] + ":" + channel.split(':')[2]
    db_key = channel.split(':')[2]
    print('redis_key = {}, db_key = {}'.format(redis_key, db_key))

    # TO DO:  
    # hgetall from Redis from key
    # construct table_field_value accordingly
    redis_hash_key = redis_client.hkeys(redis_key)
    redis_hash_value = redis_client.hvals(redis_key)
    redis_hash_key_value = redis_client.hgetall(redis_key)
    for key in redis_hash_key:
        print('Key = {}, Value = {}'.format(key, redis_hash_key_value[key]))
    table_name = channel.split(':')[1]
    table_column = 'id,' + ','.join(redis_hash_key)
    redis_hash_value.insert(0, db_key)
    table_column_value = ','.join("'" + item + "'" for item in redis_hash_value)
    #table_column_value = db_key + ',' + ','.join("'" + item + "'" for item in redis_hash_value)
    print('table_column = {}, table_column_value = {}'.format(table_column, table_column_value))

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
               stmt = sqlalchemy.text('insert into {} ({}) values ({})'.format(table_name, table_column, table_column_value)) 
               conn.execute(stmt)
            return
    except Exception as e:
        print('** Error: {}'.format(str(e)))
        return 'Error: {}'.format(str(e))
    
