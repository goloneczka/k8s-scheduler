import re
from math import sqrt, exp

from rank.SingletonMeta import SingletonMeta
from rank.ahp import Ahp
from rank.metrics import euclidean_distance, minkowski_distance


def _get_value_from_string(string):
    return int(re.split('(\d+)', string)[1])

class TOPSIS(metaclass=SingletonMeta):

    #   attrs: node.name, cpu_usage, memory_usage, disk_limit_usage, pods_usage, node.network_delay

    def _init(self):
        self._w_distance = None
        self._b_distance = None
        self._T_topsis_matrix = None
        self._topsis_matrix = None
        self._cached_nodes = None
        self._number_of_pods = None
        self._copied_initialized_score = None

    def __init__(self):
        self._init()
        self._ahp = Ahp()

    def init(self, nodes):
        self._topsis_matrix = self._generate_matrix(nodes)
        print('|| ', self._topsis_matrix, ' || ')

        self._number_of_pods = [node.pods_len for node in nodes]
        self._normalize_columns()
        print('|| ', self._topsis_matrix, ' || ')

        self._cached_nodes = [0] * len(self._topsis_matrix)

        self._calc_weighted_matrix()
        print('|| ', self._topsis_matrix, ' || ')

        self._T_topsis_matrix = [[self._topsis_matrix[j][i] for j in range(len(self._topsis_matrix))] for i in
                                 range(len(self._topsis_matrix[0]))]

        self._b_distance, self._w_distance = self._get_optima_distance()
        self._copied_initialized_score = self._calc_basic_score()
        print('|| ', self._topsis_matrix, ' || ')

    def get_best_row_name(self):
        topsis_scores = self._T_topsis_matrix[-1]
        index_of_max_score = topsis_scores.index(max(topsis_scores))
        return self._topsis_matrix[index_of_max_score][0]  # attr 0 is name

    def _generate_matrix(self, nodes):
        matrix = []
        for node in nodes:
            cpu_usage = _get_value_from_string(node.cpu_usage) / 1000000000 / _get_value_from_string(node.cpu_allocatable) * 10000
            memory_usage = _get_value_from_string(node.memory_usage) / _get_value_from_string(
                node.memory_allocatable) * 100
            disk_limit_usage = _get_value_from_string(node.eph_storage_limit) / _get_value_from_string(
                node.eph_storage_allocatable) * 100
            pods_usage = node.pods_len / int(node.pods_allocatable) * 100
            matrix.append([node.name, cpu_usage, memory_usage, disk_limit_usage, pods_usage, node.network_delay])
        return matrix

    def _normalize_columns(self):
        powed_sums = [.0] * len(self._topsis_matrix[0][1:])
        for row in self._topsis_matrix:
            for (indx, val) in enumerate(row[1:]):
                powed_sums[indx] += val * val

        powed_sums = [sqrt(i) for i in powed_sums]

        for row in self._topsis_matrix:
            for (indx, _) in enumerate(row[1:]):
                row[indx + 1] /= powed_sums[indx] if powed_sums[indx] != 0 else 1

    def _calc_weighted_matrix(self):
        for row in self._topsis_matrix:
            for (indx, _) in enumerate(row[1:]):
                row[indx + 1] *= self._ahp.weights[indx]

    def _get_optima_distance(self):
        b_distance, w_distance = [], []
        for row in self._T_topsis_matrix[1:]:
            b_distance.append(min(row))
            w_distance.append(max(row))

        return b_distance, w_distance

    def _calc_basic_score(self, metric='euclides'):
        copied_initialized_score = []
        if metric == 'euclides':
            for row in self._topsis_matrix:
                distance = euclidean_distance(row, self._b_distance, self._w_distance)
                row.append(distance)
                copied_initialized_score.append(distance)
        elif metric == 'minkowski':
            for row in self._topsis_matrix:
                distance = minkowski_distance(row, self._b_distance, self._w_distance, 4, self._ahp.weights)
                row.append(distance)
                copied_initialized_score.append(distance)
        self._T_topsis_matrix.append(copied_initialized_score)
        return copied_initialized_score

    def clear_topsis_cache(self):
        self._init()

    def update_cache(self, best_row_name):
        topsis_names = self._T_topsis_matrix[0]
        for (indx, name) in enumerate(topsis_names):
            if name == best_row_name:
                self._cached_nodes[indx] += 1
                number_of_cached_nodes = self._cached_nodes[indx]
                self._T_topsis_matrix[-1][indx] = self._topsis_matrix[indx][-1] = self._copied_initialized_score[indx] * (
                        1 - number_of_cached_nodes / (number_of_cached_nodes + self._number_of_pods[indx]) * exp( -1 / number_of_cached_nodes))  # attr 4 is number of pods, attr -1 is topsis score
                break

    def is_initialed(self):
        return self._topsis_matrix is not None
