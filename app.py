import streamlit as st
import random
import openai
import matplotlib.pyplot as plt
import networkx as nx

# 📌 Streamlit App Title
st.title("🔍 AI-Powered Problem-Solving Chatbot")

st.write("Describe a problem, and I'll guide you through **5 Whys** and **Fishbone Analysis** with AI-powered insights.")

# 📌 Step 1: User Inputs Problem
problem = st.text_area("📝 Describe the problem:")

if problem:
    # 📌 Step 2: 5 Whys Analysis
    st.subheader("❓ 5 Whys Analysis (Root Cause Exploration)")

    why_reasons = []
    for i in range(1, 6):
        why = st.text_input(f"Why {i}? (What caused the previous issue?)", key=f"why_{i}")
        why_reasons.append(why)
        if not why:
            break  # Stop if the user doesn't provide more reasons

    # 📌 Step 3: Fishbone Diagram Categories
    st.subheader("📌 Fishbone Diagram Analysis")
    st.write("Which areas could be contributing to this issue?")

    categories = ["People", "Process", "Equipment", "Materials", "Environment", "Management"]
    selected_categories = st.multiselect("Select categories:", categories)

    # 📌 Step 4: AI-Powered Root Cause Suggestions
    st.subheader("🔍 AI-Suggested Root Causes")
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

    st.write("🔎 **AI-Generated Possible Root Causes:**")
    for cause in selected_causes:
        st.write(f"- {cause}")

    # 📌 Step 5: Fishbone Diagram Generation
    if st.button("📊 Generate Fishbone Diagram"):
        fig, ax = plt.subplots(figsize=(8, 5))
        G = nx.DiGraph()

        # Main problem node
        G.add_node("Problem", color="red")

        # Adding branches for selected categories
        for category in selected_categories:
            G.add_node(category, color="blue")
            G.add_edge("Problem", category)

            # Adding causes under each category
            for cause in root_causes.get(category, []):
                G.add_node(cause, color="green")
                G.add_edge(category, cause)

        pos = nx.spring_layout(G)
        colors = [G.nodes[n]["color"] for n in G.nodes]

        nx.draw(G, pos, with_labels=True, node_color=colors, edge_color="gray", node_size=2000, font_size=10)
        st.pyplot(fig)

    # 📌 Step 6: AI-Powered Solution Plan
    if st.button("📝 Generate AI Solution Plan"):
        st.subheader("✅ AI-Powered Action Plan")
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
            st.write("**AI-Suggested Root Causes & Actions:**")
            for cause in selected_causes:
                action = f"Investigate **{cause}**, train staff, implement SOP improvements, and monitor KPIs."
                st.write(f"- 📌 {cause} ➝ **{action}**")

        st.success("🎯 AI-powered problem-solving complete! Implement changes and track progress.")
