import sqlite3, csv
from sqlite3 import Error
import pandas
import click
from flask import current_app, g


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['Reactions_DB'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def update_table_with_csv(conn,update_table_sql):
    df = pandas.read_csv(update_table_sql)

    if update_table_sql[:-4]=="elements":
            table_to_update="elements"
            print("success")
    
    if update_table_sql[:-4]=="gammaexcel":
        table_to_update="gamma"
        
    if update_table_sql[:-4]=="xray":
       table_to_update="xray"
    
    if update_table_sql[:-4]=="energy":
       table_to_update="crossSection"


    df.to_sql(table_to_update, conn, if_exists="append", index=False)



def main():
    database="Reactions_DB.db"

    conn=sqlite3.connect(database)

    if conn is not None:
        #create_table(conn,"CREATE.sql")
        #update_table_with_csv(conn,"energy.csv")
        # c=conn.cursor()
        # c.execute("""
        #     ALTER TABLE crossSection
        #     ADD COLUMN error""")
        update_table_with_csv(conn,"gammaexcel.csv")
    else:
        print("error!!!! No database connection")




if __name__== "__main__":
    main()

