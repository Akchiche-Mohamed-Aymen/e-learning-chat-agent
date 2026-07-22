import json
import random
from faker import Faker
fake = Faker()

data = json.load(open("./data/learning.json"))['courses']
def getWatched(level):
    current_level = data[level]
    watched = {}
    for key , value in current_level.items():
        watched[key] = random.randint(0, value)
    return watched


levels = ["A1", "A2", "B1", "B2", "C1", "C2"]

students = []

for i in range(1000):
    user_name = fake.name()
    print(user_name)
    student = {
        "name": f"{user_name}",
        "email": f"{user_name}@gmail.com",
        "phone": f"+2135{random.randint(10000000,99999999)}",
        "level": random.choice(levels)}
    student['watched'] = getWatched(student['level'])    
    students.append(student)

with open("./data/students.json", "w") as f:
    json.dump(students, f, indent=2)

print("Generated 1000 students")