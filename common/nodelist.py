import shelve
import constants

def write_node_list(nodes):

    s = shelve.open('node_list_shelf.db', writeback = True)
    try:
        s['node_list']= nodes
    finally:
        s.close()

    #cache this list::
    constants.nodes = get_node_list()

def get_node_list():

    nodes=[]
    s = shelve.open('node_list_shelf.db', writeback = True)
    try:
        if('node_list' in s):
            nodes = s['node_list']

    finally:
        s.close()

    return nodes