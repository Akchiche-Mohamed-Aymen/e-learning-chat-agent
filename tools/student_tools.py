from langchain.tools import tool
from json import load
data = load(open('./data/students.json'))
def get_related_students(name: str):
    '''This function is built to get student profile and progress'''
    name = name.lower()
    n = len(data)
    result = []
    for i in range(n):
        if data[i]['name'] == name:
            result.append(data[i])
    return result
@tool
def get_student_profile(name: str):
    '''This tool is built to get full profile of the student'''
    students = get_related_students(name)
    if students == []:
        return "Student not found"
    return {k: v for k, v in students[0].items() if k != "watched"}     
@tool
def get_student_progress(name: str):
    '''This tool is built to get progress of the student'''
    students = get_related_students(name)
    if students == []:
        return "Student not found"
    return students[0]['watched']           

@tool
def search_students(name: str):
    '''This tool is built to search students by name , and solve the confusion of multiple students with the same name'''
    name = name.lower()
    related_students = get_related_students(name)
    if len(related_students) == 0:
        return "No student found"
    return related_students
@tool
def get_student_summary(name):
    '''This tool is built to get summary of the student'''
    students = get_related_students(name)
    if students == []:
        return "Student not found"
    student = students[0]
    summary = f"**Level:** {student['level']}\n"
    summary += f"**Most Watched Video:** {max(student['watched'], key=student['watched'].get)}\n"
    summary += f"**Least Watched Video:** {min(student['watched'], key=student['watched'].get)}\n"
    summary += f"**Total Videos Watched:** {sum(student['watched'].values())}\n"
    return summary