from json import load
from rapidfuzz import process, fuzz

students_data = load(open('./data/students.json'))
learning_data = load(open('./data/learning.json'))

def get_courses(level: str)->str:
    return learning_data['courses'][level]

students_names = [student['name'] for student in students_data]
def get_student_by_name(name: str, threshold: int = 90):
    name = name.lower()
    user_type = 'instructor' # instructor
    result = process.extractOne(
        name,
        students_names,
        scorer=fuzz.partial_ratio
    )
    _, _, index = result
    student = students_data[index]
    student_name = load(open(f'./tools/student.json'))['name'].lower()
    if user_type == 'instructor' and student:
        return student
    elif not student and user_type == 'instructor':
        return {
            "error": "No student found with the given name."
        }
    match = student['name'] == student_name
    if match:
        return student
    else :
        return {
            "error": "You are only allowed to access your own profile."
        }
    
  