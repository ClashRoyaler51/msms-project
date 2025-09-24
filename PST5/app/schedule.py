import json
from app.student import StudentUser
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.next_lesson_id = 1
        self._load_data()

    def register_new_student(self, name, instrument):
        """Registers a new student and adds them to the students list."""
        
        new_student = StudentUser(name=name, instrument=instrument, lessons=[])
        self.students.append(new_student)
        self._save_data()
        return new_student

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # The logic here remains the same, but the source of the Course class has changed.
                # TODO: For each dictionary in data['students'], create a StudentUser object and append to self.students.
                for student_data in data.get('students', []):
                    self.students.append(StudentUser(**student_data))
                # TODO: Do the same for teachers (creating TeacherUser objects).
                for teacher_data in data.get('teachers', []):
                    self.teachers.append(TeacherUser(**teacher_data))
                # TODO: Do the same for courses (creating Course objects).
                for course_data in data.get('courses', []):
                    self.courses.append(Course(**course_data))
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # The logic here remains the same.
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
            'students': [student.__dict__ for student in self.students],
            'teachers': [teacher.__dict__ for teacher in self.teachers],
            'courses': [course.__dict__ for course in self.courses]
        }
        with open(self.data_path, 'w') as f:
        # Convert self.students, self.teachers, and self.courses into lists of dictionaries.
        # Write the result to the JSON file.
            json.dump(data_to_save, f, indent=4)     