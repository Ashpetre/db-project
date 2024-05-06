from flask import Flask, request, jsonify, abort
import mysql.connector

app = Flask(__name__)

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'passwordforlab!',
    'database': 'UniversityDB'
}

# Utility function to connect to the database
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection


@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Account (Name, Email, Password, Account_Type) 
            VALUES (%s, %s, %s, %s);
        """, (data['name'], data['email'], data['password'], data['account_type']))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(400, str(err))
    finally:
        cursor.close()
        conn.close()
    return jsonify({"status": "success", "message": "User registered."}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM Account WHERE Email = %s AND Password = %s;
        """, (data['email'], data['password']))
        user = cursor.fetchone()
        if user:
            return jsonify(user), 200
        else:
            abort(401, "Invalid credentials")
    finally:
        cursor.close()
        conn.close()

@app.route('/courses', methods=['POST'])
def create_course():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # This should check if the user is an admin before proceeding.
        cursor.execute("""
            INSERT INTO Courses (Coursename, Lecturer_ID) VALUES (%s, %s);
        """, (data['coursename'], data['lecturer_id']))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(400, str(err))
    finally:
        cursor.close()
        conn.close()
    return jsonify({"status": "success", "message": "Course created."}), 201

@app.route('/courses', methods=['GET'])
def get_all_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Courses;")
        courses = cursor.fetchall()
        return jsonify(courses), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/courses/student/<int:student_id>', methods=['GET'])
def get_courses_for_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM Courses WHERE Course_id IN (
                SELECT Course_ID FROM StudentCourses WHERE Student_ID = %s
            );
        """, (student_id,))
        courses = cursor.fetchall()
        return jsonify(courses), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/courses/lecturer/<int:lecturer_id>', methods=['GET'])
def get_courses_for_lecturer(lecturer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM Courses WHERE Lecturer_ID = %s;
        """, (lecturer_id,))
        courses = cursor.fetchall()
        return jsonify(courses), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/register_course', methods=['POST'])
def register_for_course():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO StudentCourses (Student_ID, Course_ID) VALUES (%s, %s);
        """, (data['student_id'], data['course_id']))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(400, str(err))
    finally:
        cursor.close()
        conn.close()
    return jsonify({"status": "success", "message": "Student registered for course."}), 201

@app.route('/courses/<int:course_id>/members', methods=['GET'])
def get_course_members(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM Students WHERE ID IN (
                SELECT Student_ID FROM StudentCourses WHERE Course_ID = %s
            );
        """, (course_id,))
        members = cursor.fetchall()
        return jsonify(members), 200
    finally:
        cursor.close()
        conn.close()

# Additional endpoints for Create Calendar Events, Forums, Discussion Threads, and Course Content would follow a similar pattern.
# ...previous imports and setup...

# Retrieve Calendar Events for a Course
@app.route('/courses/<int:course_id>/calendar', methods=['GET'])
def get_calendar_events(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM CalendarEvents WHERE Course_id = %s;
        """, (course_id,))
        events = cursor.fetchall()
        return jsonify(events), 200
    finally:
        cursor.close()
        conn.close()

# Create Calendar Events for a Course
@app.route('/courses/<int:course_id>/calendar', methods=['POST'])
def create_calendar_event(course_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO CalendarEvents (EventName, Date, Course_id) VALUES (%s, %s, %s);
        """, (data['event_name'], data['date'], course_id))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(400, str(err))
    finally:
        cursor.close()
        conn.close()
    return jsonify({"status": "success", "message": "Calendar event created."}), 201

# Retrieve all forums for a course
@app.route('/courses/<int:course_id>/forums', methods=['GET'])
def get_forums(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM Forums WHERE Course_id = %s;
        """, (course_id,))
        forums = cursor.fetchall()
        return jsonify(forums), 200
    finally:
        cursor.close()
        conn.close()

# Create a forum for a course
@app.route('/courses/<int:course_id>/forums', methods=['POST'])
def create_forum(course_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Forums (ForumName, Course_id) VALUES (%s, %s);
        """, (data['forum_name'], course_id))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(400, str(err))
    finally:
        cursor.close()
        conn.close()
    return jsonify({"status": "success", "message": "Forum created."}), 201

# Retrieve all discussion threads for a forum
@app.route('/forums/<int:forum_id>/threads', methods=['GET'])
def get_discussion_threads(forum_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM DiscussionThreads WHERE Forum_ID = %s;
        """, (forum_id,))
        threads = cursor.fetchall()
        return jsonify(threads), 200
    finally:
        cursor.close()
        conn.close()

# Create a new discussion thread for a forum
@app.route('/forums/<int:forum_id>/threads', methods=['POST'])
def create_discussion_thread(forum_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO DiscussionThreads (Title, Content, Forum_ID) VALUES (%s, %s, %s);
        """, (data['title'], data['content'], forum_id))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(400, str(err))
    finally:
        cursor.close()
        conn.close()
    return jsonify({"status": "success", "message": "Discussion thread created."}), 201

# Retrieve course content for a course
@app.route('/courses/<int:course_id>/content', methods=['GET'])
def get_course_content(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM CourseContent WHERE Course_id = %s;
        """, (course_id,))
        content = cursor.fetchall()
        return jsonify(content), 200
    finally:
        cursor.close()
        conn.close()

# Add course content to a course
@app.route('/courses/<int:course_id>/content', methods=['POST'])
def add_course_content(course_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO CourseContent (ContentName, ContentType, Content, Course_id) VALUES (%s, %s, %s, %s);
        """, (data['content_name'], data['content_type'], data['content'], course_id))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(400, str(err))
    finally:
        cursor.close()
        conn.close()
    return jsonify({"status": "success", "message": "Course content added."}), 201

# Submit an assignment for a course
@app.route('/courses/<int:course_id>/assignments', methods=['POST'])
def submit_assignment(course_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Assignments (AssignmentContent, Student_ID, Course_id) VALUES (%s, %s, %s);
        """, (data['assignment_content'], data['student_id'], course_id))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(400, str(err))
    finally:
        cursor.close()
        conn.close()
    return jsonify({"status": "success", "message": "Assignment submitted."}), 201

# Submit a grade for an assignment
@app.route('/assignments/<int:assignment_id>/grade', methods=['POST'])
def grade_assignment(assignment_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Assignments SET Grade = %s WHERE Assignment_ID = %s;
        """, (data['grade'], assignment_id))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(400, str(err))
    finally:
        cursor.close()
        conn.close()
    return jsonify({"status": "success", "message": "Grade submitted for assignment."}), 201

# Retrieve reports (assuming the views have already been created in the database)
@app.route('/reports/courses', methods=['GET'])
def get_course_reports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM ReportCoursesView;")
        reports = cursor.fetchall()
        return jsonify(reports), 200
    finally:
        cursor.close()
        conn.close()
        



if __name__ == '__main__':
    app.run(debug=True)
