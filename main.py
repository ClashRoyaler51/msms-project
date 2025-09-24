from schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    lessons = manager.get_lessons_by_day(day)  # Call manager method
    for lesson in lessons:
        print(f"{lesson['course_name']} ({lesson['start_time']}) in {lesson['room']}")

def switch_course(manager, student_id, from_course_id, to_course_id):
    # TODO: Implement the logic to switch a student by calling methods on the manager.
    success = manager.switch_student_course(student_id, from_course_id, to_course_id)
    if success:
        print("Course switch successful.")
    else:
        print("Course switch failed. Check student or course IDs.")

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. View Daily Roster")
        print("2. Check in a Student")
        print("3. Switch Student Course")
        print("Q. Quit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)
        elif choice == '2':
            student_id = int(input("Enter student ID: "))
            course_id = int(input("Enter course ID: "))
            manager.check_in(student_id, course_id)
        elif choice == '3':
            student_id = int(input("Enter student ID: "))
            from_course_id = int(input("Enter course ID to switch from: "))
            to_course_id = int(input("Enter course ID to switch to: "))
            switch_course(manager, student_id, from_course_id, to_course_id)
        elif choice.lower() == 'q':
            break
        
if __name__ == "__main__":
    main()
