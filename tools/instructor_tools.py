from langchain.tools import tool
from json import load
@tool
def extract_instructor_info():
    '''This tools is built to get full profile of the instructor'''
    return load(open('./data/instructor.json' ,  'r'))
