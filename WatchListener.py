import logging

from kubernetes.client import CoreV1Api, ApiException
from kubernetes.watch import watch

from NodeHelper import _get_schedulable_node
from Scheduler import schedule_pod

SCHEDULE_STRATEGY = "schedulingStrategy=meetup"

def watch_pod_events():
    V1_CLIENT = CoreV1Api()
    while True:
        try:
            logging.info("Checking for pod events....")
            try:
                watcher = watch.Watch()
                for event in watcher.stream(V1_CLIENT.list_pod_for_all_namespaces, label_selector=SCHEDULE_STRATEGY,
                                            timeout_seconds=20):
                    logging.info(
                        f"Event: {event['type']} {event['object'].kind}, {event['object'].metadata.namespace}, {event['object'].metadata.name}, {event['object'].status.phase}")
                    if event["object"].status.phase == "Pending":
                        try:
                            logging.info(f'{event["object"].metadata.name} needs scheduling...')
                            pod_namespace = event["object"].metadata.namespace
                            pod_name = event["object"].metadata.name
                            service_name = event["object"].metadata.labels["serviceName"]
                            logging.info("Processing for Pod: %s/%s", pod_namespace, pod_name)
                            node_name = _get_schedulable_node(V1_CLIENT)
                            if node_name:
                                logging.info("Namespace %s, PodName %s , Node Name: %s  Service Name: %s",
                                             pod_namespace, pod_name, node_name, service_name)
                                res = schedule_pod(V1_CLIENT, pod_name, node_name, pod_namespace)
                                logging.info("Response %s ", res)
                            else:
                                logging.error(f"Found no valid node to schedule {pod_name} in {pod_namespace}")
                        except ApiException as e:
                            logging.error(e.body)
                        except ValueError as e:
                            logging.error("Value Error %s", e)
                        except:
                            logging.exception("Ignoring Exception")
                logging.info("Resetting k8s watcher...")
            except:
                logging.exception("Ignoring Exception")
            finally:
                del watcher
        except:
            logging.exception("Ignoring Exception & listening for pod events")
