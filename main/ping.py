import subprocess
import sys

def ping6(ip):
    ping = subprocess.Popen(["ping6","-c","2", ip],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ping.wait()
    if ping.returncode != 0:
        #print ping.returncode, "ERROR: failed to ping host. Please check."
        return False
    else:
        #print "OK"
        return True