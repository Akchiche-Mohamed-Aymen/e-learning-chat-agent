import json
import random
data = json.load(open("data/learning.json"))['courses']
def getWatched(level):
    current_level = data[level]
    watched = {}
    for key , value in current_level.items():
        watched[key] = random.randint(0, value)
    return watched
first_names = [
    "Mohamed", "Ahmed", "Yacine", "Amine", "Sofiane",
    "Sarah", "Aya", "Nour", "Meriem", "Lina"
]


last_names = [
    "Akchiche", "Benali", "Bouzid", "Mansouri",
    "Cherif", "Khaldi", "Hamdi", "Brahimi"
]

levels = ["A1", "A2", "B1", "B2", "C1", "C2"]

students = []

for i in range(1000):
    first = random.choice(first_names)
    last = random.choice(last_names)
    student = {
        "name": f"{first} {last}",
        "email": f"{first}.{last}@gmail.com",
        "phone": f"+2135{random.randint(10000000,99999999)}",
        "level": random.choice(levels)}
    student['watched'] = getWatched(student['level'])    
    students.append(student)

with open("data/students.json", "w") as f:
    json.dump(students, f, indent=2)

print("Generated 1000 students")