from json import load
from rapidfuzz import process, fuzz

students_data = load(open('./data/students.json'))
learning_data = load(open('./data/learning.json'))

def get_courses(level: str)->str:
    return learning_data['courses'][level]

students_names = [student['name'] for student in students_data]
def get_student_by_name(name: str, threshold: int = 70):
    name = name.lower()

    results = process.extract(
        name,
        students_names,
        scorer=fuzz.partial_ratio,
        limit=None  # Return all matches
    )

    matches = [
        students_data[index]
        for _, score, index in results
        if score >= threshold
    ]

    return matches
