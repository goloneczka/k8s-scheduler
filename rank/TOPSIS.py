import re
from math import sqrt


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

    def __init__(self):
        self.w_distance = None
        self.b_distance = None
        self.T_topsis_matrix = None
        self.topsis_matrix = None

    def init(self, nodes):
        self.topsis_matrix = self._generate_matrix(nodes)
        self._normalize_rest_columns()
        self._calc_weighted_matrix([.3, .3, .1, .1, .2])
        self.T_topsis_matrix = [[self.topsis_matrix[j][i] for j in range(len(self.topsis_matrix))] for i in
                                range(len(self.topsis_matrix[0]))]
        self.b_distance, self.w_distance = self._get_optima_distance()
        self._calc_distance_from_optima()

    def get_best_row_name(self):
        if len(self.topsis_matrix):
            topsis_scores = self.T_topsis_matrix[-1]
            index_of_max_score = topsis_scores.index(max(topsis_scores))
            return self.topsis_matrix[index_of_max_score][0]  # attr 0 is name
        return None

    def _generate_matrix(self, nodes):
        matrix = []
        for node in nodes:
            cpu_usage = _get_value_from_string(node.cpu_usage) / 1000000000 / int(node.cpu_allocatable)
            memory_usage = _get_value_from_string(node.memory_usage) / _get_value_from_string(node.memory_allocatable)
            disk_limit_usage = _get_value_from_string(node.eph_storage_limit) / _get_value_from_string(
                node.eph_storage_allocatable)
            pods_usage = node.pods_len / int(node.pods_allocatable)
            matrix.append([node.name, cpu_usage, memory_usage, disk_limit_usage, pods_usage, node.network_delay])
        return matrix

    def _normalize_rest_columns(self):
        powed_sum_of_network_delay = .0
        for row in self.topsis_matrix:
            powed_sum_of_network_delay += row[5] * row[5]  # attr 5 is network deplay
            # TODO -> add other columns if avaible in nodes

        powed_sum_of_network_delay = sqrt(powed_sum_of_network_delay)
        for row in self.topsis_matrix:
            row[5] /= powed_sum_of_network_delay
            # TODO -> add other columns if avaible in nodes

    def _calc_weighted_matrix(self, weights):
        for row in self.topsis_matrix:
            for (indx, _) in enumerate(row[1:]):
                row[indx + 1] *= weights[indx]

    def _get_optima_distance(self):
        b_distance, w_distance = [], []
        for row in self.T_topsis_matrix[1:]:
            b_distance.append(max(row))
            w_distance.append(min(row))

        b_distance[5 - 1], w_distance[5 - 1] = w_distance[5 - 1], b_distance[
            5 - 1]  # attr 5 is delay network, which need be the lowest

        return b_distance, w_distance

    def _calc_distance_from_optima(self, metric='euclides'):
        if metric == 'euclides':
            for row in self.topsis_matrix:
                row_b_distance, row_w_distance = .0, .0
                for (indx, nested_row) in enumerate(row[1:]):
                    row_b_distance += (self.b_distance[indx] - nested_row) * (self.b_distance[indx] - nested_row)
                    row_w_distance += (self.w_distance[indx] - nested_row) * (self.w_distance[indx] - nested_row)
                if row_b_distance == 0.0:
                    row.append(1)
                else:
                    row.append(sqrt(row_w_distance) / (sqrt(row_w_distance) + sqrt(row_b_distance)))

    def clear_topsis_cache(self):
        self.w_distance = None
        self.b_distance = None
        self.T_topsis_matrix = None
        self.topsis_matrix = None


    def is_initialed(self):
        return self.topsis_matrix is not None
