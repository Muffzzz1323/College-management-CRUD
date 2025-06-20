from students import *

def menu():
    while True:
        print("\n=== College Management System ===")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student Email")
        print("4. Delete Student")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            sid = int(input("Student ID: "))
            name = input("Name: ")
            dept = input("Department: ")
            year = int(input("Year: "))
            email = input("Email: ")
            add_student(sid, name, dept, year, email)
        elif choice == '2':
            view_students()
        elif choice == '3':
            sid = int(input("Student ID: "))
            email = input("New Email: ")
            update_student_email(sid, email)
        elif choice == '4':
            sid = int(input("Student ID: "))
            delete_student(sid)
        elif choice == '5':
            break
        else:
            print("❗Invalid choice. Try again.")

if __name__ == "__main__":
    from database import create_tables
    create_tables()
    menu()
