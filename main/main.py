
from common.schedule import Schedule
from store import store
from common import controller, nodelist
import config

def start_monitoring():
    sched = Schedule(config.TIMEPERIOD)
    sched.schedule(store.monitorStore)

def main():
    #controller.update_node_list() #Enable to read all RDs from controller
    nodelist.get_node_list() # If node_list_shelf.db exists use this to avoid reading from controller
    start_monitoring()