import logging

from kubernetes.client import CoreV1Api
from kubernetes.watch import watch

from . import NodeHelper
from . import Scheduler
from .Pod import Pod

SCHEDULE_STRATEGY = "schedulingStrategy=meetup"

def watch_pod_events():
    V1_CLIENT = CoreV1Api()
    while True:
        try:
            logging.info("Checking for pod events....")
            try:
                watcher = watch.Watch()
                pod_que = []
                for event in watcher.stream(V1_CLIENT.list_pod_for_all_namespaces,
                                            timeout_seconds=20):
                    if event["object"].status.phase == "Pending" and event['object'].spec.node_name is None:
                        try:
                            logging.info(f'{event["object"].metadata.name} needs scheduling...')
                            pod = Pod(event["object"])
                            logging.info("Processing for Pod: %s/%s", pod.namespace, pod.name)
                            pod_que.append(pod)
                            node_name = NodeHelper.get_schedulable_node(V1_CLIENT)
                            if node_name:
                                res = Scheduler.schedule_pod(V1_CLIENT, pod.name, node_name, pod.namespace)
                                logging.info("Response %s ", res)
                            else:
                                logging.error(f"Found no valid node to schedule {pod.name} in {pod.namespace}")
                        except Exception as e:
                            logging.exception("Got problem:", e)
                if len(pod_que):
                    print('in que: ', len(pod_que))
                    pod_que = []
                logging.info("Resetting k8s watcher...")
            except:
                logging.exception("Ignoring Exception")
            finally:
                del watcher
        except:
            logging.exception("Ignoring Exception & listening for pod events")
