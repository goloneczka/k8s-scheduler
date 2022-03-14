import logging

from kubernetes.client import V1ObjectReference, V1ObjectMeta, V1Binding


def schedule_pod(v1_client, name, node, namespace="default"):
    target = V1ObjectReference()
    target.kind = "Node"
    target.apiVersion = "v1"
    target.name = node
    meta = V1ObjectMeta()
    meta.name = name
    body = V1Binding(api_version=None, kind=None, metadata=meta, target=target)
    logging.info("Binding Pod: %s  to  Node: %s", name, node)
    return v1_client.create_namespaced_pod_binding(name, namespace, body)