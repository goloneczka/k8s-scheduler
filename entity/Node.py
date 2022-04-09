import re


def _get_ki_value(string):
    val_and_mesaurment = re.split('(\d+)',string)
    if val_and_mesaurment[2] == 'Ki':
        return float(val_and_mesaurment[1])
    elif val_and_mesaurment[2] == 'Mi':
        return float(val_and_mesaurment[1]) * 1000
    else:
        return float(val_and_mesaurment[1])


class Node:

    def __init__(self, custom_obj):
        self.huge_pages_usage = None
        self.eph_storage_usage = None
        self.name = custom_obj['metadata']['name']
        self.cpu_usage = custom_obj['usage']['cpu']
        self.memory_usage = custom_obj['usage']['memory']

    def calculate_usages_from_pods(self, pods):
        eph_storage = .0
        huge_pages = .0
        for pod in pods.items:
            if len(pod.spec.containers):
                for pod_container in pod.spec.containers:
                    if pod_container.resources.limits and 'ephemeral-storage' in pod_container.resources.limits:
                        eph_storage += _get_ki_value(pod_container.resources.limits['ephemeral-storage'])
                    if pod_container.resources.limits and 'hugepages-2Mi' in pod_container.resources.limits:
                        huge_pages += pod_container.resources.limits['hugepages-2Mi']

        self.eph_storage_usage = str(eph_storage) + 'Ki'
        self.huge_pages_usage = str(huge_pages) + 'Ki'