import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="HR Management System", layout="wide")

# ---------- Helper Functions ----------

def load_data(file, columns):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=columns)

def save_data(df, file):
    df.to_csv(file, index=False)

# ---------- Load Data ----------

employees = load_data("employees.csv", ["emp_id", "name", "department"])
attendance = load_data("attendance.csv", ["emp_id", "date", "time_in", "time_out"])
leaves = load_data("leaves.csv", ["emp_id", "leave_type", "start_date", "end_date", "status"])
overtime = load_data("overtime.csv", ["emp_id", "date", "hours"])

# ---------- Sidebar ----------

st.sidebar.title("HR Management")
menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Employees",
    "Attendance",
    "Leave Management",
    "Overtime"
])

# ---------- Dashboard ----------

if menu == "Dashboard":
    st.title("📊 HR Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Employees", len(employees))
    col2.metric("Total Attendance Records", len(attendance))
    col3.metric("Pending Leaves", len(leaves[leaves["status"] == "Pending"]))
    col4.metric("Total OT Entries", len(overtime))

# ---------- Employee Management ----------

elif menu == "Employees":
    st.title("👥 Employee Management")

    with st.form("add_employee"):
        emp_id = st.text_input("Employee ID")
        name = st.text_input("Name")
        department = st.text_input("Department")
        submit = st.form_submit_button("Add Employee")

        if submit:
            new_row = pd.DataFrame([[emp_id, name, department]],
                                   columns=employees.columns)
            employees = pd.concat([employees, new_row], ignore_index=True)
            save_data(employees, "employees.csv")
            st.success("Employee added successfully!")

    st.subheader("Employee List")
    st.dataframe(employees)

# ---------- Attendance ----------

elif menu == "Attendance":
    st.title("🕒 Attendance")

    emp_id = st.selectbox("Select Employee", employees["emp_id"] if not employees.empty else [])

    date = st.date_input("Date", datetime.today())
    time_in = st.time_input("Time In")
    time_out = st.time_input("Time Out")

    if st.button("Submit Attendance"):
        new_row = pd.DataFrame([[emp_id, date, time_in, time_out]],
                               columns=attendance.columns)
        attendance = pd.concat([attendance, new_row], ignore_index=True)
        save_data(attendance, "attendance.csv")
        st.success("Attendance recorded!")

    st.subheader("Attendance Records")
    st.dataframe(attendance)

# ---------- Leave Management ----------

elif menu == "Leave Management":
    st.title("🌴 Leave Management")

    emp_id = st.selectbox("Employee", employees["emp_id"] if not employees.empty else [])
    leave_type = st.selectbox("Leave Type", ["Vacation", "Sick", "Emergency"])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Request Leave"):
        new_row = pd.DataFrame([[emp_id, leave_type, start_date, end_date, "Pending"]],
                               columns=leaves.columns)
        leaves = pd.concat([leaves, new_row], ignore_index=True)
        save_data(leaves, "leaves.csv")
        st.success("Leave request submitted!")

    st.subheader("Leave Requests")
    st.dataframe(leaves)

# ---------- Overtime ----------

elif menu == "Overtime":
    st.title("⏳ Overtime Logging")

    emp_id = st.selectbox("Employee", employees["emp_id"] if not employees.empty else [])
    date = st.date_input("Date")
    hours = st.number_input("OT Hours", min_value=0.0)

    if st.button("Submit OT"):
        new_row = pd.DataFrame([[emp_id, date, hours]],
                               columns=overtime.columns)
        overtime = pd.concat([overtime, new_row], ignore_index=True)
        save_data(overtime, "overtime.csv")
        st.success("Overtime logged!")

    st.subheader("Overtime Records")
    st.dataframe(overtime)
