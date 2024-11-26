import sqlalchemy as db
from sqlalchemy import func
# from sqlalchemy import text as sqltext, select, MetaData, Table, Column
from sqlalchemy_utils import database_exists, create_database
import datetime


import src.db_functions as dbf
import src.db_conn as dbc

def create_db():

    #############################
    # Define Database Engine

    try:
        db_engine = dbc.db_connection()
        print("Database Connection established")
    except Exception as e:
        print("Database Connection could not be established.", e)

    #############################
    # create new Database

    print("Creating Database....")

    create_database(db_engine.url)

    metadata = db.MetaData()

    print("Creating Tables....")

    cheerlights_logs = db.Table('cheerlights_logs', metadata,
                    db.Column('application',db.String(50)),
                    db.Column('username',db.String(500)),
                    db.Column('userid',db.String(500)),
                    db.Column('message',db.String(500)),
                    db.Column('color',db.String(500)),
                    db.Column('dt_stamp',db.DateTime, server_default=func.now()),
    )

    metadata.create_all(db_engine)