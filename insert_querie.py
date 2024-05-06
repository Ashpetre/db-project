import random



# Parameters
num_students = 100000
num_courses = 200
num_lecturers = 40
min_courses_per_student = 3
max_courses_per_student = 6
min_courses_per_lecturer = 1
max_courses_per_lecturer = 5
min_students_per_course = 10

# Generate Lecturers
lecturers = [{'id': i, 'courses': []} for i in range(1, num_lecturers + 1)]

# Assign Courses to Lecturers
courses = []
for i in range(1, num_courses + 1):
    lecturer_id = random.choice(lecturers)['id']
    courses.append({'id': i, 'lecturer_id': lecturer_id, 'students': []})

# Ensure each lecturer teaches at least one course
for lecturer in lecturers:
    if not any(course['lecturer_id'] == lecturer['id'] for course in courses):
        course_to_assign = random.choice([c for c in courses if c['lecturer_id'] != lecturer['id']])
        course_to_assign['lecturer_id'] = lecturer['id']

# Generate Students and enroll them in courses
students = [{'id': i, 'courses': set()} for i in range(1, num_students + 1)]

for student in students:
    courses_to_enroll = random.sample(courses, random.randint(min_courses_per_student, max_courses_per_student))
    for course in courses_to_enroll:
        student['courses'].add(course['id'])
        course['students'].append(student['id'])

# Ensure each course has at least 10 students
for course in courses:
    while len(course['students']) < min_students_per_course:
        student = random.choice(students)
        if len(student['courses']) < max_courses_per_student:
            student['courses'].add(course['id'])
            course['students'].append(student['id'])

# SQL Output
sql_statements = []
sql_statements.append(f"USE UniversityDB;")

# Insert Lecturers
for lecturer in lecturers:
    sql_statements.append(f"INSERT INTO Lecturers (ID, Name, Email, Password) VALUES ({lecturer['id']}, 'Lecturer{lecturer['id']}', 'lecturer{lecturer['id']}@example.com', 'password');")

# Insert Courses
for course in courses:
    sql_statements.append(f"INSERT INTO Courses (Course_id, Coursename, Lecturer_ID) VALUES ({course['id']}, 'Course{course['id']}', {course['lecturer_id']});")

# Insert Students
for student in students:
    sql_statements.append(f"INSERT INTO Students (ID, Name, Email, Password) VALUES ({student['id']}, 'Student{student['id']}', 'student{student['id']}@example.com', 'password');")

# Enroll Students in Courses
for student in students:
    for course_id in student['courses']:
        sql_statements.append(f"INSERT INTO StudentCourses (Student_ID, Course_ID) VALUES ({student['id']}, {course_id});")

# Save SQL statements to a file
with open('insert.sql', 'w') as file:
    file.write('\n'.join(sql_statements))

print("SQL script generated successfully with enforced constraints.")
