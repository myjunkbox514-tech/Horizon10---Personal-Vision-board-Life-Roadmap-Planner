import streamlit as st
import sqlite3
import pandas as pd

# 1. Page Configuration & Skyrim Cosmic Theme Injection
st.set_page_config(
    page_title="Dovahkiin | Horizon10 Skill Tree",
    page_icon="🌌",
    layout="wide"
)

# Deep cosmic ambient backdrop using safe, unnested global CSS
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%) !important;
        color: #f8fafc !important;
    }
    h1, h2, h3, h4 {
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    .action-plan-box {
        background-color: rgba(30, 41, 59, 0.5);
        border-left: 3px solid #38bdf8;
        padding: 10px 15px;
        margin-top: 5px;
        border-radius: 0 6px 6px 0;
    }
</style>
""", unsafe_allow_html=True)

# 2. Database Core Setup
def init_db():
    conn = sqlite3.connect("skyrim_blueprint_v5.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS boards (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT, board_id INTEGER, 
            year INTEGER, category TEXT, goal TEXT, level_req INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS action_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT, goal_id INTEGER,
            step_description TEXT,
            FOREIGN KEY(goal_id) REFERENCES goals(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# 3. Sidebar Configuration Console Layout
st.sidebar.markdown("### 🌌 LEVEL UP STATUS")

cursor.execute("SELECT id, name FROM boards")
all_boards = cursor.fetchall()
if not all_boards:
    cursor.execute("INSERT INTO boards (name) VALUES (?)", ("Main Character Arc Plan",))
    conn.commit()
    st.rerun()

board_dict = {name: b_id for b_id, name in all_boards}
selected_board_name = st.sidebar.selectbox("Active Profile Save Sheet:", list(board_dict.keys()))
active_board_id = board_dict[selected_board_name]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏹 Unlock a New Master Perk")
with st.sidebar.form("add_perk_form", clear_on_submit=True):
    new_year = st.slider("Required Level Milestone (Year Horizon)", min_value=1, max_value=10, value=1)
    new_cat = st.selectbox("Constellation Skill Tree Pillar", ["💼 Career & Wealth", "🏡 Lifestyle & Home", "💪 Health & Vitality", "❤️ Relationships", "🧠 Personal Growth"])
    new_goal = st.text_input("End Goal Objective (e.g. Lose Weight)...")
    submit = st.form_submit_button("Engrave Into Constellation")
    
    if submit and new_goal.strip():
        level_req = new_year * 10
        cursor.execute("INSERT INTO goals (board_id, year, category, goal, level_req) VALUES (?, ?, ?, ?, ?)",
                       (active_board_id, new_year, new_cat, new_goal.strip(), level_req))
        conn.commit()
        st.rerun()

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

# 4. Main Character HUD Layout Construction
st.markdown(f"<h1 style='text-align: center; color: #ffffff;'>✨ {selected_board_name} ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; text-transform: uppercase; letter-spacing: 3px; font-size: 0.85rem;'>Level 100 Personal Growth Skill Tree Interface</p>", unsafe_allow_html=True)

cursor.execute("SELECT id, year, category, goal, level_req FROM goals WHERE board_id = ? ORDER BY year ASC", (active_board_id,))
df = pd.DataFrame(cursor.fetchall(), columns=["ID", "Year", "Category", "Goal", "LevelReq"])

growth_count = len(df[df["Category"] == "🧠 Personal Growth"])
health_count = len(df[df["Category"] == "💪 Health & Vitality"])
career_count = len(df[df["Category"] == "💼 Career & Wealth"])

st.markdown("---")
hud_col1, hud_col2, hud_col3 = st.columns(3)
with hud_col1:
    st.metric(label="🧠 MAGICKA (Personal Growth Focus)", value=f"{min(100, (growth_count * 20) + 20)} / 100 Level")
with hud_col2:
    st.metric(label="❤️ HEALTH (Vitality & Wellbeing Status)", value=f"{min(100, (health_count * 20) + 20)} / 100 Level")
with hud_col3:
    st.metric(label="⚡ STAMINA (Wealth Engine & Career)", value=f"{min(100, (career_count * 20) + 20)} / 100 Level")
st.markdown("---")

def render_node_contents(row_id, row_category, row_goal):
    st.markdown(f"#### {row_category}")
    st.markdown(f"**🎯 Target:** {row_goal}")
    cursor.execute("SELECT id, step_description FROM action_plans WHERE goal_id = ?", (row_id,))
    steps = cursor.fetchall()
    if steps:
        st.markdown("<p style='font-size:12px; color:#38bdf8; margin-bottom:2px; text-transform:uppercase;'>📋 Active Execution Blueprint:</p>", unsafe_allow_html=True)
        for s_id, s_desc in steps:
            st.markdown(f"<div class='action-plan-box'>• {s_desc}</div>", unsafe_allow_html=True)
    else:
        st.caption("No custom action plan added to this objective yet.")

# 5. Skyrim Constellation Map Dashboard Track
st.subheader("🌌 THE ACTIVE CONSTELLATION MAP")
st.write("Expand a Level Node star to gaze into your registered dream paths and custom execution steps.")

map_cols = st.columns(5)
for i in range(1, 6):
    with map_cols[i-1]:
        year_nodes = df[df["Year"] == i]
        node_status = f"✨ {len(year_nodes)} Active" if not year_nodes.empty else "⚫ Locked"
        with st.expander(f"⭐ LEVEL {i*10} ({node_status})", expanded=False):
            if not year_nodes.empty:
                for idx, row in year_nodes.iterrows():
                    render_node_contents(row['ID'], row['Category'], row['Goal'])
                    st.markdown("---")
            else:
                st.caption("No development paths active here.")

map_cols_2 = st.columns(5)
for i in range(6, 11):
    with map_cols_2[i-6]:
        year_nodes = df[df["Year"] == i]
        node_status = f"✨ {len(year_nodes)} Active" if not year_nodes.empty else "⚫ Locked"
        with st.expander(f"⭐ LEVEL {i*10} ({node_status})", expanded=False):
            if not year_nodes.empty:
                for idx, row in year_nodes.iterrows():
                    render_node_contents(row['ID'], row['Category'], row['Goal'])
                    st.markdown("---")
            else:
                st.caption("No development paths active here.")

st.markdown("---")

# 6. Interactive Workshop Module
st.subheader("🛠️ THE MASTER WORKSHOP: STRATEGIZE BLUEPRINTS")
if not df.empty:
    st.write("Select any goal below to inject highly specific tracking habits or execution details directly beneath it.")
    goal_options = {f"Year {r['Year']} [{r['Category']}] - {r['Goal']}": r['ID'] for idx, r in df.iterrows()}
    selected_target_str = st.selectbox("Choose Target Goal to Map Out:", list(goal_options.keys()))
    selected_target_id = goal_options[selected_target_str]
    
    with st.form("action_step_form", clear_on_submit=True):
        new_step = st.text_input("What action or habit will you do to accomplish this? (e.g., 'Hit the gym 3x a week')")
        add_step_btn = st.form_submit_button("🔨 Inject Action Step into Goal")
        if add_step_btn and new_step.strip():
            cursor.execute("INSERT INTO action_plans (goal_id, step_description) VALUES (?, ?)", (selected_target_id, new_step.strip()))
            conn.commit()
            st.toast("Action plan step registered!")
            st.rerun()
else:
    st.info("Add an initial goal from the sidebar to open the Action Strategy Workshop module.")

st.markdown("---")

# 7. Structured Phase Tree Column View Panel
st.subheader("📜 ACTIVE PERK TREE LOGS")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🚀 THE NOVICE TREE\n*Level 10 - 30 Perks (Years 1-3)*")
    p1_nodes = df[df["Year"] <= 3]
    if not p1_nodes.empty:
        for idx, row in p1_nodes.iterrows():
            with st.container(border=True):
                render_node_contents(row['ID'], row['Category'], row['Goal'])
                # Safe operational line structure layout
                if st.button("🚫 Revoke Perk", key=f"del_{row['ID']}"):
                    cursor.execute("DELETE FROM goals WHERE id = ?", (row['ID'],))
                    conn.commit()
                    st.rerun()
    else:
        st.caption("No novice traits active.")

with col2:
    st.markdown("#### 🏗️ THE ADEPT TREE\n*Level 40 - 60 Perks (Years 4-6)*")
    p2_nodes = df[(df["Year"] > 3) & (df["Year"] <= 6)]
    if not p2_nodes.empty:
        for idx, row in p2_nodes.iterrows():
            with st.container(border=True):
                render_node_contents(row['ID'], row['Category'], row['Goal'])
                if st.button("🚫 Revoke Perk", key=f"del_{row['ID']}"):
                    cursor.execute("DELETE FROM goals WHERE id = ?", (row['ID'],))
                    conn.commit()
                    st.rerun()
    else:
        st.caption("No adept traits active.")

with col3:
    st.markdown("#### 📈 THE MASTER TREE\n*Level 70 - 100 Perks (Years 7-10)*")
    p3_nodes = df[df["Year"] > 6]
    if not p3_nodes.empty:
        for idx, row in p3_nodes.iterrows():
            with st.container(border=True):
                render_node_contents(row['ID'], row['Category'], row['Goal'])
