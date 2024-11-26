import os

if os.path.exists('src'):
    # Import our Custom Libraries
    import src.db_functions as dbf
    import src.db_conn as dbc
    import src.db_create as cdb
else:
	#set the parent directory one level up and then import the src files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    sys.path.insert(0, parent_dir)  

    import src.db_functions as dbf
    import src.db_conn as dbc
    import src.db_create as cdb

###############################
# create new database
cdb.create_db()

print("Database Creation Complete.")