# gui/student_pages.py
import streamlit as st
from app.schedule import ScheduleManager
def show_student_management_page(manager):
    """Renders all components for the student management page."""
    # Use the passed-in manager for all operations so new students are immediately available
    st.header("Student Management")

    # --- Search Section (remains the same) ---
    st.subheader("Find a Student")
    # ...
    search_name = st.text_input("Student Name")
    if st.button("Search"):
        results = [s for s in manager.students if search_name.lower() in s.name.lower()]
        if results:
            for student in results:
                st.write(f"ID: {student.id}, Name: {student.name}, Instrument: {student.instrument}")
        else:
            st.warning("No students found with that name.")

    # --- Registration Section (now works correctly) ---
    st.subheader("Register New Student")
    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name")
        reg_instrument = st.text_input("First Instrument")
        submitted = st.form_submit_button("Register Student")
        
        if submitted:
            # This call now works because we implemented the method in PST3.
            # TODO: Add a check for blank name/instrument.
            if reg_name and reg_instrument:
                new_student = manager.register_new_student(reg_name, reg_instrument)
                if new_student:
                    st.success(f"Successfully registered {reg_name}!")
                    # You can use st.balloons() for extra flair.
                else:
                    st.error(f"Could not register student. A teacher for {reg_instrument} might not be available.")
            else:
                st.warning("Please enter both a name and an instrument.")