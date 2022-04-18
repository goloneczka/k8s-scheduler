import re
from math import sqrt

from rank.ahp import calc_weights
from rank.metrics import euclidean_distance, minkowski_distance


def _get_value_from_string(string):
    return int(re.split('(\d+)', string)[1])


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TOPSIS(metaclass=SingletonMeta):

    #   attrs: node.name, cpu_usage, memory_usage, disk_limit_usage, pods_usage, node.network_delay

    def __init__(self):
        self._w_distance = None
        self._b_distance = None
        self._T_topsis_matrix = None
        self._topsis_matrix = None
        self._weights = None

    def init(self, nodes):
        self._topsis_matrix = self._generate_matrix(nodes)
        self._normalize_columns()
        self._weights = calc_weights(self._topsis_matrix[0][1:])
        self._calc_weighted_matrix()
        self._T_topsis_matrix = [[self._topsis_matrix[j][i] for j in range(len(self._topsis_matrix))] for i in
                                 range(len(self._topsis_matrix[0]))]
        self._b_distance, self._w_distance = self._get_optima_distance()
        self._calc_distance_from_optima()

    def get_best_row_name(self):
        if len(self._topsis_matrix):
            topsis_scores = self._T_topsis_matrix[-1]
            index_of_max_score = topsis_scores.index(max(topsis_scores))
            return self._topsis_matrix[index_of_max_score][0]  # attr 0 is name
        return None

    def _generate_matrix(self, nodes):
        matrix = []
        for node in nodes:
            cpu_usage = _get_value_from_string(node.cpu_usage) / 1000000000 / int(node.cpu_allocatable) * 100
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
                row[indx + 1] /= powed_sums[indx]

    def _calc_weighted_matrix(self):
        for row in self._topsis_matrix:
            for (indx, _) in enumerate(row[1:]):
                row[indx + 1] *= self._weights[indx]

    def _get_optima_distance(self):
        b_distance, w_distance = [], []
        for row in self._T_topsis_matrix[1:]:
            b_distance.append(min(row))
            w_distance.append(max(row))

        return b_distance, w_distance

    def _calc_distance_from_optima(self, metric='euclides'):
        if metric == 'euclides':
            for row in self._topsis_matrix:
                row.append(euclidean_distance(row, self._b_distance, self._w_distance))
        elif metric == 'minkowski':
            for row in self._topsis_matrix:
                row.append(minkowski_distance(row, self._b_distance, self._w_distance, 4, self._weights))

    def clear_topsis_cache(self):
        self._w_distance = None
        self._b_distance = None
        self._T_topsis_matrix = None
        self._topsis_matrix = None
        self._weights = None

    def is_initialed(self):
        return self._topsis_matrix is not None
