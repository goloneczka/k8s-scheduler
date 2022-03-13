import datetime

from kubernetes import client, config, watch

if __name__ == '__main__':

    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    minute_after_timestamp = datetime.datetime.now() + datetime.timedelta(minutes=1)
    w = watch.Watch()
    for event in w.stream(v1.list_pod_for_all_namespaces, _request_timeout=120):
        print("Event: %s %s" % (event['type'], event['object'].metadata.name))

    if event['type'] == 'ADDED':
        print("Object: ", event['object'].metadata.managed_fields['f:spec'])

    if datetime.datetime.now() > minute_after_timestamp:
        w.stop()

    print("Ended.")
