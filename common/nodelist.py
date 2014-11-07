import shelve
import constants
import ast

def write_node_list(nodes):

    s = shelve.open('node_list_shelf.db', writeback = True)
    try:
        s['node_list']= nodes
    finally:
        s.close()

    #cache this list::
    constants.nodes = get_node_list()

def write_file_node_list(nodes):

    s = open('rd_list.txt','w')
    try:
        s.write(str(nodes))
    finally:
        s.close()

    #cache this list::
    constants.nodes = get_file_node_list()

def get_file_node_list():

    nodes=[]
    s = open('rd_list.txt', 'r')
    try:
        val=s.readline()
        nodes = ast.literal_eval(val)
    finally:
        s.close()

    #cache this list::
    constants.nodes = nodes

    return nodes


def get_node_list():

    nodes=[]
    s = shelve.open('node_list_shelf.db', writeback = True)
    try:
        if('node_list' in s):
            nodes = s['node_list']

    finally:
        s.close()

    return nodes