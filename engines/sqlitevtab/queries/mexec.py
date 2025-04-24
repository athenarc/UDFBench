#!/usr/bin/env python

from optparse import OptionParser
import sys
import apsw
#import YeSQL
import json
import functions
import time
def exitwitherror(txt):
    sys.stderr.write(txt+'\n')
    sys.exit(1)


def main():
    start=time.time()
    startpt = time.process_time()




    desc="""Use this program to run madSQL queries on data coming from standard input. You may provide a database to run your queries. Results are streamed to standard output.
    """
    parser = OptionParser(description=desc, usage="usage: %prog [options] [dbname] flowname",
                          version="%prog 1.0")
    parser.add_option("-f", "--flow",
                      help="flow file to execute")
    parser.add_option("-d", "--db",
                      help="db to connect")
    parser.add_option("-w", "--dbw",
                      help="db to connect (open in create mode)")


    (options, args) = parser.parse_args()

    dbname = ''
    flags = apsw.SQLITE_OPEN_READWRITE | apsw.SQLITE_OPEN_CREATE
    try:
        dbname = args[0]
        flags = apsw.SQLITE_OPEN_READWRITE
    except:
        pass

    if options.db != None:
        dbname = options.db
        flags = apsw.SQLITE_OPEN_READWRITE

    if options.dbw != None:
        dbname = options.dbw

    try:
        Connection=functions.Connection(dbname, flags)

    except Exception as e:
        exitwitherror("Error in opening DB: " + str(dbname) + "\nThe error was: " + str(e))

    flowname = None
    try:
        flowname = args[1]
    except:
        pass

    if options.flow != None:
        flowname = options.flow

    if flowname == None:
        parser.print_help()
        sys.exit(1)

    try:
        f = open(flowname,'r')
    except Exception as e:
        exitwitherror("Error in opening SQL flow: " + str(e))


    statement = f.readline()
    if not statement:
        sys.exit()

    set_temp = True
    while True:
        while not apsw.complete(statement):
            line = f.readline()
            statement += line
            if not line:
                 if statement.rstrip('\r\n')!='':
                    sys.stderr.write("Incomplete query:"+statement)
                 f.close()
                 sys.exit()
        try :

            if set_temp:
                Connection.cursor().execute("pragma temp_store_directory='.';\n")
                set_temp = False
            
            for row in Connection.cursor().execute(statement):
                pass

            statement = ''
        except Exception as e:
            exitwitherror("Error when executing query: \n"+statement+"\nThe error was: "+ str(e))

        end = time.time()
        endpt = time.process_time()
        print(f'Execution Time: {(end-start)*1000:.3f} ms')
        print(f'Process Time: { (endpt-startpt)*1000:.3f} ms')



if __name__ == '__main__':
    main()


