import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Students List", page_icon="🎓", layout="centered", initial_sidebar_state="auto")

st.title("Students List")

# spreadsheet_id = "1mJp4L1qLpsBFlq3xkDJmLTebrRfLmN5WkYPAfnSbIHo"
conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="StudentsList", usecols=list(range(10)), ttl=5)  # Read all 10 columns
existing_data = existing_data.dropna(how="all")

with st.form(key="Voters_Form"):
    name = st.text_input(label="Student Name")
    class_ = st.text_input(label="Current Class")
    year = st.text_input(label="Year")
    school_clg = st.text_input(label="Enter Institution Name")
    street_name = st.selectbox("Select Street Name", ["Shakkel Bhai ki galli", "Irshad Bhai","Masjid ki galli","Masjid opposite","PG galli","Jandey ki galli","Mushrraf ki galli","Nala Galli","Misc"])
    waqt = st.selectbox("Select Waqt", ["3-Days", "40-Days", "4-months","NA"])
    ph_no = st.text_input(label="Enter Phone Number")
    dis = st.selectbox("Is the student Discontinued?", ["NA","YES"])
    reason = st.text_input(label="Enter Reason for Discontinuity")

    st.markdown("**required*")
    submit_button = st.form_submit_button(label="Submit Details")

    if submit_button:
        new_data = pd.DataFrame(
            [
                {
                    "Name": name,
                    "Current Class": class_,
                    "Year": year,
                    "Institution": school_clg,
                    "Street Name": street_name,
                    # "Part Number": part_no,
                    "Waqt": waqt,
                    "Phone Number": ph_no,
                    "Discontinued": dis,
                    "Reason": reason,
                }
            ]
        )

        # Append the new data to the existing data
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)

        # Update the worksheet
        conn.update(worksheet="StudentsList", data=updated_data)
        st.success("Student Details Submitted Successfully!!")
