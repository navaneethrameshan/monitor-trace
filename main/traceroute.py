from common import command

def collectTRACEROUTE(nodename):
    values = {}
    trace = command.CMD()
    (oval,errval) = trace.run_noexcept("traceroute -q 1 %s" % nodename)
    #oval = oval.replace("\n", " ")
    values['traceroute'] = oval
    #print "Traceroute Status: %s \n" % oval
    return values
