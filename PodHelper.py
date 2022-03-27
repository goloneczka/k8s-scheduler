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
    print(specyfied_pod[0].spec.containers[0].resources)
    print(specyfied_pod[0].spec.ephemeral_containers)