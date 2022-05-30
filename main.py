from logging import basicConfig, getLogger, INFO

from kubernetes import config

from Helper import list_nodeA, list_node, node_usage
from scheduler.WatchListener import watch_pod_events

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger("meetup-scheduler")

if __name__ == '__main__':
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    watch_pod_events()
