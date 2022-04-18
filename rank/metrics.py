from math import sqrt


def euclidean_distance(row, b_distance, w_distance):
    row_b_distance, row_w_distance = .0, .0
    for (indx, nested_row) in enumerate(row[1:]):
        row_b_distance += (b_distance[indx] - nested_row) * (b_distance[indx] - nested_row)
        row_w_distance += (w_distance[indx] - nested_row) * (w_distance[indx] - nested_row)

    return (sqrt(row_w_distance) / (sqrt(row_w_distance) + sqrt(row_b_distance))) if row_b_distance != 0.0 else 1


def minkowski_distance(row, b_distance, w_distance, p, weights):
    row_b_distance, row_w_distance = .0, .0
    for (indx, nested_row) in enumerate(row[1:]):
        row_b_distance += weights[indx] * (b_distance[indx] - nested_row) ** p
        row_w_distance += weights[indx] * (w_distance[indx] - nested_row) ** p

    return (row_w_distance ** (1 / p)) / (row_w_distance ** (1 / p) + (row_b_distance ** (1 / p))) \
        if row_b_distance != 0.0 else 1
