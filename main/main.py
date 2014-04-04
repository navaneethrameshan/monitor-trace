
from common.schedule import Schedule
from store import store
import config

def start_monitoring():
    sched = Schedule(config.TIMEPERIOD)
    sched.schedule(store.monitorStore)

def main():
    start_monitoring()