import logging
import datetime
import random

from kubernetes.client import CoreV1Api, CustomObjectsApi
from kubernetes.watch import watch

from Helper import list_node
from rank.TOPSIS import TOPSIS
from . import NodeHelper
from . import Scheduler
from entity.Pod import Pod

SCHEDULE_STRATEGY = "schedulingStrategy=meetup"


def watch_pod_events():
    V1_CLIENT, V1_API, topsis_rank = CoreV1Api(), CustomObjectsApi(), TOPSIS()
    logging.info("K8s custom scheduler started work at %s", datetime.datetime.now())
    while True:
        try:
            watcher = watch.Watch()
            for event in watcher.stream(V1_CLIENT.list_pod_for_all_namespaces,
                                        label_selector=SCHEDULE_STRATEGY,
                                        timeout_seconds=20):
                if event["object"].status.phase == "Pending" and event['object'].spec.node_name is None:
                    try:
                        logging.info(f'{event["object"].metadata.name} needs scheduling...')
                        pod = Pod(event["object"])
                        logging.info("Processing for Pod: %s/%s", pod.namespace, pod.name)
                        node_name = NodeHelper.choose_best_node(V1_CLIENT, V1_API)
                        if node_name:
                            res = Scheduler.schedule_pod(V1_CLIENT, pod.name, node_name, pod.namespace)
                            logging.info("Response %s ", res)
                        else:
                            logging.error(f"Found no valid node to schedule {pod.name} in {pod.namespace}")
                    except Exception as e:
                        logging.exception("Got problem:", e)
            topsis_rank.clear_topsis_cache()

        except:
            logging.exception("Ignoring Exception")
        finally:
            del watcher

