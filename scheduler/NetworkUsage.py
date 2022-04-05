import os
import time


def distance(val, v_max, v_min):
    return (val - v_min) / (v_max - v_min)


def calc_network(nodes_ip):
    results = test_network(nodes_ip)
    v_max = max(results)
    v_min = min(results)
    return [distance(val, v_max, v_min) for val in results]


def test_network(nodes_ip):
    responses = []
    for ip in nodes_ip:
        s_time = time.time()
        os.system("ping -c1 -w3" + ip)
        os.system("ping -c1 -w3" + ip)
        responses.append(time.time() - s_time)
    return responses
