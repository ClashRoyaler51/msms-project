from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, name, instrument, lessons=None, user_id=None, id=None, **kwargs):
        # Accept both 'id' and 'user_id' for compatibility
        actual_id = user_id if user_id is not None else id
        super().__init__(actual_id, name)
        self.instrument = instrument
        self.lessons = lessons if lessons is not None else []
        self.enrolled_course_ids = []