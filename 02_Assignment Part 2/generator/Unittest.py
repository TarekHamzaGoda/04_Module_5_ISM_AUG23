import unittest
import attacktrees
from mock import patch  # Library for patching user inputs
from anytree import Node

# Creating test nod for test tree
root = Node("A", parent=None, value=0.0)
A1 = Node(name='A1', parent=root, value=1.0)
B1 = Node(name='B1', parent=root, value=2.0)
B11 = Node(name='B11', parent=B1, value=3.0)
B12 = Node(name='B12', parent=B1, value=6.0)
C1 = Node(name='C1', parent=root, value=8.0)

# Creating Test Dict
test_data = {"root": root, "A1": A1, "B1": B1, "B11": B11, "B12": B12, "C1": C1}
test_root = root


class TestCases(unittest.TestCase):
    """A test for the file_insert function, tries to insert an incorrect file name """

    @patch('builtins.input', return_value="data_sets/pp_current.json")
    def Inserted_Files(self, input):
        """checks of the test returns an error when inputted wrong name."""
        test_result = attacktrees.file_insert()
        self.assertEqual(test_result, "File not in directory!")

    @patch('builtins.input', return_value="test_tree")
    def Plotting_trees(self, input):
        """a test for plotting the tree from the test tree"""
        test_result = attacktrees.plot_tree(test_data, test_root)
        self.assertEqual(test_result, "File created")

    @patch('attacktrees.nodes', test_data)
    @patch('attacktrees.root_node', test_root)
    def Risk_Calc(self):
        """test if the return value i correct """
        test_result = attacktrees.rsk_clc()
        self.assertEqual(test_result, 3.08)
