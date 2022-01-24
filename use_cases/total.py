import copy
import random
from typing import List, Tuple, TypeVar

from scipy.optimize import linear_sum_assignment
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.session import Session

from models import Character, Stage, Record

T = TypeVar("T")
Assignment = Tuple[List[int], List[int]]


def _chunks(lst: List[T], n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def _calculate_total(assignment: Assignment, cost_matrix: List[List[float]]):
    return sum(
        cost_matrix[char_pos][stage_pos] for (char_pos, stage_pos) in zip(*assignment)
    )


def _get_lowest_helpful_improvement(
    inverted_total: float,
    inverted_cost_matrix: List[List[float]],
    char_pos: int,
    stage_pos: int,
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


def _get_main_cast_records(session: Session) -> List[Record]:
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


def get_worst_total_records(session: Session):
    records_main_cast = _get_main_cast_records(session)
    records_matrix = list(_chunks(records_main_cast, 25))
    inverted_cost_matrix = [
        [
            -record.time if record.time is not None else float("inf")
            for record in character_records
        ]
        for character_records in records_matrix
    ]
    assignment: Assignment = linear_sum_assignment(inverted_cost_matrix)
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


def get_best_total_records(session: Session):
    records_main_cast = _get_main_cast_records(session)
    records_matrix = list(_chunks(records_main_cast, 25))
    cost_matrix = [
        [
            record.time if record.time is not None else float("inf")
            for record in character_records
        ]
        for character_records in records_matrix
    ]
    assignment: Assignment = linear_sum_assignment(cost_matrix)
    best_records = [
        records_matrix[char_pos][stage_pos]
        for (char_pos, stage_pos) in zip(*assignment)
    ]
    total = _calculate_total(assignment, cost_matrix)
    return best_records, total


def get_best_total_full_mismatch_records(session: Session):
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
    assignment: Assignment = linear_sum_assignment(cost_matrix)
    best_records = [
        records_matrix[char_pos][stage_pos]
        for (char_pos, stage_pos) in zip(*assignment)
    ]
    total = _calculate_total(assignment, cost_matrix)
    return best_records, total


def get_random_total(session: Session):
    records_main_cast = _get_main_cast_records(session)
    records_by_stage = {}
    for record in records_main_cast:
        if record.stage.position not in records_by_stage:
            records_by_stage[record.stage.position] = []
        if record.time is not None:
            records_by_stage[record.stage.position].append(record)
    assigned_character_positions: List[int] = set()
    stage_pick_order = [
        17,  # YL
        20,  # Puff
        5,  # Yoshi
        0,  # Doc
        *list(range(1, 5)),
        *list(range(6, 17)),
        *list(range(18, 20)),
        *list(range(21, 25)),
    ]
    assignment: List[Record] = []
    for stage_pos in stage_pick_order:
        stage_records = [
            record
            for record in records_by_stage[stage_pos]
            if record.character.position not in assigned_character_positions
        ]
        random_record = random.choice(stage_records)
        assignment.append(random_record)
        assigned_character_positions.add(random_record.character.position)
    ordered_records = sorted(assignment, key=lambda record: record.character.position)
    return ordered_records, sum(record.time for record in ordered_records)
