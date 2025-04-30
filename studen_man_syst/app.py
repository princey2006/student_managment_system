import streamlit as st
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password",
            database="school"
        )
        return conn
    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None


def init_db():
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES LIKE 'students'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                grade VARCHAR(10)
            )
        """)
        conn.commit()
    cursor.close()
    conn.close()


def add_student(name, age, grade):
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)", (name, age, grade))
    conn.commit()
    cursor.close()
    conn.close()


def get_all_students():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_student(name):
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE %s", (f"%{name}%",))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def delete_student(student_id):
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()


def main():
    st.title("🎓 Student Management System")
    menu = ["Add Student", "Display Students", "Search Student", "Delete Student"]
    choice = st.sidebar.selectbox("Menu", menu)

    init_db()

    if choice == "Add Student":
        st.subheader("Add Student")
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, step=1)
        grade = st.text_input("Grade")
        if st.button("Add"):
            if name and grade:
                add_student(name, age, grade)
                st.success(f"Student '{name}' added successfully!")
            else:
                st.warning("Please fill all fields.")

    elif choice == "Display Students":
        st.subheader("All Students")
        students = get_all_students()
        if students:
            for student in students:
                st.write(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")
        else:
            st.info("No students found.")

    elif choice == "Search Student":
        st.subheader("Search Student by Name")
        search_name = st.text_input("Enter name to search")
        if st.button("Search"):
            results = search_student(search_name)
            if results:
                for student in results:
                    st.write(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")
            else:
                st.warning("No matching student found.")

    elif choice == "Delete Student":
        st.subheader("Delete Student by ID")
        student_id = st.number_input("Enter Student ID", step=1, min_value=1)
        if st.button("Delete"):
            delete_student(student_id)
            st.success(f"Student with ID {student_id} deleted successfully.")

if __name__ == "__main__":
    main()
