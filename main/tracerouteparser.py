import cStringIO
import re
from common import getip, getname, nodelist, constants
import traceroute
import ping


class Probe(object):
    """
    Abstraction of an individual probe in a traceroute.
    """
    def __init__(self):
        self.ipaddr = None
        self.name = None
        self.rtt = None # RTT in ms
        self.anno = None # Annotation, such as !H, !N, !X, etc
        self.group= None #RD from where the request originated

    def clone(self):
        """
        Return a copy of this probe, conveying the same endpoint.
        """
        copy = Probe()
        copy.ipaddr = self.ipaddr
        copy.name = self.name
        return copy

    def __str__(self):
        res = []
        if self.ipaddr:
            res.append("IP Address: " + str(self.ipaddr))
            res.append("Name: " + str(self.name))
            res.append("rtt: "+ str(self.rtt))
            res.append("group: " + str(self.group))
        return ' '.join(res)

    def json(self):
        res ={}
        if self.ipaddr:
            res.update({"IP Address" : str(self.ipaddr)})
            res.update({"Name" : str(self.name)})
            res.update({"rtt" : str(self.rtt)})
            res.update({"group" : str(self.group)})
        return res

class Hop(object):
    """
    A traceroute hop consists of a number of probes.
    """
    def __init__(self):
        self.idx = None # Hop count, starting at 1
        self.probes = [] # Series of Probe instances

    def add_probe(self, probe):
        self.probes.append(probe)

    def __str__(self):
        res = []
        last_probe = None
        for probe in self.probes:
            if probe.name is None:
                res.append('*')
                continue
            anno = '' if probe.anno is None else ' ' + probe.anno
            if last_probe is None or last_probe.name != probe.name:
                res.append('%s (%s) %1.3f ms%s' % (probe.name, probe.ipaddr,
                                                   probe.rtt, anno))
            else:
                res.append('%1.3f ms%s' % (probe.rtt, anno))
            last_probe = probe
        return '  '.join(res)

class TracerouteParser(object):
    """
    A parser for traceroute text. A traceroute consists of a sequence of
    hops, each of which has at least one probe. Each probe records IP,
    hostname, timing information and the RD from where the request originated.
    """
    HEADER_RE = re.compile(r'traceroute to (\S+) \((\d+\.\d+\.\d+\.\d+)\)')

    def __init__(self):
        self.dest_ip = None
        self.dest_name = None
        self.hops = []

    def __str__(self):
        res = ['traceroute to %s (%s)' % (self.dest_name, self.dest_ip) ]
        ctr = 1
        for hop in self.hops:
            res.append('%2d  %s' % (ctr, str(hop)))
            ctr += 1
        return '\n'.join(res)


    def get_probe(self):
        probe_result = []
        for hop in self.hops:
            for probe in hop.probes:
                if probe.ipaddr:
                    #print probe.ipaddr
                    probe_result.append(probe)
        return probe_result

    def get_probe_json(self):
        probe_result = []

        #add itself as the first hop and continue
        myself = Probe()
        myself.ipaddr = getip.get_ip6('confine')
        myself.group = myself.ipaddr
        myself.name = getname.get_name_from_API()
        probe_result.append(myself.json())

        for hop in self.hops:
            for probe in hop.probes:
                if probe.ipaddr:
                    #print probe.ipaddr
                    probe_result.append(probe.json())
        return probe_result

    def parse_data(self, data):
        self.parse_hdl(cStringIO.StringIO(data))

    def parse_hdl(self, hdl):
        self.dest_ip = None
        self.dest_name = None
        self.hops = []

        for line in hdl:
            line = line.strip()
            if line == '':
                continue
            if line.lower().startswith('traceroute'):
                mob = self.HEADER_RE.match(line)
                if mob:
                    self.dest_ip = mob.group(2)
                    self.dest_name = mob.group(1)
            else:
                hop = self._parse_hop(line)
                self.hops.append(hop)

    def _parse_hop(self, line):
        parts = line.split()
        parts.pop(0) # Drop hop number, implicit in resulting sequence
        hop = Hop()
        probe = None

        while len(parts) > 0:
            probe = self._parse_probe(parts, probe)
            if probe:
                hop.add_probe(probe)

        return hop

    def _parse_probe(self, parts, last_probe=None):
        """Internal helper, parses the next probe's results from a line."""
        try:
            probe = Probe() if last_probe is None else last_probe.clone()

            tok1 = parts.pop(0)
            if tok1 == '*':
                return probe

            tok2 = parts.pop(0)
            if tok2 == 'ms':
                probe.rtt = float(tok1)
                if len(parts) > 0 and parts[0].startswith('!'):
                    probe.anno = parts.pop(0)
            else:
                probe.name = tok1
                probe.ipaddr = tok2[1:][:-1]
                probe.rtt = float(parts.pop(0))
                parts.pop(0) # Drop "ms"
                if len(parts) > 0 and parts[0].startswith('!'):
                    probe.anno = parts.pop(0)

            #Add group information for probe
            probe.group = getip.get_ip6('confine')

            return probe

        except (IndexError, ValueError):
            return None


def test():
    tr_data_1 = """
traceroute to edgecastcdn.net (72.21.81.13), 30 hops max, 38 byte packets
 1  *  *
 2  *  *
 3  *  *
 4  100 (100)  3574.616 ms
 5  200 (200)  465.821 ms
 6  C (C)  170.197 ms

"""

    tr_data_2 = """
traceroute to edgecastcdn.net (72.21.81.13), 30 hops max, 38 byte packets
 1  *  *
 2  *  *
 3  *  *
 4  400 (400)  3574.616 ms
 5  100 (100)  465.821 ms
 6  300 (300)  170.197 ms
 7  C (C)  170.197 ms
"""
    # Create parser instance:
    trp_1 = TracerouteParser()

    # Give it some data:
    trp_1.parse_data(tr_data_1)

    trp_2 = TracerouteParser()

    # Give it some data:
    trp_2.parse_data(tr_data_2)

    probe_list_1 = trp_1.get_probe_json()
    probe_list_2 = trp_2.get_probe()

   # for probe in probe_list_2:
    #    print probe.json()

    print str(probe_list_1)

#    all_path = Paths(probe_list_1)
#    all_path.add_path(probe_list_2)
#
#
#    represent = Analyse()
#    represent.represent(all_path)
#    print str(represent.get_representation())
#
#    Generate(represent.get_representation())
#

def demo():
    trace = traceroute.collectTRACEROUTE("controller.confine-project.eu")
    print str(trace)

    trp = TracerouteParser()

    # Give it some data:
    trp.parse_data(trace['traceroute'])

    probe_list = trp.get_probe_json()

    print str(probe_list)

def get_trace_info():
    trace = traceroute.collectTRACEROUTE("controller.confine-project.eu")

    trp = TracerouteParser()

    # Give it some data:
    trp.parse_data(trace['traceroute'])

    probe_dict = trp.get_probe_json()
    return probe_dict


def get_inter_node_trace():

    probe=[]

    nodelist = constants.nodes

    #First element in the List is always Self!!!
    ipaddr = getip.get_ip6('confine')
    group = ipaddr
    name = getname.get_name_from_API()
    probe.append({'IP Address':ipaddr,'Name':name.encode('utf8'), 'Status': True})

    for nodes in nodelist:
        ping_status = ping.ping6(nodes['IP Address'])
        probe.append({'IP Address':nodes['IP Address'],'Name':nodes['Name'].encode('utf8'), 'Status': ping_status})

    return probe


if __name__ == '__main__':
    test()
    #demo()
