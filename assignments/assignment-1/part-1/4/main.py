from typing import Any


def has_passed(student: dict[str, Any]) -> bool:
    scores = student["calificaciones"]
    return sum(scores)/len(scores) >= 6


def filter_students(students: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return list(filter(has_passed, students))


if __name__ == "__main__":
    estudiantes = [
        {"nombre": "Juan", "calificaciones": [7, 8, 6, 5]},
        {"nombre": "Ana", "calificaciones": [9, 6, 8]},
        {"nombre": "Pedro", "calificaciones": [4, 5, 3]},
        {"nombre": "Maria", "calificaciones": [10, 9, 9]},
        {"nombre": "Luis", "calificaciones": [3, 2, 5]}
    ]

    print(filter_students(estudiantes))
