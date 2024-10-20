import table_ops as to
import analysis as ans

def menu():
    choice1 = int(input('''\n-> How can I help you?
1.Table Operations
2.View Analysis
3.Exit
Enter choice(corresponding number):'''))
    if choice1 == 1:
        to.to_menu()
    elif choice1 == 2:
        ans.ans_menu()
    elif choice1 == 3:
        print("-> Thank You for using!")
    else:
        print("-> Please enter a valid value!")
        menu()
        
    if choice1 in [1, 2]:
        choice2 = int(input("\n-> What do you want to do next?\n1.Continue with main menu\n2.Exit application.\nEnter choice(corresponding number):"))
        if choice2 == 1:
            menu()
        elif choice2 == 2:
            print("-> Thank You for using!")
        else:
            print("-> You did not enter a valid value!")

menu()
