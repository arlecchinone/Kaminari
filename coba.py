import pypyodbc as odbc
import random
from datetime import datetime

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-HFFP4M5'
DATABASE_NAME = 'kaminaribot'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
    uid=sa;
    pwd=P@ssw0rd;
"""

conn = odbc.connect(connection_string)
c = conn.cursor()
# sql = "SELECT * FROM player WHERE user_id=?"
id = "873940508504883261"
id2 = "1020875073550299156"

query2 = "SELECT userid FROM temp_inv WHERE executer=?"
user = c.execute(query2, (id, )).fetchone()

print(user[0])