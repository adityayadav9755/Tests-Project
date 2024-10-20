import matplotlib.pyplot as plt
import table_ops as to
import numpy as np
import pandas as pd

con = to.con
cur = to.cur

def ans_menu():
    choice1 = int(input('''\n-> What will you like to see?
1.Test scores
2.Aggregate
Enter choice(corresponding number):'''))
    if choice1 == 1:
        graph()
    elif choice1 == 2:
        choice3 = int(input('''\n-> Choose the type of function
1.Average marks
2.Maximum marks
3.Minimum marks
Enter choice(corresponding number):'''))
        if choice3 == 1:
            avgm()
        elif choice3 == 2:
            maxm()
        elif choice3 == 3:
            minm()
        else:
            print("-> Please enter a valid value!")

    elif choice1 == 3:
        print("-> Thank You for using!")
    else:
        print("-> Please enter a valid value!")
        
    if choice1 != 3:
        choice2 = int(input("\n-> What do you want to do next?\n1.Continue with analysis menu\n2.Exit analysis menu\nEnter choice:"))
        if choice2 == 1:
            ans_menu()
        elif choice2 == 2:
            print("-> Thank You for using!")
        else:
            print("-> You did not enter a valid value!")


def graph():
    cur.execute("select * from Tests order by date")
    df = pd.DataFrame(cur.fetchall())
    mains = df.loc[df[4]=="mains", 3]
    adv = df.loc[df[4]=="adv", 3]
    spt = df.loc[df[4]=="spt", 3]
    plt.plot(np.arange(1, len(mains)+1), mains, label="Mains")
    plt.plot(np.arange(1, len(adv)+1), adv, label="Advanced")
    plt.plot(np.arange(1, len(spt)+1), spt, label="SPT")
    plt.xticks(np.arange(1, max(len(mains), len(adv), len(spt))+1))
    plt.legend()
    plt.title("Test Marks")
    plt.show()


def data():
    cur.execute("select * from tests order by date")
    df = pd.DataFrame(cur.fetchall())
    df1 = df[df[1]=="XI"]
    df2 = df[df[1]=="XII"]
    return [df1.loc[df[4]=="mains", 3], df1.loc[df[4]=="adv", 3],
            df1.loc[df[4]=="spt", 3], df2.loc[df[4]=="mains", 3],
            df2.loc[df[4]=="adv", 3], df2.loc[df[4]=="spt", 3],
            df.loc[df[4]=="mains", 3], df.loc[df[4]=="adv", 3],
            df.loc[df[4]=="spt", 3]]
    

def avgm():
    l = data()
    dic = {"XI":[l[0].mean(), l[1].mean(), l[2].mean()],
           "XII":[l[3].mean(), l[4].mean(), l[5].mean()],
           "Overall":[l[6].mean(), l[7].mean(), l[8].mean()]}
    daf = pd.DataFrame(dic, index=["Mains", "Advance", "SPT"])
    daf.plot(kind="bar")
    plt.title("Average Marks")
    plt.legend()
    plt.show()
    

def maxm():
    l = data()
    dic = {"XI":[l[0].max(), l[1].max(), l[2].max()],
           "XII":[l[3].max(), l[4].max(), l[5].max()],
           "Overall":[l[6].max(), l[7].max(), l[8].max()]}
    daf = pd.DataFrame(dic, index=["Mains", "Advance", "SPT"])
    daf.plot(kind="bar")
    plt.title("Maximum Marks")
    plt.legend()
    plt.show()
    
    
def minm():
    l = data()
    dic = {"XI":[l[0].min(), l[1].min(), l[2].min()],
           "XII":[l[3].min(), l[4].min(), l[5].min()],
           "Overall":[l[6].min(), l[7].min(), l[8].min()]}
    daf = pd.DataFrame(dic, index=["Mains", "Advance", "SPT"])
    daf.plot(kind="bar")
    plt.title("Minimum Marks")
    plt.legend()
    plt.show()
    