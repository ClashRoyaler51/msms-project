import json
from student import StudentUser
from teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # TODO: Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
        # ... (next_id counters) ...
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                students = data.get("students", [])
                teachers = data.get("teachers", [])
                courses = data.get("courses", [])
                attendance = data.get("attendance", [])

                # Load students
                for s in students:
                    student_obj = StudentUser(s['id'], s['name'])
                    student_obj.enrolled_course_ids = s.get('enrolled_course_ids', [])
                    self.students.append(student_obj)

                # Load teachers
                for t in teachers:
                    teacher_obj = TeacherUser(t['id'], t['name'], t.get('speciality', ""))
                    self.teachers.append(teacher_obj)

                # Load courses
                for c in courses:
                    course_obj = Course(c['id'], c['name'], c.get('instrument', ""), c.get('teacher_id', None))
                    course_obj.enrolled_student_ids = c.get('enrolled_student_ids', [])
                    course_obj.lessons = c.get('lessons', [])
                    self.courses.append(course_obj)

                # Load attendance log
                self.attendance_log = attendance

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")

    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            "attendance": self.attendance_log,
        }

        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def get_lessons_by_day(self, day):
        """Return all lessons for a given day across all courses."""
        lessons_for_day = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson.get("day") == day:
                    lessons_for_day.append({
                        "course_name": course.name,
                        "start_time": lesson.get("start_time"),
                        "room": lesson.get("room")
                    })
        return lessons_for_day

    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        # Find or create student
        student = next((s for s in self.students if s.id == student_id), None)
        if student is None:
            student = StudentUser(student_id, f"Student{student_id}")
            self.students.append(student)
            print(f"Info: Created dummy student with ID {student_id}")

        # Find or create course
        course = next((c for c in self.courses if c.id == course_id), None)
        if course is None:
            course = Course(course_id, f"Course{course_id}", "", None)
            self.courses.append(course)
            print(f"Info: Created dummy course with ID {course_id}")

        # Add student to course and course to student
        if course_id not in student.enrolled_course_ids:
            student.enrolled_course_ids.append(course_id)
        if student_id not in course.enrolled_student_ids:
            course.enrolled_student_ids.append(student_id)

        # Create attendance record
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        self.attendance_log.append(log_entry)
        print(f"{student.name} checked in for {course.name}")

        # Save immediately
        self._save_data()

    def switch_student_course(self, student_id, from_course_id, to_course_id):
        """Switch a student from one course to another."""
        student = next((s for s in self.students if s.id == student_id), None)
        from_course = next((c for c in self.courses if c.id == from_course_id), None)
        to_course = next((c for c in self.courses if c.id == to_course_id), None)

        if not student or not from_course or not to_course:
            return False

        if from_course_id not in student.enrolled_course_ids:
            return False

        # Perform switch
        student.enrolled_course_ids.remove(from_course_id)
        from_course.enrolled_student_ids.remove(student_id)

        if to_course_id not in student.enrolled_course_ids:
            student.enrolled_course_ids.append(to_course_id)
        if student_id not in to_course.enrolled_student_ids:
            to_course.enrolled_student_ids.append(student_id)

        # Save immediately
        self._save_data()
        return True
