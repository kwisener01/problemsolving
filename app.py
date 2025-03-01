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

# Selection of Root Cause Analysis Method
st.subheader("Select Root Cause Analysis Method")
analysis_method = st.selectbox("Choose a method:", ["5 Whys", "Fishbone Diagram", "Pareto Analysis", "Fault Tree Analysis", "Cause and Effect Matrix"])

root_cause_analysis = ""  # Initialize variable
creative_solutions = ""  # Initialize variable

if problem_description:
    if analysis_method == "5 Whys":
        st.subheader("Root Cause Analysis - 5 Whys Conversation")
        why_responses = []
        previous_why = problem_description  # Initialize the first 'Why' with the problem description
        
        for i in range(1, 6):
            question = f"Why {i}? (Based on: {previous_why})"
            guidance_code = f"(Think deeper: Consider process failures, lack of training, systemic issues)"
            response = st.text_area(f"{question} {guidance_code}", key=f"why_{i}")
            why_responses.append(response)
            if not response:
                break
            previous_why = response  # Update for the next iteration
        
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
    
    elif analysis_method == "Fishbone Diagram":
        st.subheader("Root Cause Analysis - Fishbone Diagram")
        categories = ["People", "Process", "Equipment", "Materials", "Environment", "Management"]
        causes = {}
        for category in categories:
            causes[category] = st.text_area(f"Potential causes in {category}:", key=f"fishbone_{category}")
        
        if st.button("Analyze Fishbone", key="fishbone_button"):
            prompt = "Analyze the Fishbone Diagram causes:\nProblem: " + problem_description + "\n" + "\n".join([f"{cat}: {cause}" for cat, cause in causes.items() if cause])
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            root_cause_analysis = response.choices[0].message.content
            st.subheader("Root Cause Analysis Result")
            st.write(root_cause_analysis)
    
    elif analysis_method == "Pareto Analysis":
        st.subheader("Root Cause Analysis - Pareto Analysis")
        causes = st.text_area("List possible causes and their frequency/severity (comma-separated, e.g., 'Cause1: 10, Cause2: 5'):", key="pareto_input")
        
        if st.button("Analyze Pareto", key="pareto_button"):
            prompt = "Analyze the Pareto data and prioritize causes:\nProblem: " + problem_description + "\nData: " + causes
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            root_cause_analysis = response.choices[0].message.content
            st.subheader("Root Cause Analysis Result")
            st.write(root_cause_analysis)
    
    elif analysis_method == "Fault Tree Analysis":
        st.subheader("Root Cause Analysis - Fault Tree Analysis")
        faults = st.text_area("Describe contributing failure events (comma-separated):", key="fault_tree_input")
        
        if st.button("Analyze Fault Tree", key="fault_tree_button"):
            prompt = "Analyze the Fault Tree failure events:\nProblem: " + problem_description + "\nEvents: " + faults
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            root_cause_analysis = response.choices[0].message.content
            st.subheader("Root Cause Analysis Result")
            st.write(root_cause_analysis)
    
    elif analysis_method == "Cause and Effect Matrix":
        st.subheader("Root Cause Analysis - Cause and Effect Matrix")
        effects = st.text_area("List key factors affecting the problem (comma-separated):", key="cause_effect_input")
        
        if st.button("Analyze Cause and Effect Matrix", key="cause_effect_button"):
            prompt = "Analyze the Cause and Effect Matrix:\nProblem: " + problem_description + "\nFactors: " + effects
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            root_cause_analysis = response.choices[0].message.content
            st.subheader("Root Cause Analysis Result")
            st.write(root_cause_analysis)

# Generate Creative Solutions
st.subheader("Generate Creative Solutions")
if st.button("Suggest Solutions", key="suggest_button"):
    if problem_description:
        prompt = "Based on the problem and root cause analysis, provide innovative and practical solutions.\nProblem: " + problem_description + "\n" + root_cause_analysis
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        creative_solutions = response.choices[0].message.content
        st.subheader("Suggested Solutions")
        st.write(creative_solutions)
    else:
        st.warning("Please enter a problem description.")
