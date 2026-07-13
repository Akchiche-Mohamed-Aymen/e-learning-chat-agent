from json import load
from rapidfuzz import process, fuzz

students_data = load(open('./data/students.json'))
learning_data = load(open('./data/learning.json'))

def get_courses(level: str)->str:
    return learning_data['courses'][level]

students_names = [student['name'] for student in students_data]
def get_student_by_name(name: str, threshold: int = 70):
    name = name.lower()
    user_type = 'student' # instructor
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
    student_name = load(open(f'./tools/student.json'))['name'].lower()
    if user_type == 'instructor' and matches:
        return matches
    elif not matches and user_type == 'instructor':
        return {
            "error": "No student found with the given name."
        }
    matches = [student for student in matches if student['name'].lower() == student_name]
    if matches:
        return matches
    else :
        return {
            "error": "You are only allowed to access your own profile."
        }
    
  