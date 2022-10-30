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


def execute(db, msg_json):
    channel = msg_json['data']['message']['channel']
    db_key = channel.split(':')[2]
    table_name = channel.split(':')[1]

    stmt = sqlalchemy.text('select count(*) from {} where id={}'.format(table_name, db_key))
    try:
        with db.connect() as conn:
            result = conn.execute(stmt)
            row = result.fetchone()
            print(row[0])
            if row[0] > 0:
               print("** row EXISTS")
               print("** delete existing row")
               stmt = sqlalchemy.text('delete from {} where id={}'.format(table_name, db_key))
               conn.execute(stmt)
               return
            else:
               print("** row not found in SQL table")
               return
    except Exception as e:
        print('** Error: {}'.format(str(e)))
        return 'Error: {}'.format(str(e))
    
