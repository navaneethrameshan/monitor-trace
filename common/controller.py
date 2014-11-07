import json
import urllib2
from common import nodelist
import config

def update_node_list():

    nodes =[]

    url = 'http://'+ config.CONTROLLER_IP + '/api/nodes/'
    request = urllib2.Request(url)
    response= None
    try:
        response = urllib2.urlopen(request)
    except:
        response = None

    if(response):

        nodes_uri = json.loads(response.read())
        for dict_node_uri in nodes_uri:
            node_uri= dict_node_uri['uri']
            node_ip6= get_node_ip_from_node_uri(node_uri)
            name = dict_node_uri['name']
            print name
            if (node_ip6):
                nodes.append({'Name':name, 'IP Address':node_ip6})

        print nodes
        nodelist.write_file_node_list(nodes)

    else:
        print "[ERROR] No response from Controller"




def get_node_ip_from_node_uri(node_uri):

    request = urllib2.Request(node_uri)
    response= None
    try:
        response = urllib2.urlopen(request)
    except:
        response = None

    if(response):
        node_info = json.loads(response.read())
        node_mgmt_net = node_info['mgmt_net']
        node_ip6 = node_ip6='['+node_mgmt_net['addr'] +']'
        return node_ip6

    return None
