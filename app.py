import streamlit as st
import openai
import pandas as pd
import json

# Set OpenAI API Key
client = openai.OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

# Initialize Streamlit App
st.title("Creative Problem-Solving & Root Cause Analysis Tool")

# User Inputs
st.subheader("Describe the Problem")
problem_description = st.text_area("Enter the problem you are facing:", key="problem_input")

st.subheader("Root Cause Analysis - 5 Whys Conversation")

if problem_description:
    why_responses = []
    for i in range(1, 6):
        question = f"Why {i}?"
        guidance_code = f"(Think deeper: Consider process failures, lack of training, systemic issues)"
        response = st.text_area(f"{question} {guidance_code}", key=f"why_{i}")
        why_responses.append(response)
        if not response:
            break

    if st.button("Analyze Root Cause", key="analyze_button"):
        filled_why_responses = [resp for resp in why_responses if resp]
        if filled_why_responses:
            prompt = "Analyze the 5 Whys responses:\nProblem: " + problem_description + "\n" + "\n".join([f"{i+1}. {resp}" for i, resp in enumerate(filled_why_responses)])
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            root_cause_analysis = response.choices[0].message.content
            st.subheader("Root Cause Analysis Result")
            st.write(root_cause_analysis)
        else:
            st.warning("Please answer at least one Why question.")

# Generate Creative Solutions
st.subheader("Generate Creative Solutions")
if st.button("Suggest Solutions", key="suggest_button"):
    if problem_description:
        prompt = "Based on the problem and 5 Whys analysis, provide innovative and practical solutions.\nProblem: " + problem_description + "\n" + "\n".join([f"{i+1}. {resp}" for i, resp in enumerate(why_responses) if resp])
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
            "5 Whys": why_responses,
            "Root Cause Analysis": root_cause_analysis,
            "Suggested Solutions": creative_solutions
        }
        with open(f"{save_name}.json", "w") as file:
            json.dump(results, file)
        st.success(f"Results saved as {save_name}.json")
    else:
        st.warning("Please enter a file name.")
