import mysql.connector as mc
import pandas as pd

h = "localhost"
p = "Aditya2612"
u = "root"

try:
    con = mc.connect(host=h, passwd=p, user=u)
    cur = con.cursor()
except Exception as e:
    print(e)

try:
    cur.execute("create database if not exists meradb1")
    cur.execute("use meradb1")
    table_creation = '''create table if not exists tests (testname varchar(30), 
    class varchar(4), 
    totalmarks int(4),
    obtainedmarks int(4),
    type varchar(6),
    percentage int(3),
    percentile decimal(5,2),
    date date,
    primary key(testname, class))'''
    cur.execute(table_creation)
    con.commit()
except Exception as e:
    print(e)

def to_menu():
    choice1 = int(input('''\n-> Which operation would you like to perform?
1.Insert data
2.Read data
3.Update data
4.Delete data
Enter choice(corresponding number):'''))
    if choice1 == 1:
        insert()
    elif choice1 == 2:
        read()
    elif choice1 == 3:
        update()
    elif choice1 == 4:
        delete()
    else:
        print("-> Please enter a valid value!")
        
    choice2 = int(input("\n-> What do you want to do next?\n1.Continue with table menu\n2.Exit table menu\nEnter choice:"))
    if choice2 == 1:
        to_menu()
    elif choice2 == 2:
        print("-> Thank You for using!")
    else:
        print("-> You did not enter a valid value!")
    

def insert():
    tn = input("Enter test name:")
    cl = input("Enter class(XI/XII):")
    tm = int(input("Enter total marks:"))
    obm = int(input("Enter obtained marks:"))
    typ = input("Enter type of test(mains/adv/spt):")
    pile = float(input("Enter percentile:"))
    page = (obm*100)/tm
    dat = input("Enter date of test in \'yyyy-mm-dd\' format:")
    cur.execute(f"insert into tests values('{tn}', '{cl}', {tm}, {obm}, '{typ}', floor({page}), {pile}, '{dat}')")
    con.commit()
    print("-> Data entered successfully!")
    
def read():
    print()
    index = []
    cur.execute("desc Tests")
    for x in cur.fetchall():
        index.append(x[0])
    cur.execute("select * from Tests")
    df = pd.DataFrame(cur.fetchall())
    if df.empty == False:
        df.columns = index
    print(df)
    print()
        
def delete():
    print("Enter details of the row to be deleted.")
    cl = input("Class:")
    tn = input("Test name:")
    cur.execute(f"select count(*) from Tests where class='{cl}' and testname='{tn}'")
    count = cur.fetchone()[0]
    if count != 0:
        cur.execute(f"delete from Tests where class='{cl}' and testname='{tn}'")
        con.commit()
        print("-> Data deleted successfully!")
    else:
        print("-> No such row found!")
        
def update():
    print("Enter details of the row to be updated.")
    cl = input("Class:")
    tn = input("Test name:")
    cur.execute(f"select count(*), totalmarks, obtainedmarks from Tests where class='{cl}' and testname='{tn}'")
    l = cur.fetchone()
    count = l[0]
    tm = l[1]
    om = l[2]
    if count != 0:
        cur.execute("desc Tests")
        print("\nColumns:")
        for x in cur.fetchall():
            print(x[0])
        clm = input("Which column do you want to change from these(full name):")
        if clm not in ["testname", "class", "type", "date"]:
            val = int(input("Enter new value:"))
            cur.execute(f"update tests set {clm}={val} where testname='{tn}' and class='{cl}'")
        else:
            val = input("Enter new value:")
            cur.execute(f"update tests set {clm}='{val}', where testname='{tn}' and class='{cl}'")
        con.commit()
        if clm == "obtainedmarks":
            new = (val*100)/tm
        if clm == "totalmarks":
            new = (om*100)/val
        cur.execute(f"update tests set percentage={new} where testname='{tn}' and class='{cl}'")
        con.commit()
        print("-> Data updated succesfully!")
    else:
        print("-> No such row found!")
    

