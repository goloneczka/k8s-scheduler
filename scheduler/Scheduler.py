
from kubernetes.client import V1ObjectReference, V1ObjectMeta, V1Binding


def schedule_pod(v1_client, name, node, namespace="default"):
    target = V1ObjectReference(kind='Node', api_version='v1', name=node)
    meta = V1ObjectMeta(name=name)
    body = V1Binding(metadata=meta, target=target)
    return v1_client.create_namespaced_binding(namespace, body, _preload_content=False)