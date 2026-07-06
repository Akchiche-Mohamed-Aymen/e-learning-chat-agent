from langchain.tools import tool
from json import load
data = load(open('./data/students.json'))
@tool
def get_student_profile(name: str):
    '''This tool is built to get full profile of the student'''
    n = len(data)
    for i in range(n):
        if data[i]['name'] == name:
            info = data[i]
            break