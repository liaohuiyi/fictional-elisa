import MySQLdb

def fetchone(host, user, pwd, db, sql):
    db = MySQLdb.connect(host, user, pwd, db)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
    except:
        print "Error: unable to fetch one data..."
    db.close()
    return results

def fetchall(host, user, pwd, db, sql):
    db = MySQLdb.connect(host, user, pwd, db)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print "Error: unable to fetch data..."
    db.close()
    return results

def executedmsqls(host, user, pwd, db, sqls):
    if sqls and len(sqls) > 0:
        db = MySQLdb.connect(host, user, pwd, db)
        cursor = db.cursor()
        try:
            for sql in sqls:
                cursor.execute(sql)
            db.commit()
        except:
            print "Error: unable to execute data manipulation sql..."
            db.rollback()
        db.close()
        return
    else:
        print 'no sqls......'

def executeddsqls(host, user, pwd, db, sqls):
    if sqls and len(sqls) > 0:
        db = MySQLdb.connect(host, user, pwd, db)
        cursor = db.cursor()
        try:
            for sql in sqls:
                cursor.execute(sql)
        except:
            print "Error: unable to execute data definition sql..."
        db.close()
        return
    else:
        print 'no sqls......'

if __name__ == '__main__':
    host = '127.0.0.1'
    user = 'efilm'
    pwd = 'efilm'
    db = 'efilm'
    sql = """
          SELECT dcmImg FROM INSTANCE WHERE studyId = '697338'
          """

    print 'SQL : ', sql
    print
    print 'Results :'
    results = fetchall(host, user, pwd, db, sql)
    i = 0
    if results:
        for result in results:
            i += 1
            print str(i).rjust(10), result[0]

    print

