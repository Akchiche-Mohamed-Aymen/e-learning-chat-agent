from langchain.tools import tool
from auth.repeated_code import  get_student_by_name
from json import load 


def get_courses(level: str)->str:
    learning_data = load(open('./data/learning.json'))
    return learning_data['courses'][level]
@tool
def get_student_profile(name: str):
    '''This tool is built to get full profile of the student'''
    students = get_student_by_name(name)
    if isinstance(students, dict):
        return students['error']
    elif len(students) > 1:
        return "Multiple students matched the name provided. Please provide a more specific name."
    student = students[0]
    return {k: v for k, v in student.items() if k != "watched"}     
@tool
def get_student_course_progress(name: str):
    '''This tool is built to get progress of the student'''
    students = get_student_by_name(name)
    if isinstance(students , dict):
        return students['error']
    elif len(students) > 1:
        return "Multiple students matched the name provided. Please provide a more specific name."
    student = students[0]
    watched = student['watched']
    courses = get_courses(student['level'])
    progress = {}
    for key in courses.keys():
        if key in watched:
            progress[key] = f'{round((watched[key] / courses[key]) * 100, 2)} %' 
    progress['completion_percentage'] = f'{round((sum(watched.values()) / sum(courses.values())) * 100, 2)} %'
    return progress

@tool
def get_student_summary(name : str):
    '''This tool is built to get stats about the student'''
    students = get_student_by_name(name)
    if isinstance(students , dict):
        return students['error']
    elif len(students) > 1:
        return "Multiple students matched the name provided. Please provide a more specific name."
    student = students[0]
    summary = f"**Level:** {student['level']}\n"
    summary += f"**Most Watched Video:** {max(student['watched'], key=student['watched'].get)}\n"
    summary += f"**Least Watched Video:** {min(student['watched'], key=student['watched'].get)}\n"
    summary += f"**Total Videos Watched:** {sum(student['watched'].values())}\n"
    return summary
@tool
def recommend_next_skill(name : str):
    '''This tool is built to recommend the next skill for the student'''
    students = get_student_by_name(name)
    if isinstance(students , dict):
        return students['error']
    elif len(students) > 1:
        return "Multiple students matched the name provided. Please provide a more specific name."
    student = students[0]
    if student is None:
        return "No student matched the name provided"
    courses = get_courses(student['level'])
    watched = student['watched']
    for _ in range(4):
        min_skill = min(watched ,  key=watched.get)
        if watched[min_skill] < courses[min_skill]:
            return min_skill
        else:
            watched  = watched.pop(min_skill)
            if watched == {}:
                return "All skills completed for this level , great job! You can move to the next level."

student_tools = [get_student_profile, get_student_course_progress, get_student_summary, recommend_next_skill]
