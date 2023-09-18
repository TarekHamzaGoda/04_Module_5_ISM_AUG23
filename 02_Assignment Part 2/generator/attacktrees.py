import os  # for checking files in the directory
from anytree import Node, RenderTree  # module for generating dependency trees
import json  # module for reading .json files
from graphviz import Source  # module for printing the attack tree on screen
from anytree.exporter import DotExporter  # library for converting to .dot file for graphviz to read

# This a line of code is fix for finding graphviz executables file location after installation. change the path to
# location of the installed program
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

# Creating global variables to be accessed by the functions

root_node = Node("default")  # anytree method to identify root node
nodes = {}  # dict for specific nodes
data = {}
files = []  # A list to store file name for user selection


def file_insert():
    """A function for displaying and loading the file in the directory"""

    global data, files  # accessing the global variables

    path = r"data_sets"
    file_path = os.listdir(path)  # method for listing all the file in the project directory
    for file in file_path:
        print(file)
        files.append(file)  # adding the file in a list

    file_name_input = input("Please type a file name from the list above or type ext to terminate the program")

    if file_name_input in files:

        # syntax used to open json file from the imported module
        with open(f'data_sets/{file_name_input}', 'r') as file1:
            data = json.load(file1)
            print("Json File Loaded")  # test if the file is loaded
            gen_tree()  # function for iterating data in the json

    elif file_name_input == "ext":
        exit()

    else:
        print("File not in the directory!")
        file_insert()


def gen_tree():
    """ A function to  interpret .json files """
    global root_node, data

    # The next step is to iterate over the data in the Json file to assign values to the tree nodes.
    data_len = len(data)  # to iterate on the number of data present in the json file.
    main_root = data['root']['name']  # storing the name of the root node
    node_names = list(data.keys())  # converting all the keys in the json to iterable list

    for i in range(data_len):
        leaf = node_names[i]  # retrieve items from json dict
        leaf_name = data[leaf]['name']
        leaf_parent = data[leaf]['parent']
        leaf_value = data[leaf]['value']

        # This step is to replace any "none" values of the parents
        if leaf_parent == "None":
            leaf_parent = None
            print("none")
        elif leaf_parent == main_root:
            leaf_parent = root_node
        else:
            for key in nodes.keys():
                if leaf_parent == key:
                    leaf_parent = nodes[key]
                else:
                    pass

        # This step is to replace any "null" values
        if leaf_value is None:
            leaf_value = 0.0
        else:
            leaf_value = float(leaf_value)

        # Using the Node method from anytree to place the extracted values from json
        leaf = Node(name=leaf_name, parent=leaf_parent, value=leaf_value)

        # re-assigns the leaf with no parent to the root node
        if leaf.parent is None:
            root_node = leaf
            nodes["root"] = root_node
        else:
            nodes[leaf.name] = leaf


def plot_tree():
    """A function using the rendertree method to display the tree on the console"""
    print(RenderTree(root_node))


def rsk_clc():
    """A function that calculates risk value of leaf nods and prints the evaluation based on scorning system.
    This calculation divides the total risk values over the number of nodes"""

    # This step is to assess the leaf nod height from root node, its essential for
    # storing the value of only the child nods
    root_height = root_node.height
    node_length = root_height - 1

    # This step for accessing the node values
    while True:
        while node_length >= 0:
            for node in nodes.values():
                if node.depth == node_length:
                    if node.children:  # First using . children method to check if there are child leaves
                        child_nodes = []
                        child_nodes.extend(node.children)  # adding leaf node names to the list
                        # print(child_nodes)
                        child_nodes_num = len(child_nodes)
                        # print(child_nodes)   # print statements for testing
                        # print(child_nodes_num)
                        total_v = 0
                        # this step of adding the values of the child/leaf nodes and dividing it by the number or child
                        # nods, the node values of the parent will change to the new calculated value
                        for child in child_nodes:
                            total_v += child.value    # adding the total child/leaf node values
                            # print(total_v)
                        node.value = round(total_v / child_nodes_num, 2)   # diving the total on the number of child
                        # leaf nodes and rounding
                        # print(node.value)
            node_length -= 1

        # the root_node value is changed so we will recall the new value for evaluation
        total_tree_value = root_node.value

        # This Step for evaluating the new root_node value
        if 10 >= total_tree_value > 9.5:
            rating = "Very High Risk"
        elif 9.5 >= total_tree_value > 8.0:
            rating = "High Risk"
        elif 7.9 >= total_tree_value > 2.0:
            rating = "Moderate Risk"
        elif 2.0 >= total_tree_value > 0.5:
            rating = "Low Risk"
        elif 0.5 >= total_tree_value >= 0:
            rating = "Very Low Risk"
        else:
            rating = "Invalid values, check leaf nod values "

        print(f"Total Risk value is: {total_tree_value}, Total Threat Rate {rating}.")

        return root_node.value


def insert_v():
    """User inputted values for leaves nodes"""

    # this step to iterate over the leaf node list to show the user the options
    for child_nodes in nodes:
        print(10 * "-")
        print(child_nodes)
        print(10 * "-")

    leaf_node_input = input("Please input leaf node name from above or press 'Enter' For main menu")
    print()

    # This step to evaluate the user's input - Checks if the leaf node and value is correct.
    while True:
        if leaf_node_input == "":
            print("Returning to main menu")
            break

        if leaf_node_input not in nodes.keys():
            print("Leaf node not found, please try again!")
            insert_v()

        else:
            # This process validates the user's value input
            while True:
                try:
                    new_leaf_node_value = input("Input any value from 0 - 10")
                    if 0 <= float(new_leaf_node_value) <= 10:
                        nodes[leaf_node_input].value = float(new_leaf_node_value)  # updating dict key
                        print("New leaf node value updated!")
                        break
                    else:
                        print("Invalid inout value, Please input a number from 0 - 10")

                except ValueError:
                    print("Invalid, please insert a number")

            # This step allows the user input a new value
            new_leaf_node_input = input("Enter another value?(y), Evaluate current(n)")
            if new_leaf_node_input == "y":
                insert_v()
            elif new_leaf_node_input == "n":
                rsk_clc()
            else:
                print("Invalid Input, Type (y/n)")
        return


def print_tree():
    """Prints a .PNG of the tree generated and modified """

    # this step modifies the name of each node to contain the value as well
    for node_name in nodes.values():
        node_name.name = f"{node_name.name}\n{node_name.value}"
        # print(node_name) # for testing purposes

    file_name_input = input("Please input file name")
    # This step allows the user to type the file name
    if file_name_input:
        print(" A PNG file will pop on your screen")
        # Dot exporter saves the root node dict as .nod file for graphviz to read
        DotExporter(root_node).to_dotfile('temp')
        # this variable will store the location of the temporary dot file called "temp"
        dot = Source.from_file('temp')
        dot.render(outfile=f'exportedtrees/{file_name_input}.png', view=True)
    else:
        print("file not saved")
