from math import sqrt


class TOPSIS:

    def __init__(self, nodes):
        self.topsis_matrix = self._generate_matrix(nodes)
        self._normalize_rest_columns()
        self._calc_weighted_matrix([.3, .3, .1, .1, .2])
        self.b_distance, self.w_distance = self._get_optima_distance()
        self._calc_distance_from_optima()

    def get_best_row_name(self):
        if len(self.topsis_matrix):
            T_topsis_matrix = self.topsis_matrix # TODO !!! o magic with transportive matrix
            index_of_max_score = list.index(max(T_topsis_matrix[-1]))
            return self.topsis_matrix[index_of_max_score][0] # attr 0 is name
        return None



    def _generate_matrix(self, nodes):
        matrix = []
        for node in nodes:
            cpu_usage = node.cpu_usage / node.cpu_allocatable
            memory_usage = node.memory_usage / node.memory_allocatable
            disk_limit_usage = node.eph_storage_limit / node.eph_storage_allocatable
            pods_usage = node.pods_len / node.pods_allocatable
            matrix.append([node.name, cpu_usage, memory_usage, disk_limit_usage, pods_usage, node.network_delay])
        return matrix

    def _normalize_rest_columns(self):
        powed_sum_of_network_delay = .0
        for row in self.topsis_matrix:
            powed_sum_of_network_delay += row[5] * row[5] # attr 5 is network deplay
            # TODO -> add other columns if avaible in nodes

        powed_sum_of_network_delay = sqrt(powed_sum_of_network_delay)
        for row in self.topsis_matrix:
            row[5] /= powed_sum_of_network_delay
            # TODO -> add other columns if avaible in nodes

    def _calc_weighted_matrix(self, weights):
        for row in self.topsis_matrix:
            for (indx, nested_row) in enumerate(row[1:]):
                nested_row *= weights[indx]


    def _get_optima_distance(self):
        b_distance, w_distance = [], []
        T_topsis_matrix = self.topsis_matrix # TODO !!! o magic with transportive matrix
        for row in T_topsis_matrix[1:]:
            b_distance.append(max(row))
            w_distance.append(min(row))

        b_distance[5 - 1], w_distance[5 - 1] = w_distance[5 - 1], b_distance[5 - 1] # attr 5 is delay network, which need be the lowest

        return b_distance, w_distance

    def _calc_distance_from_optima(self):
        for row in self.topsis_matrix:
            row_b_distance, row_w_distance = .0, .0
            for (indx, nested_row) in enumerate(row[1:]):
                row_b_distance += (self.b_distance[indx] - nested_row) * (self.b_distance[indx] - nested_row)
                row_w_distance += (self.w_distance[indx] - nested_row) * (self.w_distance[indx] - nested_row)
            row.append(sqrt(row_w_distance) / (sqrt(row_w_distance) + sqrt(row_b_distance)))






