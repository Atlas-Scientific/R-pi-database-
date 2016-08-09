import random
import sqlite3 as lite

import xlwt


def execute_query(db_name, query):
    """
    Executes given query.
    :param db_name: DB file name(full path is )
    """
    # print "Executing query: ", query
    try:
        conn = lite.connect(db_name)
        curs = conn.cursor()
        curs.execute(query)
        conn.commit()
        conn.close()
        return True

    except lite.Error as e:
        print("Error %s:" % e.args[0])
        return False


def request_query(db_name, query):
    """
    Send request and return received result.
    """
    # print "Requesting query:", query
    try:
        conn = lite.connect(db_name)
        curs = conn.cursor()
        curs.execute(query)
        result = curs.fetchall()
        conn.close()
        if result is not None:
            return [list(re) for re in result]
        else:
            return None

    except lite.Error as e:
        print("Error %s:" % e.args[0])
        return None


def create_table(db_name, table_name):
    """
    Create db file and also table as well with given parameters.

    :param db_name: path & file name of db file
    :param table_name: name of table
    """
    query = 'CREATE TABLE if NOT EXISTS ' + table_name + ' ( id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                                                         'date_time DATETIME, ' \
                                                         'val1 NUMERIC, ' \
                                                         'val2 NUMERIC, ' \
                                                         'val3 NUMERIC, ' \
                                                         'val4 NUMERIC ' \
                                                         ');'
    return execute_query(db_name, query)


def insert_data(db_name, table_name, val1, val2=0, val3=0, val4=0):
    """
    Insert data to db.
    :param db_name: path & file name of db file
    :param table_name: name of table
    :param val1: 1st value
    :param val2: 2nd value
    :param val3: 3rd value
    :param val4: 4th value
    """
    query = "INSERT INTO '" + table_name + \
            "' (date_time, val1, val2, val3, val4) values(datetime('now','localtime'), " + \
            str(val1) + ", " + str(val2) + ", " + str(val3) + ", " + str(val4) + ");"
    execute_query(db_name, query)


def get_last_value(db_name, table_name):
    """
    Get last record from the given table.
    :return : List of data in order of Date & Time, val1, val2, val3, val4
    """
    query = "select * from '" + table_name + "' ORDER BY id DESC LIMIT 1;"  # get last one

    q_result = request_query(db_name, query)

    return q_result[0]      # result is type of list


def get_max_value(db_name, table_name):
    """
    Get a record from the given table which has maximum sensor value.
    :return : List of data in order of Date & Time, val1, val2, val3, val4
    """
    query = 'SELECT * FROM ' + table_name + ' WHERE val1=(SELECT max(val1) FROM ' + table_name + ');'

    q_result = request_query(db_name, query)

    return q_result[0]      # result is type of list


def get_min_value(db_name, table_name):
    """
    Get a record from the given table which has minimum sensor value.
    :return : List of data in order of Date & Time, val1, val2, val3, val4
    """
    query = 'SELECT * FROM ' + table_name + ' WHERE val1=(SELECT min(val1) FROM ' + table_name + ');'

    q_result = request_query(db_name, query)

    return q_result[0]      # result is type of list


def get_table_name(db_name):
    """
    Get table name from the given database file.
    """
    query = 'SELECT name from sqlite_sequence'

    q_result = request_query(db_name, query)

    if q_result is not None:
        return q_result[0][0]   # result if list of lists
    else:
        return None


def export_xls(db_name):
    """
    Export sqlite db to excel file which has same name with db file.
    :param db_name: db file name
    """

    table_name = get_table_name(db_name)

    if table_name is None:
        print "Error, there is no table"
        return False

    str_query = "SELECT * FROM " + table_name
    data_list = request_query(db_name, str_query)

    if data_list is not None:
        try:
            workbook = xlwt.Workbook()
            worksheet = workbook.add_sheet(table_name)
            col = 0

            for rec_data in data_list:
                col += 1
                row = 0

                for cell_data in rec_data:
                    worksheet.write(col, row, cell_data)
                    row += 1

            worksheet.write(0, 0, "ID")
            worksheet.write(0, 1, "Data & Time")
            worksheet.write(0, 2, "Val1")
            worksheet.write(0, 3, "Val2")
            worksheet.write(0, 4, "Val3")
            worksheet.write(0, 5, "Val4")

            if db_name[-7:] == ".sqlite":
                xls_name = db_name[:-7] + ".xls"
            else:
                xls_name = db_name + ".xls"

            workbook.save(xls_name)
            return True
        except IOError as e:
            print e
            return False
    else:
        print "No data recorded."


if __name__ == '__main__':

    db_test = 'test1.sqlite'
    table_test = 'tb_test'

    create_table(db_test, table_test)

    for i in range(10):
        insert_data(db_test, table_test, random.uniform(1.0, 3.0))

    print "Last value:", get_last_value(db_test, table_test)
    #
    print "Max value: ", get_max_value(db_test, table_test)
    print "Min value: ", get_min_value(db_test, table_test)

    print "Table name: ", get_table_name(db_test)

    print "Exporting: ", export_xls('test1.sqlite')
