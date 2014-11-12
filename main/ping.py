import subprocess
import sys

def ping6(ip):
    ping = subprocess.Popen(["ping6","-q","-c","5", ip],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ping.wait()
    if ping.returncode != 0:
        #print ping.returncode, "ERROR: failed to ping host. Please check."
        return {'Status':True,'Loss':None,'Min':None,'Avg':None,'Max':None}
    else:
        #print "OK"
        output = ping.stdout.read().split("\n")
        packet_loss = output[3].split(',')[2].split('%')[0].strip(' ')
        (min,avg,max) = output[4].split('=')[1].split('/')
        min= min.strip(' ')
        avg= avg.strip(' ')
        max = max.strip("ms")
        #print "Packetloss: ", packet_loss
        #print "Min, Avg, Max: ", min,avg,max
        return {'Status':True,'Loss':packet_loss,'Min':min,'Avg':avg,'Max':max}