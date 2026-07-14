from langchain.tools import tool
from json import load
@tool
def extract_instructor_info():
    """
    Returns the platform instructor's biography, specializations, and contact
    information.
    Use this tool whenever the user asks:
    - about Dr. Sarah Johnson or the instructor,
    - how to contact the instructor,
    - how to send a message, request, or email to the instructor,
    - for any communication channel.
"""
    return load(open('./data/instructor.json' ,  'r'))
