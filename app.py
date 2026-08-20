import streamlit as st
import sqlite3
import pandas as pd

# 1. Page Configuration & Skyrim Nebula Interface Styling
st.set_page_config(
    page_title="Dovahkiin | Horizon10 Skill Tree",
    page_icon="🌌",
    layout="wide"
)

# Deep cosmic theme styles mimicking the game UI
st.markdown("""
<style>
    /* Dark space void canvas backdrop */
    .stApp {
        background: radial-gradient(circle at center, #111424 0%, #060810 100%);
        color: #e2e8f0;
        font-family: 'Futura', 'Helvetica Neue', sans-serif;
    }
    
    /* Skyrim Skill Header Typography */
    .skyrim-title {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 6px;
        color: #ffffff;
        font-size: 2.5rem;
        text-shadow: 0 0 15px rgba(255,255,255,0.4);
        margin-bottom: 2px;
    }
    .skyrim-subtitle {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 40px;
    }
    
    /* Cosmic Galaxy Constellation Map Row Track */
    .nebula-track {
        display: flex;
        justify-content: space-around;
        align-items: center;
        position: relative;
        padding: 60px 20px;
        background: url('https://unsplash.com') center center no-repeat;
        background-size: cover;
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: inset 0 0 50px #000, 0 15px 35px rgba(0,0,0,0.6);
        border: 2px solid #1e293b;
    }
    
    /* Interactive Shimmering Constellation Nodes */
    .constellation-node {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
    }
    .star-core {
        width: 18px;
        height: 18px;
        background: #ffffff;
        border-radius: 50%;
        border: 3px solid #6366f1;
        box-shadow: 0 0 15px #6366f1, 0 0 30px #8b5cf6;
        transition: all 0.4s ease;
    }
    .constellation-node:hover .star-core {
        transform: scale(1.6);
        background: #818cf8;
        box-shadow: 0 0 25px #ff007f, 0 0 50px #ff007f;
        border-color: #ff007f;
    }
    
    /* Skyrim Description Pop-up Glass Panel bubble */
    .perk-popup {
        visibility: hidden;
        width: 250px;
        background: rgba(10, 15, 30, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #f1f5f9;
        text-align: center;
        padding: 16px;
        border-radius: 8px;
        position: absolute;
        z-index: 100;
        bottom: 160%;
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
    }
    .perk-popup::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -6px;
        border-width: 6px;
        border-style: solid;
        border-color: rgba(10, 15, 30, 0.95) transparent transparent transparent;
    }
    .constellation-node:hover .perk-popup {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
    .node-title {
        font-weight: bold;
        text-transform: uppercase;
        font-size: 13px;
        color: #38bdf8;
        letter-spacing: 1px;
    }
    
    /* Skyrim Skill Attributes HUD Panel Bar */
    .hud-bar-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-bottom: 40px;
    }
    .hud-bar-wrapper {
        width: 260px;
        text-align: center;
    }
    .hud-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
        color: #94a3b8;
    }
    .hud-base-track {
        height: 6px;
        background: #1e293b;
        border-radius: 3px;
        overflow: hidden;
        border: 1px solid #334155;
    }
    .hud-fill {
        height: 100%;
        transition: width 0.5s ease-in-out;
    }
    
    /* Column Deck layout formatting cards */
    .tree-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
    }
    .perk-unlocked-card {
        background: linear-gradient(135deg, #1e1b4b, #0f172a);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 4px solid #6366f1;
    }
</style>
""", unsafe_allow_html=True)

# 2. Database Core Mechanics Setup
def init_db():
    conn = sqlite3.connect("skyrim_blueprint_v2.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS boards (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT, board_id INTEGER, 
            year INTEGER, category TEXT, goal TEXT, level_req INTEGER
        )
    """)
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# 3. Sidebar Configuration Console Layout
st.sidebar.markdown("<h2 style='color:#818cf8; letter-spacing:2px; text-transform:uppercase; font-size:18px;'>⚡ Character Profile</h2>", unsafe_allow_html=True)

cursor.execute("SELECT id, name FROM boards")
all_boards = cursor.fetchall()
if not all_boards:
    cursor.execute("INSERT INTO boards (name) VALUES (?)", ("Main Character Arc Plan",))
    conn.commit()
    st.rerun()

board_dict = {name: b_id for b_id, name in all_boards}
selected_board_name = st.sidebar.selectbox("Active Character Save Sheet:", list(board_dict.keys()))
active_board_id = board_dict[selected_board_name]

# Form panel to generate skill perks matching constellations
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏹 Unlock a New Perk Node")
with st.sidebar.form("add_perk_form", clear_on_submit=True):
    new_year = st.slider("Required Level Milestone (Year Horizon)", min_value=1, max_value=10, value=1)
    new_cat = st.selectbox("Constellation Skill Tree Pillar", ["💼 Career & Wealth", "🏡 Lifestyle & Home", "💪 Health & Vitality", "❤️ Relationships", "🧠 Personal Growth"])
    new_goal = st.text_input("Perk Mastery Description...")
    submit = st.form_submit_button("Engrave Into Constellation")
    
    if submit and new_goal.strip():
        level_req = new_year * 10
        cursor.execute("INSERT INTO goals (board_id, year, category, goal, level_req) VALUES (?, ?, ?, ?, ?)",
                       (active_board_id, new_year, new_cat, new_goal.strip(), level_req))
        conn.commit()
        st.rerun()

# Board Management Settings
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
st.markdown(f"<h1 class='skyrim-title'>{selected_board_name}</h1>", unsafe_allow_html=True)
st.markdown("<p class='skyrim-subtitle'>Level 100 Personal Growth Interface Matrix</p>", unsafe_allow_html=True)

# Pull current profile's inventory rows
cursor.execute("SELECT id, year, category, goal, level_req FROM goals WHERE board_id = ? ORDER BY year ASC", (active_board_id,))
df = pd.DataFrame(cursor.fetchall(), columns=["ID", "Year", "Category", "Goal", "LevelReq"])

# Compute resource bar metrics
growth_count = len(df[df["Category"] == "🧠 Personal Growth"])
health_count = len(df[df["Category"] == "💪 Health & Vitality"])
career_count = len(df[df["Category"] == "💼 Career & Wealth"])

magicka_width = min(100, (growth_count * 20) + 20)
health_width = min(100, (health_count * 20) + 20)
stamina_width = min(100, (career_count * 20) + 20)

st.markdown(f"""
<div class='hud-bar-container'>
    <div class='hud-bar-wrapper'>
        <div class='hud-label'>🧠 Magicka (Growth Focus) {magicka_width}/100</div>
        <div class='hud-base-track'><div class='hud-fill' style='width: {magicka_width}%; background: #3b82f6;'></div></div>
    </div>
    <div class='hud-bar-wrapper'>
        <div class='hud-label'>❤️ Health (Vitality Status) {health_width}/100</div>
        <div class='hud-base-track'><div class='hud-fill' style='width: {health_width}%; background: #ef4444;'></div></div>
    </div>
    <div class='hud-bar-wrapper'>
        <div class='hud-label'>⚡ Stamina (Wealth Engine) {stamina_width}/100</div>
        <div class='hud-base-track'><div class='hud-fill' style='width: {stamina_width}%; background: #10b981;'></div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Build the Interactive Nebula Sky Map Panel Grid
nebula_html = '<div class="nebula-track">'

for step_year in range(1, 11):
    year_nodes = df[df["Year"] == step_year]
    
    if not year_nodes.empty:
        bubble_body = "<br>".join([f"✦ <b>{row['Category'][2:]}:</b> {row['Goal'][:35]}" for idx, row in year_nodes.iterrows()])
        node_glow = "background: #a78bfa; border-color: #ffffff; box-shadow: 0 0 20px #8b5cf6, 0 0 40px #ff007f;"
    else:
        bubble_body = "Locked. No active development parameters registered."
        node_glow = "background: #111424; border-color: #3b82f6;"

    # Appended using clean inline string blocks to prevent parsing crashes
