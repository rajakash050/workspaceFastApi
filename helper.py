from db_connection import DB
import time
import base64

BESTSCORE = 12
db_name = "playcards"
TOTALCARDS = 12
DBSTRING = "mysql+pymysql://root:@127.0.0.1:3306/"


def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def get_sql_data_list(sql_query):
    """
    Fetches the data from mysql db
    """
    print("Connecting to ", db_name)
    print("Querying : ", sql_query)
    result = []
    sql_connection_flag = False
    for i in range(0, 3):
        try:
            cur = DB.get_db(DBSTRING, db_name)
            # Get the cursor to execute the query
            result2 = cur.execute(sql_query)
            result = result2.fetchall()
            sql_connection_flag = True
            return result, sql_connection_flag
        except Exception as err:
            print("ERROR: Cannot connect to SQL" + str(err))
            time.sleep(3)
            DB.reset_db_conn(DBSTRING, db_name)
            continue
    return result, sql_connection_flag


def writeToSql(query):
    '''
    func to insert in DB
    '''
    print("Connecting to Db : ", db_name)
    print("Querying for : ", query)
    db_conn = None
    for i in range(0, 3):
        try:
            db_conn = DB.get_db(DBSTRING, db_name)

            # db_conn.begin()
            db_conn.execute(query)
            print("Data inserted into MySQL")
            return 1
        except Exception as e:
            print("Trying to writing data into mysql: ", e)
            time.sleep(2)
            DB.reset_db_conn(DBSTRING, db_name)

    print("Error in writing data into mysql for query : ", query)
    return 0