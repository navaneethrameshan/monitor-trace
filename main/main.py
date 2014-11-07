
from common.schedule import Schedule
from store import store
from common import controller, nodelist
import config

def start_monitoring():
    sched = Schedule(config.TIMEPERIOD)
    sched.schedule(store.monitorStore)

def main():
    #controller.update_node_list() #Enable to read all RDs from controller
    nodelist.get_file_node_list() # If RD list(file) exists, use this to avoid using controller API
    start_monitoring()