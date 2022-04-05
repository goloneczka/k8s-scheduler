import logging
import random

from entity.Node import Node

from kubernetes.client import ApiException

from scheduler.NetworkUsage import calc_network

_NOSCHEDULE_TAINT = "NoSchedule"

def _get_ready_nodes(v1_client, filtered=True):
    ready_nodes = []
    try:
        for n in v1_client.list_node().items:
            if not n.spec.unschedulable:
                no_schedule_taint = False
                if n.spec.taints:
                    # Check if there are any taints on the node that might indicate that pods should not be scheduled.
                    for taint in n.spec.taints:
                        if _NOSCHEDULE_TAINT == taint.to_dict().get("effect", None):
                            no_schedule_taint = True
                            break
                if not no_schedule_taint:
                    for status in n.status.conditions:
                        if status.status == "True" and status.type == "Ready" and n.metadata.name:
                            ready_nodes.append(n)
                else:
                    logging.error("NoSchedule taint effect on node %s", n.metadata.name)
            else:
                logging.error("Scheduling disabled on %s ", n.metadata.name)
        logging.info("Nodes : %s, Filtered: %s", ready_nodes, filtered)
    except ApiException as e:
        logging.error(e.body)
        ready_nodes = []
    return ready_nodes


def calc_nodes(node_list, v1_api):
    k8s_nodes = [Node(v1_api.get_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes", n.metadata.name)) for n in node_list]

    calc_network([n.status.addresses[0].address] for n in node_list)
    return 0


def get_schedulable_node(v1_client, v1_api):
    node_list = _get_ready_nodes(v1_client)
    if not node_list:
        return None
    best_node = calc_nodes(node_list, v1_api)
    available_nodes = list(set(node_list))
    return random.choice(available_nodes)