from langchain.tools import tool
from json import load
@tool
def extract_instructor_info():
    '''This tools is built to get full profile of the instructor'''
    data = load(open('./data/instructor.json' ,  'r'))
    info = ''
    flag = False
    for key , value in data.items():
        if isinstance(value , dict):
            for key1 , value1 in value.items():
                if not flag:
                    info += f'***{key.capitalize()} *** \n'
                    flag = True
                info += f'- ** {key1} ** : {value1} \n'
            flag = False
        else :
            info += f'- ** {key} ** : {value} \n'
    return info
