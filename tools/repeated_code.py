from json import load
from rapidfuzz import process, fuzz

students_data = load(open('./data/students.json'))
learning_data = load(open('./data/learning.json'))

def get_related_students(name: str):
    '''This function is built to get student profile and progress'''
    name = name.lower()
    n = len(students_data)
    result = []
    for i in range(n):
        if students_data[i]['name'] == name:
            result.append(students_data[i])
    return result
def get_courses(level: str)->str:
    return learning_data['courses'][level]

students_names = [student['name'] for student in students_data]
def get_student_by_name(name: str):
    name = name.lower()
    result = process.extractOne(
        name,
        students_names,
        scorer=fuzz.partial_ratio
    )
    if result is None:
        return None
    _, score, index = result
    return students_data[index] if score >= 70 else None