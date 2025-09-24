# PST5

PST5 is a music school management system designed to help administrators manage students, teachers, courses, and daily operations efficiently. The application features a user-friendly interface built with Streamlit and supports registration, check-in, and roster management.

## Features
- Register new students and assign instruments
- Manage teachers and their specialties
- Create and manage courses
- Student check-in and daily roster
- Search for students by name
- Data persistence using JSON files

## Project Structure
```
PST5/
├── main.py                # Streamlit app entry point
├── msms.json              # Data file (if present)
├── app/
│   ├── schedule.py        # Business logic and data management
│   ├── student.py         # StudentUser class
│   ├── teacher.py         # TeacherUser and Course classes
│   └── user.py            # Base User class
├── gui/
│   ├── main_dashboard.py  # Main dashboard and navigation
│   ├── roster_pages.py    # Roster and check-in UI
│   └── student_pages.py   # Student management UI
└── data/
    └── msms.json          # Data storage (created at runtime)
```

## Getting Started
1. **Install dependencies:**
   - Python 3.12+
   - Streamlit
   - pandas
   - (Optional) Anaconda for environment management

2. **Run the app:**
   ```sh
   streamlit run PST5/main.py
   ```

3. **Usage:**
   - Use the sidebar to navigate between student management and roster pages.
   - Register new students, check them in, and manage daily operations.

## Data Storage
- All data is stored in `data/msms.json`.
- The app will create the file and directory if they do not exist.

## Contributing
Pull requests and suggestions are welcome!

## License
MIT License
