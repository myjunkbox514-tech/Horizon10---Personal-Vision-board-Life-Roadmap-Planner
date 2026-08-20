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
    /* Clean Minimalist Background & Typography */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Interactive Hover Timeline styles */
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
    
    /* Elegant Pop-up Bubble UI (Transparent Glassmorphism) */
    .timeline-bubble {
        visibility: hidden;
        width: 220px;
        background: rgba(17, 24, 39, 0.85);
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
    
    /* Modern Phase Column Cards */
    .phase-card {
        background: #111827;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #1f2937;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        min-height: 400px;
    }
    .goal-item {
        background: #1f2937;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 12px;
        border-left: 4px solid #8b5cf6;
    }
</style>
""", unsafe_allow_html=True)

# 2. Database Core Setup
def init_db():
    conn = sqlite3.connect("roadmap_clean.db", check_same_thread=False)
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

# 3. Sidebar Profile Management
st.sidebar.markdown("<h2 style='color:#3b82f6; margin-bottom:0;'>🎨 Studio Canvas</h2>", unsafe_allow_html=True)
st.sidebar.write("Switch layouts or create separate dynamic maps instantly.")

# Fetch / Seed Boards
cursor.execute("SELECT id, name FROM boards")
all_boards = cursor.fetchall()
if not all_boards:
    cursor.execute("INSERT INTO boards (name) VALUES (?)", ("My Vision Core Blueprint",))
    conn.commit()
    st.rerun()

board_dict = {name: b_id for b_id, name in all_boards}
selected_board_name = st.sidebar.selectbox("Current Active Map:", list(board_dict.keys()))
active_board_id = board_dict[selected_board_name]

# Modular Sidebar Data Entry Form
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

# Board Management Tools
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

# 4. Main App Interface Header
st.markdown(f"<h1 style='text-align: center; margin-bottom: 5px; color:#ffffff;'>✨ {selected_board_name}</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; margin-bottom: 40px;'>Hover over timeline nodes below to peek into future targets instantly.</p>", unsafe_allow_html=True)

# Fetch current target data frame
cursor.execute("SELECT id, year, category, goal FROM goals WHERE board_id = ? ORDER BY year ASC", (active_board_id,))
goals_list = cursor.fetchall()
df = pd.DataFrame(goals_list, columns=["ID", "Year", "Category", "Goal"])

# 5. Interactive Floating-Bubble Map Generator (HTML/CSS Hybrid)
timeline_html = '<div class="timeline-container"><div class="timeline-line"></div>'

for target_year in range(1, 11):
    # Pull milestones matching the specific year segment
    year_milestones = df[df["Year"] == target_year]
    
    if not year_milestones.empty:
        # Build transparent bubble description block string
        bubble_content = "<br>".join([f"<b>{row['Category']}:</b> {row['Goal'][:40]}..." for _, row in year_milestones.iterrows()])
        dot_style = "border-color: #ec4899; box-shadow: 0 0 15px #ec4899;" # Glow pink if populated
    else:
        bubble_content = "No milestones configured for this calendar track yet."
        dot_style = "border-color: #3b82f6;"

    timeline_html += f"""
    <div class="timeline-node">
        <div class="timeline-bubble">
            <span style='color:#3b82f6; font-weight:bold; font-size:15px;'>📅 Year {target_year} Forecast</span><br>
            <hr style='border-color:rgba(255,255,255,0.1); margin:6px 0;'>
            <span style='font-size:12px; color:#e5e7eb; display:block; text-align:left;'>{bubble_content}</span>
        </div>
        <div class="timeline-dot" style="{dot_style}"></div>
        <div class="timeline-label">Yr {target_year}</div>
    </div>
    """
timeline_html += '</div>'
st.markdown(timeline_html, unsafe_allow_html=True)

# 6. Column-Phase Macro Layout
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='phase-card'><h3>🚀 Phase 1: Near Horizon</h3><p style='color:#6b7280; font-size:13px;'>Years 1 - 3 • Core Foundations</p><hr style='border-color:#1f2937;'>", unsafe_allow_html=True)
    p1_df = df[df["Year"] <= 3]
    if not p1_df.empty:
        for _, row in p1_df.iterrows():
            st.markdown(f"<div class='goal-item'><b>Year {row['Year']} — {row['Category']}</b><br><span style='color:#d1d5db; font-size:14px;'>{row['Goal']}</span></div>", unsafe_allow_html=True)
            if st.button("🗑️ Drop", key=f"del_{row['ID']}", help="Remove from database"):
                cursor.execute("DELETE FROM goals WHERE id = ?", (row['ID'],))
                conn.commit()
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='phase-card'><h3>🏗️ Phase 2: Mid Horizon</h3><p style='color:#6b7280; font-size:13px;'>Years 4 - 6 • Transition Shifts</p><hr style='border-color:#1f2937;'>", unsafe_allow_html=True)
    p2_df = df[(df["Year"] > 3) & (df["Year"] <= 6)]
    if not p2_df.empty:
        for _, row in p2_df.iterrows():
            st.markdown(f"<div class='goal-item' style='border-left-color:#3b82f6;'><b>Year {row['Year']} — {row['Category']}</b><br><span style='color:#d1d5db; font-size:14px;'>{row['Goal']}</span></div>", unsafe_allow_html=True)
            if st.button("🗑️ Drop", key=f"del_{row['ID']}", help="Remove from database"):
                cursor.execute("DELETE FROM goals WHERE id = ?", (row['ID'],))
                conn.commit()
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='phase-card'><h3>📈 Phase 3: Far Horizon</h3><p style='color:#6b7280; font-size:13px;'>Years 7 - 10 • Compounding Scalability</p><hr style='border-color:#1f2937;'>", unsafe_allow_html=True)
    p3_df = df[df["Year"] > 6]
