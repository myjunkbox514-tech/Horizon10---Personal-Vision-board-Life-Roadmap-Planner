import streamlit as st
import sqlite3
import pandas as pd

# 1. Page Configuration & Custom Theme Styles Injection
st.set_page_config(
    page_title="Horizon10 | Vision Studio",
    page_icon="✨",
    layout="wide"
)

# Custom UI/UX Styles injection
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    .timeline-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        padding: 40px 20px;
        background: linear-gradient(145deg, #111827, #1f2937);
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border: 1px solid #374151;
    }
    .timeline-line {
        position: absolute;
        top: 50%;
        left: 5%;
        right: 5%;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        z-index: 1;
        transform: translateY(-50%);
    }
    .timeline-node {
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
    }
    .timeline-dot {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background-color: #111827;
        border: 4px solid #3b82f6;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 12px rgba(59, 130, 246, 0.5);
    }
    .timeline-node:hover .timeline-dot {
        transform: scale(1.4);
        background-color: #3b82f6;
        box-shadow: 0 0 20px #3b82f6, 0 0 40px #8b5cf6;
    }
    .timeline-bubble {
        visibility: hidden;
        width: 220px;
        background: rgba(17, 24, 39, 0.95);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        color: #fff;
        text-align: center;
        border-radius: 12px;
        padding: 12px;
        position: absolute;
        z-index: 10;
        bottom: 150%;
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        opacity: 0;
        transition: opacity 0.3s ease, transform 0.3s ease, visibility 0.3s;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .timeline-node:hover .timeline-bubble {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
    .timeline-label {
        margin-top: 8px;
        font-weight: 600;
        font-size: 14px;
        color: #9ca3af;
    }
    .phase-card {
        background: #111827;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #1f2937;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        min-height: 250px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Database Setup
def init_db():
    conn = sqlite3.connect("roadmap_v3.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS boards (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT, board_id INTEGER, 
            year INTEGER, category TEXT, goal TEXT, status TEXT
        )
    """)
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# 3. Sidebar Board Selection
st.sidebar.markdown("<h2 style='color:#3b82f6; margin-bottom:0;'>🎨 Studio Canvas</h2>", unsafe_allow_html=True)

cursor.execute("SELECT id, name FROM boards")
all_boards = cursor.fetchall()
if not all_boards:
    cursor.execute("INSERT INTO boards (name) VALUES (?)", ("My Vision Core Blueprint",))
    conn.commit()
    st.rerun()

board_dict = {name: b_id for b_id, name in all_boards}
selected_board_name = st.sidebar.selectbox("Current Active Map:", list(board_dict.keys()))
active_board_id = board_dict[selected_board_name]

# 4. Sidebar Form: Add New Milestones
st.sidebar.markdown("---")
st.sidebar.markdown("### ➕ Drop a New Milestone")
with st.sidebar.form("add_goal_form", clear_on_submit=True):
    new_year = st.slider("Target Horizon Year", min_value=1, max_value=10, value=1)
    new_cat = st.selectbox("Life Pillar Focus", ["💼 Career & Wealth", "🏡 Lifestyle & Home", "💪 Health & Vitality", "❤️ Relationships", "🧠 Personal Growth"])
    new_goal = st.text_input("Enter your dream brief...")
    submit = st.form_submit_button("Manifest Onto Board")
    
    if submit and new_goal.strip():
        cursor.execute("INSERT INTO goals (board_id, year, category, goal, status) VALUES (?, ?, ?, ?, ?)",
                       (active_board_id, new_year, new_cat, new_goal.strip(), "In Progress"))
        conn.commit()
        st.rerun()

# Sidebar Settings: Creation & Wiping
with st.sidebar.expander("🛠️ Board Studio Settings", expanded=False):
    new_board = st.text_input("Create Brand New Roadmap:")
    if st.button("Initialize New Canvas") and new_board.strip():
        try:
            cursor.execute("INSERT INTO boards (name) VALUES (?)", (new_board.strip(),))
            conn.commit()
            st.rerun()
        except sqlite3.IntegrityError:
            st.error("Name taken!")
    st.markdown("---")
    if st.button("🗑️ Wipe Active Canvas Completely"):
        cursor.execute("DELETE FROM boards WHERE id = ?", (active_board_id,))
        cursor.execute("DELETE FROM goals WHERE board_id = ?", (active_board_id,))
        conn.commit()
        st.rerun()

# 5. Main App Header Interface
st.markdown(f"<h1 style='text-align: center; margin-bottom: 5px; color:#ffffff;'>✨ {selected_board_name}</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; margin-bottom: 40px;'>Hover over timeline nodes below to peek into future targets instantly.</p>", unsafe_allow_html=True)

# Fetch Goal Data
cursor.execute("SELECT id, year, category, goal FROM goals WHERE board_id = ? ORDER BY year ASC", (active_board_id,))
goals_list = cursor.fetchall()
df = pd.DataFrame(goals_list, columns=["ID", "Year", "Category", "Goal"])

# 6. Interactive Floating-Bubble Map Generator
timeline_html = '<div class="timeline-container"><div class="timeline-line"></div>'
for target_year in range(1, 11):
    year_milestones = df[df["Year"] == target_year]
    if not year_milestones.empty:
        bubble_content = "<br>".join([f"<b>{row['Category']}:</b> {row['Goal'][:40]}..." for idx, row in year_milestones.iterrows()])
        dot_style = "border-color: #ec4899; box-shadow: 0 0 15px #ec4899;"
    else:
        bubble_content = "No milestones configured for this calendar track yet."
        dot_style = "border-color: #3b82f6;"

    timeline_html += f"""<div class="timeline-node"><div class="timeline-bubble"><span style='color:#3b82f6; font-weight:bold; font-size:15px;'>📅 Year {target_year} Forecast</span><br><hr style='border-color:rgba(255,255,255,0.1); margin:6px 0;'><span style='font-size:12px; color:#e5e7eb; display:block; text-align:left;'>{bubble_content}</span></div><div class="timeline-dot" style="{dot_style}"></div><div class="timeline-label">Yr {target_year}</div></div>"""
timeline_html += '</div>'

st.markdown(timeline_html, unsafe_allow_html=True)

# 7. Clean Macro Data Management Desk
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='phase-card'><h3>🚀 Phase 1: Near Horizon</h3><p style='color:#6b7280; font-size:13px;'>Years 1 - 3 • Core Foundations</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='phase-card'><h3>🏗️ Phase 2: Mid Horizon</h3><p style='color:#6b7280; font-size:13px;'>Years 4 - 6 • Transition Shifts</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='phase-card'><h3>📈 Phase 3: Far Horizon</h3><p style='color:#6b7280; font-size:13px;'>Years 7 - 10 • Compounding Results</p></div>", unsafe_allow_html=True)

st.markdown("### 📊 Active Milestones Registry")
if not df.empty:
    for idx, row in df.iterrows():
        r_col1, r_col2, r_col3 = st.columns([2, 6, 2])
        r_col1.write(f"**Year {row['Year']}** ({row['Category']})")
        r_col2.info(row['Goal'])
        if r_col3.button("🗑️ Drop", key=f"del_{row['ID']}"):
            cursor.execute("DELETE FROM goals WHERE id = ?", (row['ID'],))
            conn.commit()
            st.rerun()
else:
    st.info("Your active vision canvas is completely blank. Drop a milestone via the sidebar menu to begin tracking.")
