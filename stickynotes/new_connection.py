import pymysql

conn = pymysql.connect(
    host='localhost',
    user='swaralee', 
    passwd='swaralee@123', 
    db='StickyNotes')
cur = conn.cursor()

def execute_query(sql_query, query_type= None):
    try:
        cur.execute(sql_query)
        if query_type == 'insert':
            conn.commit()
        response = []
        for res in cur:
            response.append(res)
        return response
    except:
        pass
