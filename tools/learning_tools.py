from langchain.tools import tool
from repeated_code import get_courses_stats_by_level , learning_data , student_data
@tool
def get_courses_stats_by_level(level: str)->str:
    """
    Search information about an English learning level (A1-C2).
    Returns the number of reading, writing, listening, and speaking lessons,
    levels are A1, A2, B1, B2, C1, C2.
    """
    info = get_courses_stats_by_level(level)
    return f'''
        Level {level} contains :
        - Reading: {info['reading']} lessons
        - Writing: {info['writing']} lessons
        - Listening: {info['listening']} lessons
        - Speaking: {info['speaking']} lessons
    '''   
@tool
def get_exam_link():
    return learning_data['exam_level_link']
@tool
def num_of_enrolled_students(level: str):
    """
    Search the number of enrolled students in a specific English learning level (A1-C2).
    Returns the number of enrolled students for the specified level.
    """
    num = 0
    for student in student_data:
        if student['level'] == level:
            num += 1
    return f"Number of enrolled students in level {level}: {num}"
learning_tools = [get_courses_stats_by_level, get_exam_link, num_of_enrolled_students]