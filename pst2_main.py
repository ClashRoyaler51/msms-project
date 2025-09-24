# pst2_main.py - The Persistent Application
import json
import datetime

DATA_FILE = "msms.json"
app_data = {
    "students": [],
    "teachers": [],
    "attendance": [],
    "next_student_id": 1,
    "next_teacher_id": 1
} # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            # TODO: Use json.load(f) to load the file's content into the global 'app_data' variable.
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        # TODO: If the file doesn't exist, initialize 'app_data' with a default dictionary.
        # It should have keys like: "students", "teachers", "attendance", "next_student_id", "next_teacher_id".
        # The lists should be empty and the IDs should start at 1.
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    # TODO: Open the file at 'path' in write mode ('w').
    # Use json.dump() to write the global 'app_data' dictionary to the file.
    # Use the 'indent=4' argument in json.dump() to make the file readable.
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")

# --- Helper function ---
def get_nonempty_input(prompt):
    """Prompts until the user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")

# --- Full CRUD for Core Data ---
def add_teacher(name, speciality):
    """Adds a teacher dictionary to the data store."""
    teacher_id = app_data['next_teacher_id']
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    app_data['teachers'].append(new_teacher)
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")

def update_teacher(teacher_id, **fields):
    """Finds a teacher by ID and updates their data with provided fields."""
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")

def remove_student(student_id):
    """Removes a student from the data store."""
    for i in range(len(app_data['attendance'])): 
        if app_data['attendance'][i]['student_id'] == student_id:
            app_data['attendance'].remove(app_data['attendance'][i])
            print(f"Student {student_id} removed.")
            return
    app_data['students'] = [s for s in app_data['students'] if s['id'] != student_id]
    print(f"Student {student_id} removed.")

def remove_teacher(teacher_id):
    """Removes a teacher from the data store."""
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            app_data['teachers'].remove(teacher)
            print(f"Teacher {teacher_id} removed.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")

def update_student(student_id, **fields):
    """Finds a student by ID and updates their data with provided fields."""
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return
    print(f"Error: Student with ID {student_id} not found.") 

# --- New Receptionist Features ---
def check_in(student_id, course_id, timestamp=None):
    """Records a student's attendance for a course."""
    if timestamp is None:
        # TODO: Get the current time as a string using datetime.datetime.now().isoformat()
        timestamp = datetime.datetime.now().isoformat()
    
    # --- Inline fix: create student if missing ---
    student = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student = s
            break
    if student is None:
        student = {"id": student_id, "name": f"Student{student_id}", "enrolled_in": []}
        app_data['students'].append(student)
        print(f"Info: Created dummy student with ID {student_id}")

    # --- Inline fix: create courses structure if missing ---
    if 'courses' not in app_data:
        app_data['courses'] = []

    course = None
    for c in app_data['courses']:
        if c['id'] == course_id:
            course = c
            break
    if course is None:
        course = {"id": course_id, "name": f"Course{course_id}", "instrument": "", "enrolled_students": []}
        app_data['courses'].append(course)
        print(f"Info: Created dummy course with ID {course_id}")

    # Add student to course and course to student
    if course_id not in student.get('enrolled_in', []):
        student.setdefault('enrolled_in', []).append(course_id)
    if student_id not in course.get('enrolled_students', []):
        course.setdefault('enrolled_students', []).append(student_id)

    # TODO: Create a check-in record dictionary.
    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    # TODO: Append this new record to the app_data['attendance'] list.
    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student_id} checked into {course_id}.")
    save_data()  # <- ensures JSON is updated immediately

def print_student_card(student_id):
    """Creates a text file badge for a student."""
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break
    
    if student_to_print:
        filename = f"{student_id}_card.txt"
        with open(filename, 'w') as f:
            f.write("========================\n")
            f.write(f"  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Enrolled In: {', '.join(str(cid) for cid in student_to_print.get('enrolled_in', []))}\n")
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")
    
# --- Main Application Loop ---
def main():
    """Main function to run the MSMS application."""
    load_data() # Load all data from file at startup.

    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("1. Check-in Student")
        print("2. Print Student Card")
        print("3. Update Teacher Info")
        print("4. Remove Student")
        print("q. Quit and Save")
        
        choice = get_nonempty_input("Enter your choice: ")
        
        made_change = False # A flag to track if we need to save
        if choice == '1':
            student_id = int(get_nonempty_input("Enter student ID: "))
            course_id = int(get_nonempty_input("Enter course ID: "))
            check_in(student_id, course_id)
            made_change = False  # already saved inside check_in()

        elif choice == '2':
            student_id = int(get_nonempty_input("Enter student ID: "))
            print_student_card(student_id)
            made_change = False

        elif choice == '3':
            teacher_id = int(get_nonempty_input("Enter teacher ID: "))
            new_speciality = get_nonempty_input("Enter new speciality: ")
            update_teacher(teacher_id, speciality=new_speciality)
            made_change = True

        elif choice == '4':
            student_id = int(get_nonempty_input("Enter student ID: "))
            remove_student(student_id)
            made_change = True

        elif choice.lower() == 'q':
            print("Saving final changes and exiting.")
            break
        else:
            print("Invalid choice.")

        if made_change:
            save_data() # Save the data immediately after any change.

    save_data() # One final save on exit.

# --- Program Start ---
if __name__ == "__main__":
    main()
