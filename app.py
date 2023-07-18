import streamlit as st
import requests
import plotly.express as px
import pandas as pd

# Backend API URL
API_URL = "http://localhost:8000"

# Fetch samples data from the backend API
response = requests.get(f"{API_URL}/samples")
if response.status_code != 200:
    st.error("Failed to fetch samples from the API")
    st.stop()

samples = response.json()
cities = [sample["city"] for sample in samples if "city" in sample]
counts = [sample["count"] for sample in samples if "count" in sample]

df = pd.DataFrame(samples)

# Create bar chart using Plotly Express
fig = px.bar(data_frame=df, x="city", y="count", title="Sample Count by Cities")

# Streamlit app
st.title("Sample Count by Cities")
st.plotly_chart(fig)

# Display the data in a table on the sidebar
st.sidebar.subheader("Sample Data")
st.sidebar.table(df)

# Add Sample Form on the sidebar
with st.sidebar.form("add_form"):
    st.subheader("Add Sample")
    add_city = st.text_input("City", key="add_city")
    add_count = st.number_input("Count", min_value=0, step=1, key="add_count")
    add_button = st.form_submit_button("Add")

    # Handle Add Sample form submission
    if add_button:
        add_params = {"city": add_city, "count": add_count}
        add_response = requests.post(f"{API_URL}/samples", params=add_params)
        if add_response.status_code == 200:
            st.success("Sample added successfully")
            samples.append(add_response.json())
            cities, counts = zip(*[(sample["city"], sample["count"]) for sample in samples])
            fig.data[0].x = cities
            fig.data[0].y = counts
        else:
            st.error("Failed to add sample")

# Update Sample Form on the sidebar
with st.sidebar.form("update_form"):
    st.subheader("Update Sample")
    update_id = st.number_input("Sample ID", min_value=1, step=1, key="update_id")
    update_city = st.text_input("City", key="update_city")
    update_count = st.number_input("Count", min_value=0, step=1, key="update_count")
    update_button = st.form_submit_button("Update")

    # Handle Update Sample form submission
    if update_button:
        update_params = {"city": update_city, "count": update_count}
        update_response = requests.put(f"{API_URL}/samples/{update_id}", params=update_params)
        if update_response.status_code == 200:
            st.success("Sample updated successfully")
            index = next((i for i, sample in enumerate(samples) if sample["id"] == update_id), None)
            if index is not None:
                samples[index].update(update_params)
                cities, counts = zip(*[(sample["city"], sample["count"]) for sample in samples])
                fig.data[0].x = cities
                fig.data[0].y = counts
        else:
            st.error("Failed to update sample")

# Delete Sample Form on the sidebar
with st.sidebar.form("delete_form"):
    st.subheader("Delete Sample")
    delete_id = st.number_input("Sample ID", min_value=1, step=1, key="delete_id")
    delete_button = st.form_submit_button("Delete")

    # Handle Delete Sample form submission
    if delete_button:
        delete_response = requests.delete(f"{API_URL}/samples/{delete_id}")
        if delete_response.status_code == 200:
            st.success("Sample deleted successfully")
            index = next((i for i, sample in enumerate(samples) if sample["id"] == delete_id), None)
            if index is not None:
                del samples[index]
                cities, counts = zip(*[(sample["city"], sample["count"]) for sample in samples])
                fig.data[0].x = cities
                fig.data[0].y = counts




