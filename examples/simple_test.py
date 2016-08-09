import pylibAtlas
import random

if __name__ == '__main__':

    db_test = 'test1.sqlite'
    table_test = 'tb_test'

    pylibAtlas.create_table(db_test, table_test)

    for i in range(10):
        pylibAtlas.insert_data(db_test, table_test, random.uniform(1.0, 3.0))

    print "Last value:", pylibAtlas.get_last_value(db_test, table_test)
    #
    print "Max value: ", pylibAtlas.get_max_value(db_test, table_test)
    print "Min value: ", pylibAtlas.get_min_value(db_test, table_test)

    print "Table name: ", pylibAtlas.get_table_name(db_test)

    # export to excel file which has same file name with db file.
    print "Exporting: ", pylibAtlas.export_xls('test1.sqlite')
