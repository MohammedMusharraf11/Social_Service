import streamlit as st
from csv import DictWriter
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Voters-Details", page_icon="👆", layout="centered", initial_sidebar_state="auto")

st.title("Survey Of Voters")
id="1mJp4L1qLpsBFlq3xkDJmLTebrRfLmN5WkYPAfnSbIHo"
conn = st.connection("gsheets", type=GSheetsConnection, spreadsheet_id=id)

existing_data = conn.read(worksheet="Data", usecols=list(range(10)), ttl=5)  # Read all 10 columns
existing_data = existing_data.dropna(how="all")

with st.form(key="Voters_Form"):
    building_name = st.text_input(label="Building Name/No")
    floor = st.text_input(label="Floor No")
    voters_name = st.text_input(label="Voters Name")
    no_of_voters = st.text_input(label="Total No of Voters")
    part_no = st.text_input(label="Enter Part Number")
    part_name = st.selectbox("Select Part Name", ["ILMA School", "Newton School"," "])
    status = st.selectbox("Select Status", ["Active", "Inactive"])
    ph_no = st.text_input(label="Enter Phone Number")
    serial_no = st.text_input(label="Enter Serial Number")
    epic_no = st.text_input(label="Enter Epic Number")

    st.markdown("**required*")
    submit_button = st.form_submit_button(label="Submit Details")
    vendor_data = pd.DataFrame()

    if submit_button:
        vendor_data = pd.DataFrame(
            [
                {
                    "Building Name or Number": building_name,
                    "Floor": floor,
                    "Total No of Voters": no_of_voters,
                    "Voters Name": voters_name,
                    "Part No": part_no,
                    "Part Name": part_name,
                    "Serial Number": serial_no,
                    "Status": status,
                    "Epic Number": epic_no,
                    "Phone Number": ph_no,
                }
            ]
        )

        # Find the index of the row to be updated (if it exists)
        update_index = existing_data[
            (existing_data["Building Name or Number"] == building_name) & (existing_data["Floor"] == floor)
        ].index

        # If the row exists, update the values; otherwise, add a new row
        if not update_index.empty:
            existing_data.loc[update_index, ["Serial Number", "Status", "Epic Number", "Phone Number"]] = vendor_data[
                ["Serial Number", "Status", "Epic Number", "Phone Number"]
            ].values
        else:
            existing_data = pd.concat([existing_data, vendor_data], ignore_index=True)

        # Update the worksheet
        conn.update(worksheet="Data", data=existing_data)
        st.success("Voters Details Submitted Successfully!!")
