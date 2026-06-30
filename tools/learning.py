from json import load
from langchain.tools import tool
data = load(open('./data/learning.json'))
@tool
def get_courses_stats_by_level(level: str)->str:
    """
    Search information about an English learning level (A1-C2).
    Returns the number of reading, writing, listening, and speaking lessons,
    """
    info = data['courses']['level']
    return f'''
         Level {level} contains :
        - Reading: {info['reading']} lessons
        - Writing: {info['writing']} lessons
        - Listening: {info['listening']} lessons
        - Speaking: {info['speaking']} lessons
    
    '''

    
@tool
def get_exam_link():
    return data['exam_level_link']