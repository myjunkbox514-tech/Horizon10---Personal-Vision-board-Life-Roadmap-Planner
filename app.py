import streamlit as st
import sqlite3
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="My Vision Boards & Roadmaps",
    page_icon="🌟",
    layout="wide"
)

# 2. Database Initialization Logic
def init_db():
    conn = sqlite3.connect("roadmap_vault.db", check_same_thread=False)
    cursor = conn.cursor()
    # Table for storing different boards
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS boards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)
    # Table for storing goals attached to boards
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_id INTEGER,
            year INTEGER,
            category TEXT,
            goal TEXT,
            status TEXT,
            FOREIGN KEY(board_id) REFERENCES boards(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# 3. Sidebar - Board Management & Board Switching
st.sidebar.title("🗂️ My Vision Boards")

# Feature: Create a brand new board
with st.sidebar.expander("✨ Create New Board / Roadmap", expanded=False):
    new_board_name = st.text_input("Board Name (e.g., Personal, Business 2026)")
    if st.button("Create Board"):
        if new_board_name.strip():
            try:
                cursor.execute("INSERT INTO boards (name) VALUES (?)", (new_board_name.strip(),))
                conn.commit()
                st.success(f"'{new_board_name}' created!")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("A board with this name already exists.")

# Fetch all available boards
cursor.execute("SELECT id, name FROM boards")
all_boards = cursor.fetchall()

if not all_boards:
    # Seed an initial default board if none exist
    cursor.execute("INSERT INTO boards (name) VALUES (?)", ("My Core 10-Year Plan",))
    conn.commit()
    st.rerun()

# Board selection dropdown
board_dict = {name: b_id for b_id, name in all_boards}
selected_board_name = st.sidebar.selectbox("Active Board:", list(board_dict.keys()))
active_board_id = board_dict[selected_board_name]

# Feature: Delete an entire board
with st.sidebar.expander("⚠️ Danger Zone", expanded=False):
    if st.button("Delete This Entire Board"):
        cursor.execute("DELETE FROM boards WHERE id = ?", (active_board_id,))
        # SQLite cascade handling
        cursor.execute("DELETE FROM goals WHERE board_id = ?", (active_board_id,))
        conn.commit()
        st.toast("Board deleted successfully.")
        st.rerun()

st.sidebar.markdown("---")

# 4. Sidebar - Add Milestones to the Active Board
st.sidebar.header("➕ Add a New Dream")
with st.sidebar.form("goal_form", clear_on_submit=True):
    new_year = st.slider("Target Year (From Now)", min_value=1, max_value=10, value=1)
    new_cat = st.selectbox("Category Pillar", ["💼 Career & Wealth", "🏡 Lifestyle & Home", "💪 Health & Vitality", "❤️ Relationships", "🧠 Personal Growth"])
    new_goal = st.text_area("What do you want to achieve/obtain?")
    new_status = st.selectbox("Current Status", ["Not Started", "In Progress", "Achieved"])
    
    submit = st.form_submit_button("Add to Roadmap")
    if submit and new_goal.strip():
        cursor.execute("""
            INSERT INTO goals (board_id, year, category, goal, status) 
            VALUES (?, ?, ?, ?, ?)
        """, (active_board_id, new_year, new_cat, new_goal.strip(), new_status))
        conn.commit()
        st.toast("Added successfully!")
        st.rerun()

# 5. Main App Panel Layout
st.title(f"🌟 {selected_board_name}")
st.write("A completely modular, editable space to map your long-term vision profiles.")

# Global filtering tool
cursor.execute("SELECT DISTINCT category FROM goals WHERE board_id = ?", (active_board_id,))
active_cats = [c[0] for c in cursor.fetchall()]
categories = ["All Active Pillars"] + active_cats
selected_cat = st.selectbox("🗂️ Filter Layout Lens", categories)

# Fetch goals for active board
if selected_cat == "All Active Pillars":
    cursor.execute("SELECT id, year, category, goal, status FROM goals WHERE board_id = ? ORDER BY year ASC", (active_board_id,))
else:
    cursor.execute("SELECT id, year, category, goal, status FROM goals WHERE board_id = ? AND category = ? ORDER BY year ASC", (active_board_id, selected_cat))

goals_data = cursor.fetchall()
df = pd.DataFrame(goals_data, columns=["ID", "Year", "Category", "Goal", "Status"])

# 6. Render Chronological Visual Columns
if not df.empty:
    phase1 = df[df["Year"] <= 3]
    phase2 = df[(df["Year"] > 3) & (df["Year"] <= 6)]
    phase3 = df[df["Year"] > 6]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🚀 Phase 1: The Launch (Years 1-3)")
        for idx, row in phase1.iterrows():
            with st.expander(f"Year {row['Year']} - {row['Category']}", expanded=True):
                st.write(row['Goal'])
                st.caption(f"Status: {row['Status']}")
                # Unique button key using database ID to allow targeting removal
                if st.button("🗑️ Delete Milestone", key=f"del_{row['ID']}"):
                    cursor.execute("DELETE FROM goals WHERE id = ?", (row['ID'],))
                    conn.commit()
                    st.rerun()
                    
    with col2:
        st.markdown("### 🏗️ Phase 2: The Build (Years 4-6)")
        for idx, row in phase2.iterrows():
            with st.expander(f"Year {row['Year']} - {row['Category']}", expanded=True):
                st.write(row['Goal'])
                st.caption(f"Status: {row['Status']}")
                if st.button("🗑️ Delete Milestone", key=f"del_{row['ID']}"):
                    cursor.execute("DELETE FROM goals WHERE id = ?", (row['ID'],))
                    conn.commit()
                    st.rerun()
                    
    with col3:
        st.markdown("### 📈 Phase 3: The Scale (Years 7-10)")
        for idx, row in phase3.iterrows():
            with st.expander(f"Year {row['Year']} - {row['Category']}", expanded=True):
                st.write(row['Goal'])
                st.caption(f"Status: {row['Status']}")
                if st.button("🗑️ Delete Milestone", key=f"del_{row['ID']}"):
                    cursor.execute("DELETE FROM goals WHERE id = ?", (row['ID'],))
                    conn.commit()
                    st.rerun()
else:
    st.info("This roadmap board is currently empty. Use the sidebar menu to populate your goals.")
