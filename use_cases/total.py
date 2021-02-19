import copy

from scipy.optimize import linear_sum_assignment

from models import Character, Stage, Record


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def _calculate_total(assignment, cost_matrix):
    return sum(
        cost_matrix[char_pos][stage_pos] for (char_pos, stage_pos) in zip(*assignment)
    )


def _get_lowest_helpful_improvement(
    inverted_total, inverted_cost_matrix, char_pos, stage_pos
):
    cur_total = inverted_total
    upper_bound_time = 0
    lower_bound_time = inverted_cost_matrix[char_pos][stage_pos]

    matrix_copy = copy.deepcopy(inverted_cost_matrix)
    matrix_copy[char_pos][stage_pos] = 0
    best_total = _calculate_total(linear_sum_assignment(matrix_copy), matrix_copy)
    while True:
        midtime = (upper_bound_time + lower_bound_time) // 2
        matrix_copy[char_pos][stage_pos] = midtime
        cur_total = _calculate_total(linear_sum_assignment(matrix_copy), matrix_copy)
        if cur_total < best_total:
            if midtime == lower_bound_time:
                return -upper_bound_time
            lower_bound_time = midtime
        else:
            if midtime == lower_bound_time:
                return -lower_bound_time
            upper_bound_time = midtime


def get_worst_total_records(session):
    records_main_cast = (
        session.query(Record)
        .join(Character)
        .join(Stage)
        .filter(Character.position <= 24, Stage.position <= 24)
        .order_by(Character.position, Stage.position)
        .all()
    )
    records_matrix = list(_chunks(records_main_cast, 25))
    inverted_cost_matrix = [
        [
            -record.time if record.time is not None else float("inf")
            for record in character_records
        ]
        for character_records in records_matrix
    ]
    assignment = linear_sum_assignment(inverted_cost_matrix)
    worst_records = [
        records_matrix[char_pos][stage_pos]
        for (char_pos, stage_pos) in zip(*assignment)
    ]
    inverted_total = _calculate_total(assignment, inverted_cost_matrix)
    lowest_helpful_improvements = [
        _get_lowest_helpful_improvement(
            inverted_total, inverted_cost_matrix, char_pos, stage_pos
        )
        for char_pos, stage_pos in zip(*assignment)
    ]

    return worst_records, lowest_helpful_improvements, -inverted_total


def get_best_total_records(session):
    records_main_cast = (
        session.query(Record)
        .join(Character)
        .join(Stage)
        .filter(Character.position <= 24, Stage.position <= 24)
        .order_by(Character.position, Stage.position)
        .all()
    )
    records_matrix = list(_chunks(records_main_cast, 25))
    cost_matrix = [
        [
            record.time if record.time is not None else float("inf")
            for record in character_records
        ]
        for character_records in records_matrix
    ]
    assignment = linear_sum_assignment(cost_matrix)
    best_records = [
        records_matrix[char_pos][stage_pos]
        for (char_pos, stage_pos) in zip(*assignment)
    ]
    total = _calculate_total(assignment, cost_matrix)
    return best_records, total


def get_best_total_full_mismatch_records(session):
    records_main_cast = (
        session.query(Record)
        .join(Character)
        .join(Stage)
        .filter(Character.position <= 24, Stage.position <= 24)
        .order_by(Character.position, Stage.position)
        .all()
    )
    records_matrix = list(_chunks(records_main_cast, 25))
    cost_matrix = [
        [
            record.time
            if record.time is not None
            and record.character.position != record.stage.position
            else float("inf")
            for record in character_records
        ]
        for character_records in records_matrix
    ]
    assignment = linear_sum_assignment(cost_matrix)
    best_records = [
        records_matrix[char_pos][stage_pos]
        for (char_pos, stage_pos) in zip(*assignment)
    ]
    total = _calculate_total(assignment, cost_matrix)
    return best_records, total
