#   attrs: cpu_usage, memory_usage, disk_limit_usage, pods_usage, node.network_delay

from rank import SingletonMeta

_criteria_matrix = [[1.0, 1.0, 5.0, 3.0, 3.0],
                    [1.0, 1.0, 5.0, 3.0, 3.0],
                    [0.2, 0.2, 1.0, 0.33, 0.33],
                    [0.33, 0.33, 3.0, 1.0, 1.0],
                    [0.33, 0.33, 3.0, 1.0, 1.0]]
_count_criteria_columns = 5


class Ahp(metaclass=SingletonMeta):

    def __init__(self):
        self.weights = self._calc_weights()

    def _calc_weights(self):

        col_sum = [.0] * _count_criteria_columns
        for row in _criteria_matrix:
            for (indx, val) in row:
                col_sum[indx] += val

        eigen_vector = []
        for row in _criteria_matrix:
            t_sum = .0
            for (indx, _) in _criteria_matrix:
                row[indx] /= col_sum[indx]
                t_sum += row[indx]
            eigen_vector.append(t_sum)

        return eigen_vector
