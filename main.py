import datetime

from kubernetes import client, config, watch

from WatchListener import watch_pod_events

if __name__ == '__main__':
    config.load_kube_config()
    watch_pod_events()