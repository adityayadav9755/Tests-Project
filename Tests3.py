import sqlite3 as sq
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

try:
    con = sq.connect("meradb3")
    cur = con.cursor()
except Exception as e:
    print(e)

try:
    table_creation = '''create table if not exists tests (testname varchar(30), 
    class varchar(4), 
    totalmarks int(4),
    obtainedmarks int(4),
    percentage int(3),
    percentile decimal(5,2),
    primary key(testname, class))'''
    cur.execute(table_creation)
    con.commit()
except Exception as e:
    print(e)

def menu():
    choice1 = int(input('''\nHow can I help you?
1.Insert data
2.Read data
3.Update data
4.Delete data
5.Show graph
6.Exit
Enter choice(corresponding number):'''))
    if choice1 == 1:
        insert()
    elif choice1 == 2:
        read()
    elif choice1 == 3:
        update()
    elif choice1 == 4:
        delete()
    elif choice1 == 5:
        graph()
    elif choice1 == 6:
        print("-> Use nhi krna tha to chalu kyu kiya be!")
    else:
        print("-> Dhang ki value daal gadhe!")
        
    if choice1 != 6:
        choice2 = int(input("\nWhat do you want to do next?\n1.Continue\n2.Exit\nEnter choice:"))
        if choice2 == 1:
            menu()
        elif choice2 == 2:
            print("-> Thank You for using!")
    

def insert():
    tn = input("Enter test name:")
    cl = input("Enter class:")
    tm = int(input("Enter total marks:"))
    obm = int(input("Enter obtained marks:"))
    pile = float(input("Enter percentile:"))
    page = (obm*100)/tm
    cur.execute(f"insert into tests values('{tn}', '{cl}', {tm}, {obm}, floor({page}), {pile})")
    con.commit()
    print("-> Data entered successfully!")
    
def read():
    print()
    cur.execute("select * from Tests")
    index = [desc[0] for desc in cur.description]
    df = pd.DataFrame(cur.fetchall())
    df.columns = index
    print(df)
    print()
        
def delete():
    count = 0
    print("Enter details of the row to be deleted.")
    cl = input("Class:")
    tn = input("Test name:")
    cur.execute(f"select * from Tests where class='{cl}' and testname='{tn}'")
    count = cur.fetchone()[0]
    if count != 0:
        cur.execute(f"delete from Tests where class='{cl}' and testname='{tn}'")
        con.commit()
        print("-> Data deleted successfully!")
    else:
        print("-> No such row found!")
        
def update():
    print("Enter details of the row to be deleted.")
    cl = input("Class:")
    tn = input("Test name:")
    cur.execute(f"select count(*) from Tests where class='{cl}' and testname='{tn}'")
    count = cur.fetchone()[0]
    if count != 0:
        cur.execute("select * from Tests")
        for x in cur.description:
            print(x[0])
        clm = input("Which column do you want to change from these(full name):")
        if clm not in ["testname", "class"]:
            val = int(input("Enter new value:"))
            cur.execute(f"update tests set {clm}={val} where testname='{tn}' and class='{cl}'")
        else:
            val = input("Enter new value:")
            cur.execute(f"update tests set {clm}='{val}', where testname='{tn}' and class='{cl}'")
        con.commit()
        print("-> Data updated succesfully!")
    else:
        print("-> No such row found!")
    

def graph():
    mains = []
    adv = []
    spt = []
    cur.execute("select obtainedmarks from Tests where totalmarks=300 order by class")
    for x in cur.fetchall():
        mains.append(x[0])
    cur.execute("select obtainedmarks from Tests where totalmarks in(180, 192) order by class")
    for x in cur.fetchall():
        adv.append(x[0])
    cur.execute("select obtainedmarks from Tests where totalmarks=96 order by class")
    for x in cur.fetchall():
        spt.append(x[0])
    plt.plot(np.arange(1, len(mains)+1), mains, label="Mains")
    plt.plot(np.arange(1, len(adv)+1), adv, label="Advanced")
    plt.plot(np.arange(1, len(spt)+1), spt, label="SPT")
    plt.xticks(np.arange(1, max(len(mains), len(adv), len(spt))+1))
    plt.legend()
    plt.title("Test Scores")
    plt.show()
    

if __name__ == "__main__":
    menu()
    con.close()
