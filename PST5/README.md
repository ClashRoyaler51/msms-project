# PST5

PST5 is a music school management system designed to help administrators manage students, teachers, courses, and daily operations efficiently. The application features a user-friendly interface built with Streamlit and supports registration, check-in, and roster management.

## Features
- Register new students and assign instruments
- Manage teachers and their specialties
- Create and manage courses
- Student check-in and daily roster
- Search for students by name
- Data persistence using JSON files

1. **Packages Used:**
   - Streamlit
   - pandas

2. **Run the app:**
   ```
   streamlit run PST5/main.py
   ```

3. **Usage:**
   - Use the sidebar to navigate between student management and roster pages.
   - Register new students, check them in, and manage daily operations.

## Data Storage
- All data is stored in `data/msms.json`.
- The app will create the file and directory if they do not exist.
