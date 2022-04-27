import re
import subprocess
import time


def _get_ki_value(string):
    val_and_mesaurment = re.split('(\d+)',string)
    if val_and_mesaurment[2] == 'Ki':
        return float(val_and_mesaurment[1])
    elif val_and_mesaurment[2] == 'Mi':
        return float(val_and_mesaurment[1]) * 1000
    else:
        return float(val_and_mesaurment[1])


class Node:

    def __init__(self, custom_obj, status):
        self.eph_storage_limit = None
        self.huge_pages_limit = None
        self.network_delay = None
        self.pods_len = None

        self.name = custom_obj['metadata']['name']
        self.cpu_usage = custom_obj['usage']['cpu']
        self.memory_usage = custom_obj['usage']['memory']

        self.cpu_allocatable = status.allocatable['cpu']
        self.memory_allocatable = status.allocatable['memory']
        self.eph_storage_allocatable = status.allocatable['ephemeral-storage']
        self.pods_allocatable = status.allocatable['pods']

        self.ip = status.addresses[0].address



    def calculate_usages_from_pods(self, pods):
        eph_storage = .0
        huge_pages = .0
        pods = [pod for pod in pods.items if 'schedulingStrategy' in pod.metadata.labels]
        for pod in pods:
            if len(pod.spec.containers):
                for pod_container in pod.spec.containers:
                    if pod_container.resources.limits and 'ephemeral-storage' in pod_container.resources.limits:
                        eph_storage += _get_ki_value(pod_container.resources.limits['ephemeral-storage'])
                    if pod_container.resources.limits and 'hugepages-2Mi' in pod_container.resources.limits:
                        huge_pages += pod_container.resources.limits['hugepages-2Mi']

        self.eph_storage_limit = str(eph_storage) + 'Ki'
        self.huge_pages_limit = str(huge_pages) + 'Ki'
        self.pods_len = len(pods)


    def set_network_delay(self):
        s_time = time.time()
        proc = subprocess.Popen(
            ['ping', '-q', '-c', '1', self.ip],
            stdout=subprocess.DEVNULL)
        proc.wait()
        proc = subprocess.Popen(
            ['ping', '-q', '-c', '1', self.ip],
            stdout=subprocess.DEVNULL)
        proc.wait()
        self.network_delay = time.time() - s_time
