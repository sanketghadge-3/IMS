import sqlite3
con=sqlite3  
def create_db():
    con =sqlite3.connect(database=r"ims.db")
    cur=con.cursor()
    cur.execute( "create table if not exists emp13(eid integer primary key autoincrement, name text,email text, gender text, contact text , dob text , doj text , pass text , utype text , address text , salary text )" )
    con.commit()
    
    cur.execute( "create table if not exists sup13(invoice integer primary key autoincrement, name text,contact text, desc text)" )
    con.commit()
    cur.execute( "create table if not exists cat13(cid integer primary key autoincrement, name text)" )
    con.commit()

    cur.execute( "create table if not exists pdt13(pid integer primary key autoincrement, Supplier text,Category text, name text, price text , qty text , status text)" )
    con.commit()


create_db()