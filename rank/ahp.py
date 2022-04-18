
#   attrs: cpu_usage, memory_usage, disk_limit_usage, pods_usage, node.network_delay

def calc_weights(st_row_without_name):
    count_columns = len(st_row_without_name)
    if count_columns != 4:
        return [1/count_columns] * count_columns

    criteria_matrix = [ [1.0, 1.0, 5.0, 3.0, 3.0],
                        [1.0, 1.0, 5.0, 3.0, 3.0],
                        [0.2, 0.2, 1.0, 0.33, 0.33],
                        [0.33, 0.33, 3.0, 1.0, 1.0],
                        [0.33, 0.33, 3.0, 1.0, 1.0]]

    col_sum = [.0] * count_columns
    for row in criteria_matrix:
        for (indx, val) in row:
            col_sum[indx] += val

    eigen_vector = []
    for row in criteria_matrix:
        t_sum = .0
        for (indx, _) in criteria_matrix:
            row[indx] /= col_sum[indx]
            t_sum += row[indx]
        eigen_vector.append(t_sum)

    return eigen_vector

