import logging
import os
import subprocess
import time

from kubernetes import client, config


def describe_pods():
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        
def describe_pod(name = None):
    v1 = client.CoreV1Api()
    if name is None:
        describe_pods()
        return 
    print("Listing pod ", name)
    ret = v1.list_pod_for_all_namespaces(watch=False)
    specyfied_pod = [item for item in ret.items if item.metadata.name == name]



def list_node():
    v1 = client.CoreV1Api()
    for n in v1.list_node().items:
        ip = n.status.addresses[1].address
        print(n.metadata.name)
        os.system("ping -c8 -w8 " + ip)

    logging.info("done ! \n \n")

def list_nodeA():
    v1 = client.CoreV1Api()
    for n in v1.list_node().items:
        print(n.metadata.name)
        ip = n.status.addresses[1].address
        proc = subprocess.Popen(
            ['ping', '-q', '-c5', '-s16384', ip])
        proc.wait()


def node_usage():
    api = client.CustomObjectsApi()
    k8s_nodes = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
    for stats in k8s_nodes['items']:
        print("Node Name: %s\tCPU: %s\tMemory: %s" % (stats['metadata']['name'], stats['usage']['cpu'], stats['usage']['memory']))

    k8s_node = api.get_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes", 'kind-control-plane')
    k = 1

def node_describe():
    api = client.CoreV1Api()
    nod = api.read_node('kind-control-plane')
    a = 2