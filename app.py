import streamlit as st
import pandas as pd
import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="My 10-Year Roadmap & Vision Board",
    page_icon="🌟",
    layout="wide"
)

# 2. Initialize Session State for Data Persistence (During Session)
if 'goals' not in st.session_state:
    st.session_state.goals = [
        {"Year": 1, "Category": "💼 Career & Wealth", "Goal": "Save $10k emergency fund & take a certification course.", "Status": "In Progress"},
        {"Year": 3, "Category": "🏡 Lifestyle & Home", "Goal": "Move into a spacious, sunlit apartment.", "Status": "Not Started"},
        {"Year": 5, "Category": "💪 Health & Vitality", "Goal": "Run a half-marathon and maintain a consistent routine.", "Status": "Not Started"},
        {"Year": 10, "Category": "🧠 Personal Growth", "Goal": "Launch a passion-project business and achieve financial freedom.", "Status": "Not Started"}
    ]

# 3. Sidebar - Add New Goals
st.sidebar.header("➕ Add a New Dream")
with st.sidebar.form("goal_form", clear_on_submit=True):
    new_year = st.slider("Target Year (From Now)", min_value=1, max_value=10, value=1)
    new_cat = st.selectbox("Category", ["💼 Career & Wealth", "🏡 Lifestyle & Home", "💪 Health & Vitality", "❤️ Relationships", "🧠 Personal Growth"])
    new_goal = st.text_area("What do you want to achieve/obtain?")
    
    submit = st.form_submit_button("Add to Roadmap")
    if submit and new_goal:
        st.session_state.goals.append({
            "Year": new_year,
            "Category": new_cat,
            "Goal": new_goal,
            "Status": "Not Started"
        })
        st.sidebar.success("Goal added successfully!")

# 4. Main App Interface
st.title("🌟 My 10-Year Vision Board & Roadmap")
st.write("Track your dreams, visualize your timeline, and step into your ideal future.")

# Filter Layout
categories = ["All"] + list(set([g["Category"] for g in st.session_state.goals]))
selected_cat = st.selectbox("🗂️ Filter by Pillar", categories)

# Filter Data
filtered_goals = st.session_state.goals
if selected_cat != "All":
    filtered_goals = [g for g in st.session_state.goals if g["Category"] == selected_cat]

# Convert to DataFrame for visualization sorting
df = pd.DataFrame(filtered_goals)

if not df.empty:
    df = df.sort_values(by="Year")
    
    # 5. Visual Roadmap Timeline Display
    st.subheader("🗺️ Your Interactive Timeline")
    
    # Split into chronological phases
    phase1 = df[df["Year"] <= 3]
    phase2 = df[(df["Year"] > 3) & (df["Year"] <= 6)]
    phase3 = df[df["Year"] > 6]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🚀 Phase 1: The Launch (Years 1-3)")
        if not phase1.empty:
            for idx, row in phase1.iterrows():
                with st.expander(f"Year {row['Year']} - {row['Category']}", expanded=True):
                    st.write(row['Goal'])
                    st.caption(f"Status: {row['Status']}")
        else:
            st.info("No goals added for this phase yet.")
            
    with col2:
        st.markdown("### 🏗️ Phase 2: The Build (Years 4-6)")
        if not phase2.empty:
            for idx, row in phase2.iterrows():
                with st.expander(f"Year {row['Year']} - {row['Category']}", expanded=True):
                    st.write(row['Goal'])
                    st.caption(f"Status: {row['Status']}")
        else:
            st.info("No goals added for this phase yet.")
            
    with col3:
        st.markdown("### 📈 Phase 3: The Scale (Years 7-10)")
        if not phase3.empty:
            for idx, row in phase3.iterrows():
                with st.expander(f"Year {row['Year']} - {row['Category']}", expanded=True):
                    st.write(row['Goal'])
                    st.caption(f"Status: {row['Status']}")
        else:
            st.info("No goals added for this phase yet.")

    # 6. Raw Data View
    st.subheader("📊 All Milestones")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Your roadmap is empty. Use the sidebar to start adding your dreams!")
