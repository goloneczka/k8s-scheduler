#   attrs: cpu_usage, memory_usage, disk_limit_usage, pods_usage, node.unused_costs

from rank.SingletonMeta import SingletonMeta

# _criteria_matrix = [[1,     1,      5,      3,      1/3],
#                     [1,     1,      5,      3,      1/3],
#                     [1/5,   1/5,    1,      1/3,    1/7],
#                     [1/3,   1/3,    2,      1,      1/5],
#                     [3,     3,      7,      5,        1]]

_criteria_matrix = [[1.0, 1.0, 5.0, 3.0, 0.33],
                    [1.0, 1.0, 5.0, 3.0, 0.33],
                    [0.2, 0.2, 1.0, 0.33, 0.14],
                    [0.33, 0.33, 2.0, 1.0, 0.2],
                    [3.0, 3.0, 7.0, 5.0, 1.0]]


_count_criteria_columns = 5


class Ahp(metaclass=SingletonMeta):

    def __init__(self):
        self.weights = self._calc_weights()

    def _calc_weights(self):

        col_sum = [.0] * _count_criteria_columns
        for row in _criteria_matrix:
            for (indx, val) in enumerate(row):
                col_sum[indx] += val

        eigen_vector = []
        for row in _criteria_matrix:
            t_sum = .0
            for indx in range(len(_criteria_matrix)):
                row[indx] /= col_sum[indx]
                t_sum += row[indx]
            eigen_vector.append(t_sum)
        return eigen_vector
