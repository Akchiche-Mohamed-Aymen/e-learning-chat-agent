from json import load
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