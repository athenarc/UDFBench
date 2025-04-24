import apsw
import sys
import importlib
import importlib.util
import inspect
import pandas as pd
import time
import os

def register_functions(current_dir, conn):
    # Load the module dynamically
    for module_name in os.listdir(current_dir):
        if module_name.endswith(".py"):  
            spec = importlib.util.spec_from_file_location(current_dir,f"{current_dir}/{module_name}" )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


            # Iterate through module members
            for name, obj in inspect.getmembers(module):
                # Register scalar functions
                if inspect.isfunction(obj):
                    conn.createscalarfunction(name, obj)
                # Register aggregate functions
                elif inspect.isclass(obj):
                    if hasattr(obj, 'step') and hasattr(obj, 'final'):
                        agg_instance = obj()
                        setattr(obj, 'factory', classmethod(lambda cls:(cls(), cls.step, cls.final)))
                        conn.createaggregatefunction(name, obj.factory)


if len(sys.argv) != 5:
    print("Usage: python3 exec.py <database_name> <query_file> <udf module>")
    sys.exit(1)
    
start = time.time()
startpt = time.process_time()

database_name = sys.argv[1]
query_file = sys.argv[2]

conn = apsw.Connection(database_name)

register_functions(sys.argv[3], conn)
register_functions(sys.argv[4], conn)


with open(query_file, 'r') as file:
    sql_query = file.read()

# Execute SQL query
cursor = conn.cursor()
cursor.execute(sql_query)
results = cursor.fetchall()

end = time.time()
endpt = time.process_time()

print(f'Execution Time: {(end-start)*1000:.3f} ms\n')
print(f'Process Time: {(endpt-startpt)*1000:.3f} ms\n')


conn.close()
