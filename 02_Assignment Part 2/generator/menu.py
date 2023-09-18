from cmd import Cmd  # methods for accepting cmd inputs
from generator.attacktrees import insert_v, rsk_clc, file_insert, plot_tree, print_tree
# Importing from created module

# This is the command prompt file to navigate the program.
# the class inputs will contain the main functions of the program.


class Inputs(Cmd):
    """This class contains the main functions of the program the do_commands records the user input
    through the CLI
    """

    def do_ext(self, *args):
        """Terminates the program"""
        print("Program is now Terminated")
        exit()

    def do_plt(self, *args):
        """generates a  tree from the valuse in the json file"""
        plot_tree()
        menu()

    def do_ins(self, *args):
        """allows the user to modify the values of the tree in the json file"""
        insert_v()
        menu()

    def do_rsk(self, *args):
        """provides the total risk vaule based on the trees"""
        rsk_clc()
        menu()

    def do_prn(self, *args):
        """plots a .png of the tree created and saves it to directory"""
        print_tree()
        menu()


# A function to display the main menu for the user to insert the .jason file name
def main_menu():
    print(10 * "=" + " " + "Welcome to The Attack Tree Generator, Current Data files in directory:"+ " " + 10 * "=")
    file_insert()


# A function to display the main menu for the user to insert the .jason file name
def menu():
    "CLI Main Menu"
    print(10 * "=" + " " + "Insert one of the following commands:" + " " + 10 * "=")
    print("""
    plt = Plots the tree in the console.
    rsk = Evaluates the risk of the current loaded file. 
    ins = Inserts new Values for the tree leaves.
    prn = provides a .png image of the tree, run rsk command first if risk values required. 
    ext = Terminates program. 
    """)


main_menu()
menu()
Inputs().cmdloop()
