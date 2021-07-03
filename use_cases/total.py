import copy

from munkres import Munkres
from sqlalchemy.orm import contains_eager

from models import Character, Stage, Record

m = Munkres()


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def _calculate_total(assignment, cost_matrix):
    return sum(cost_matrix[char_pos][stage_pos] for (char_pos, stage_pos) in assignment)


def _get_lowest_helpful_improvement(
    inverted_total, inverted_cost_matrix, char_pos, stage_pos
):
    cur_total = inverted_total
    upper_bound_time = 0
    lower_bound_time = inverted_cost_matrix[char_pos][stage_pos]

    matrix_copy = copy.deepcopy(inverted_cost_matrix)
    matrix_copy[char_pos][stage_pos] = 0
    best_total = _calculate_total(m.compute(matrix_copy), matrix_copy)
    while True:
        midtime = (upper_bound_time + lower_bound_time) // 2
        matrix_copy[char_pos][stage_pos] = midtime
        cur_total = _calculate_total(m.compute(matrix_copy), matrix_copy)
        if cur_total < best_total:
            if midtime == lower_bound_time:
                return -upper_bound_time
            lower_bound_time = midtime
        else:
            if midtime == lower_bound_time:
                return -lower_bound_time
            upper_bound_time = midtime


def _get_main_cast_records(session):
    return (
        session.query(Record)
        .join(Record.character)
        .join(Record.stage)
        .join(Record.players, isouter=True)
        .options(contains_eager(Record.character))
        .options(contains_eager(Record.stage))
        .options(contains_eager(Record.players))
        .filter(Character.position <= 24, Stage.position <= 24)
        .order_by(Character.position, Stage.position)
        .all()
    )


def get_worst_total_records(session):
    records_main_cast = _get_main_cast_records(session)
    records_matrix = list(_chunks(records_main_cast, 25))
    inverted_cost_matrix = [
        [
            -record.time if record.time is not None else float("inf")
            for record in character_records
        ]
        for character_records in records_matrix
    ]
    assignment = m.compute(inverted_cost_matrix)
    worst_records = [
        records_matrix[char_pos][stage_pos] for (char_pos, stage_pos) in assignment
    ]
    inverted_total = _calculate_total(assignment, inverted_cost_matrix)
    lowest_helpful_improvements = [
        _get_lowest_helpful_improvement(
            inverted_total, inverted_cost_matrix, char_pos, stage_pos
        )
        for char_pos, stage_pos in assignment
    ]

    return worst_records, lowest_helpful_improvements, -inverted_total


def get_best_total_records(session):
    records_main_cast = _get_main_cast_records(session)
    records_matrix = list(_chunks(records_main_cast, 25))
    cost_matrix = [
        [
            record.time if record.time is not None else float("inf")
            for record in character_records
        ]
        for character_records in records_matrix
    ]
    assignment = m.compute(cost_matrix)
    best_records = [
        records_matrix[char_pos][stage_pos] for (char_pos, stage_pos) in assignment
    ]
    total = _calculate_total(assignment, cost_matrix)
    return best_records, total


def get_best_total_full_mismatch_records(session):
    records_main_cast = _get_main_cast_records(session)
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
    assignment = m.compute(cost_matrix)
    best_records = [
        records_matrix[char_pos][stage_pos] for (char_pos, stage_pos) in assignment
    ]
    total = _calculate_total(assignment, cost_matrix)
    return best_records, total
