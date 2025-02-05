import streamlit as st
import random

# 📌 Streamlit App Title
st.title("🔍 Problem-Solving Chatbot (5 Whys & Fishbone Analysis)")

st.write("Describe a problem, and I'll guide you through **5 Whys** and **Fishbone Analysis** to find the root cause.")

# 📌 Step 1: User Inputs Problem
problem = st.text_area("📝 Describe the problem:")

if problem:
    # 📌 Step 2: 5 Whys Analysis
    st.subheader("❓ Let's do the **5 Whys Analysis**")

    why_reasons = []
    for i in range(1, 6):
        why = st.text_input(f"Why {i}? (What caused the previous issue?)", key=f"why_{i}")
        why_reasons.append(why)
        if not why:
            break  # Stop if the user doesn't provide more reasons

    # 📌 Step 3: Fishbone Diagram Categories
    st.subheader("📌 Select Fishbone Diagram Categories")
    st.write("Which areas could be contributing to this issue?")

    categories = ["People", "Process", "Equipment", "Materials", "Environment", "Management"]
    selected_categories = st.multiselect("Select categories:", categories)

    # 📌 Step 4: Suggested Root Causes
    st.subheader("🔍 Suggested Root Causes")
    root_causes = {
        "People": ["Lack of training", "Communication issues", "Employee fatigue"],
        "Process": ["Wrong procedure", "Lack of SOP", "Slow response time"],
        "Equipment": ["Machine breakdown", "Sensor failure", "Poor maintenance"],
        "Materials": ["Defective raw materials", "Wrong part used", "Material contamination"],
        "Environment": ["Humidity issues", "Temperature fluctuation", "Workspace layout"],
        "Management": ["Poor planning", "No feedback system", "Unclear goals"],
    }

    selected_causes = []
    for category in selected_categories:
        selected_causes += random.sample(root_causes[category], 2)

    st.write("🔎 **Possible Root Causes:**")
    for cause in selected_causes:
        st.write(f"- {cause}")

    # 📌 Step 5: Generate Summary & Solution
    if st.button("📝 Generate Solution Plan"):
        st.subheader("✅ Problem Summary & Action Plan")
        st.write(f"**Problem:** {problem}")

        if why_reasons:
            st.write("**5 Whys Analysis:**")
            for i, why in enumerate(why_reasons, start=1):
                if why:
                    st.write(f"🔹 Why {i}: {why}")

        if selected_categories:
            st.write("**Fishbone Analysis Categories:**")
            st.write(", ".join(selected_categories))

        if selected_causes:
            st.write("**Suggested Root Causes & Actions:**")
            for cause in selected_causes:
                st.write(f"- 📌 {cause} ➝ **Investigate & Improve**")

        st.success("🎯 Problem-solving complete! Implement changes and monitor results.")
