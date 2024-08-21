import mysql.connector as mc
import matplotlib.pyplot as plt
import numpy as np

try:
    con = mc.connect(host="localhost", passwd="Aditya2612", user="root", database="Analysis")
    cur = con.cursor()
except Exception as e:
    print(e)

def menu():
    choice1 = int(input("\nHow can I help you?\n1.Insert data\n2.Read data\n3.Show graph\n4.Exit\nEnter choice:"))
    if choice1 == 1:
        insert()
    elif choice1 == 2:
        read()
    elif choice1 == 3:
        graph()
    elif choice1 == 4:
        print("Use nhi krna tha to chalu kyu kiya be!")
        
    if choice1 != 4:
        choice2 = int(input("\nwhat do you want to do next?\n1.Continue\n2.Exit\nEnter choice:"))
        if choice2 == 1:
            menu()
        elif choice2 == 2:
            print("Thank You for using!")
    

def insert():
    tn = input("Enter test name:")
    cl = input("Enter class:")
    tm = int(input("Enter total marks:"))
    obm = int(input("Enter obtained marks:"))
    pile = float(input("Enter percentile:"))
    page = (obm*100)/tm
    cur.execute(f"insert into Tests values('{tn}', '{cl}', {tm}, {obm}, floor({page}), {pile})")
    con.commit()
    print("Data entered successfully!")
    
def read():
    cur.execute("select * from Tests")
    for a in cur.fetchall():
        print(a)
        
def graph():
    mains = []
    adv = []
    spt = []
    cur.execute("select ObtainedMarks from Tests where TotalMarks=300 order by Class")
    for x in cur.fetchall():
        mains.append(x[0])
    cur.execute("select ObtainedMarks from Tests where TotalMarks in(180, 192) order by Class")
    for x in cur.fetchall():
        adv.append(x[0])
    cur.execute("select ObtainedMarks from Tests where TotalMarks=96 order by Class")
    for x in cur.fetchall():
        spt.append(x[0])
    plt.plot(np.arange(len(mains)), mains, label="Mains")
    plt.plot(np.arange(len(adv)), adv, label="Advanced")
    plt.plot(np.arange(len(spt)), spt, label="SPT")
    plt.legend()
    plt.title("Test Scores")
    plt.show()

if __name__ == "__main__":
        menu()
