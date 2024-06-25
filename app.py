import streamlit as st
from csv import DictWriter
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Voters-Details", page_icon="👆", layout="centered", initial_sidebar_state="auto")

st.title("Students List")

# spreadsheet_id = "1mJp4L1qLpsBFlq3xkDJmLTebrRfLmN5WkYPAfnSbIHo"
conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="VoterSurvey", usecols=list(range(10)), ttl=5)  # Read all 10 columns
existing_data = existing_data.dropna(how="all")

with st.form(key="Voters_Form"):
    name = st.text_input(label="Student Name")
    class_ = st.text_input(label="Current Class")
    year = st.text_input(label="Year")
    school_clg = st.text_input(label="Enter School Name")
    street_name = st.selectbox("Select Street Name", ["Shakkel Bhai ki galli", "Irshad Bhai","Masjid ki galli","Masjid opposite","PG galli","Jandey ki galli","Mushrraf ki galli","Nala Galli","Misc"])
    part_no = st.text_input(label="Enter Part Number")
    waqt = st.selectbox("Select Waqt", ["3-Days", "40-Days", "4-months","NA"])
    ph_no = st.text_input(label="Enter Phone Number")
    dis = st.selectbox("Select Status", ["YES","NA"])
    reason = st.text_input(label="Enter Reason for Discontinuity")
    # epic_no = st.text_input(label="Enter Epic Number")

    st.markdown("**required*")
    submit_button = st.form_submit_button(label="Submit Details")
    vendor_data = pd.DataFrame()

    if submit_button:
        vendor_data = pd.DataFrame(
            [
                {
                    "Name": name,
                    "Current Class": class_,
                    "Year": year,
                    "Institution": school_clg,
                    "Street Name": street_name,
                    "Waqt": waqt,
                    "Phone Number": ph_no,
                    "Discontinued": dis,
                    "Reason": reason,
                    # "Epic Number": epic_no,
                }
            ]
        )

        # Find the index of the row to be updated (if it exists)
        # update_index = existing_data[
        #     (existing_data["Building Name or Number"] == building_name) & (existing_data["Floor"] == floor)
        # ].index

        # # If the row exists, update the values; otherwise, add a new row
        # if not update_index.empty:
        #     existing_data.loc[update_index, ["Serial Number", "Status", "Epic Number", "Phone Number"]] = vendor_data[
        #         ["Serial Number", "Status", "Epic Number", "Phone Number"]
        #     ].values
        # else:
        #     existing_data = pd.concat([existing_data, vendor_data], ignore_index=True)

        # Update the worksheet
        conn.update(worksheet="VoterSurvey", data=existing_data)
        st.success("Voters Details Submitted Successfully!!")
