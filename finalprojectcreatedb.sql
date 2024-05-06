CREATE DATABASE UniversityDB;
USE UniversityDB;

-- Admin Table
CREATE TABLE Admin (
    admin_ID INT AUTO_INCREMENT PRIMARY KEY,
    adminname VARCHAR(255),
    adminnumber VARCHAR(255),
    adminemail VARCHAR(255) UNIQUE
);

-- Account Table
CREATE TABLE Account (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    Account_Type ENUM('admin', 'student', 'lecturer')
);

-- Students Table
CREATE TABLE Students (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Password VARCHAR(255)
);

-- Lecturers Table
CREATE TABLE Lecturers (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Password VARCHAR(255)
);

-- Courses Table
CREATE TABLE Courses (
    Course_id INT AUTO_INCREMENT PRIMARY KEY,
    Coursename VARCHAR(255),
    CourseLecturer VARCHAR(255),
    Coursegrade VARCHAR(255),
    Lecturer_ID INT,
    FOREIGN KEY (Lecturer_ID) REFERENCES Lecturers(ID)
);

-- Assignment Table
CREATE TABLE Assignment (
    ID_Number INT AUTO_INCREMENT PRIMARY KEY,
    Assignmentgrade VARCHAR(255),
    Assignmentnumber INT
);

-- Section Table
CREATE TABLE Section (
    Sectionid INT AUTO_INCREMENT PRIMARY KEY,
    Section_Name VARCHAR(255),
    Active BOOLEAN,
    Courseid INT,
    FOREIGN KEY (Courseid) REFERENCES Courses(Course_id)
);

-- Sectionitems Table
CREATE TABLE Sectionitems (
    Sectionid INT,
    Itemid INT AUTO_INCREMENT PRIMARY KEY,
    ItemName VARCHAR(255),
    FOREIGN KEY (Sectionid) REFERENCES Section(Sectionid)
);

-- Discussion Forum Table
CREATE TABLE discussionforum (
    Forum_ID INT AUTO_INCREMENT PRIMARY KEY,
    Discussion_Name VARCHAR(255),
    Course_id INT,
    Date_Posted DATETIME,
    Active BOOLEAN,
    FOREIGN KEY (Course_id) REFERENCES Courses(Course_id)
);

-- Discussion Threads Table
CREATE TABLE discussionthreads (
    Thread_ID INT AUTO_INCREMENT PRIMARY KEY,
    Forum_ID INT,
    Threadname VARCHAR(255),
    Threadreplies INT,
    Threadno INT,
    Replycontent TEXT,
    FOREIGN KEY (Forum_ID) REFERENCES discussionforum(Forum_ID)
);

-- Calendar Events Table
CREATE TABLE CalendarEvents (
    Event_no INT AUTO_INCREMENT PRIMARY KEY,
    eventname VARCHAR(255),
    eventdate DATETIME,
    courseid INT,
    FOREIGN KEY (courseid) REFERENCES Courses(Course_id)
);
