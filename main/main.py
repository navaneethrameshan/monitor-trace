
from common.schedule import Schedule
from store import store
from common import controller
import config

def start_monitoring():
    sched = Schedule(config.TIMEPERIOD)
    sched.schedule(store.monitorStore)

def main():
    controller.update_node_list()
    start_monitoring()