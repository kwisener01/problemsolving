import streamlit as st
import openai
import pandas as pd
import json

# Set OpenAI API Key
client = openai.OpenAI(api_key="your_openai_api_key")

# Initialize Streamlit App
st.title("Creative Problem-Solving & Root Cause Analysis Tool")

# User Inputs
st.subheader("Describe the Problem")
problem_description = st.text_area("Enter the problem you are facing:", key="problem_input")

st.subheader("Root Cause Analysis")
selected_method = st.selectbox("Select a method for root cause analysis:", ["5 Whys", "Fishbone Diagram", "Pareto Analysis"], key="method_selection")

if st.button("Analyze Root Cause", key="analyze_button"):
    if problem_description:
        prompt = f"Perform a {selected_method} analysis on the following problem: {problem_description}."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        root_cause_analysis = response.choices[0].message.content
        st.subheader("Root Cause Analysis Result")
        st.write(root_cause_analysis)
    else:
        st.warning("Please enter a problem description.")

# Generate Creative Solutions
st.subheader("Generate Creative Solutions")
if st.button("Suggest Solutions", key="suggest_button"):
    if problem_description:
        prompt = f"Provide innovative solutions for the following problem: {problem_description}."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        creative_solutions = response.choices[0].message.content
        st.subheader("Suggested Solutions")
        st.write(creative_solutions)
    else:
        st.warning("Please enter a problem description.")

# Save Results
st.subheader("Save Analysis")
save_name = st.text_input("Enter a file name to save results:", key="save_name_input")
if st.button("Save", key="save_button"):
    if save_name:
        results = {
            "Problem": problem_description,
            "Root Cause Analysis": root_cause_analysis,
            "Suggested Solutions": creative_solutions
        }
        with open(f"{save_name}.json", "w") as file:
            json.dump(results, file)
        st.success(f"Results saved as {save_name}.json")
    else:
        st.warning("Please enter a file name.")
