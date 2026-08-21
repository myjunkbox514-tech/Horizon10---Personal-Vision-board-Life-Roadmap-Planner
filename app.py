import streamlit as st
import sqlite3
import pandas as pd

# 1. Page Configuration & Futuristic Theme Architecture
st.set_page_config(
    page_title="Horizon10",
    page_icon="📡",
    layout="wide"
)

# Premium High-Tech Global Stylesheet Injection (Ookla Inspired Color Scheme)
st.markdown("""
<style>
    /* Deep Ookla Space Navy Canvas Void */
    .stApp {
        background: #0a0e1a !important;
        color: #e2e8f0 !important;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Neon Highlights & Headers */
    h1 {
        color: #00f0ff !important;
        font-weight: 800 !important;
        letter-spacing: 4px !important;
        text-transform: uppercase !important;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.4) !important;
    }
    h2, h3, h4 {
        color: #00bcff !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    
    /* Cyberpunk Layout Panel Containers */
    .data-card-wrapper {
        background: linear-gradient(145deg, #0d1527, #070b15);
        border: 1px solid #14213d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    
    /* Nested Strategy Blueprint Output Elements */
    .blueprint-node-item {
        background: rgba(0, 188, 255, 0.04);
        border-left: 3px solid #00f0ff;
        padding: 10px 14px;
        margin-top: 8px;
        border-radius: 0 8px 8px 0;
        font-size: 13.5px;
        color: #94a3b8;
        box-shadow: 0 2px 8px rgba(0, 240, 255, 0.05);
    }
    
    /* Native Metric UI Color Overrides for Telemetry look */
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        font-size: 11px !important;
    }
    [data-testid="stMetricValue"] {
        color: #00f0ff !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Database Architectural Core Setup
def init_db():
    conn = sqlite3.connect("horizon10_network_v3.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("CREATE TABLE IF NOT EXISTS boards (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT, board_id INTEGER, 
            year INTEGER, category TEXT, goal TEXT, data_weight INTEGER
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
cursor.execute("PRAGMA foreign_keys = ON")

# 3. Sidebar Network Controller Configuration Console
st.sidebar.markdown("<h2 style='color:#00f0ff; margin-bottom:5px;'>📡 NETWORK HUB</h2>", unsafe_allow_html=True)

cursor.execute("SELECT id, name FROM boards")
all_boards = cursor.fetchall()
if not all_boards:
    cursor.execute("INSERT INTO boards (name) VALUES (?)", ("Core Life Network Vector",))
    conn.commit()
    st.rerun()

board_dict = {name: b_id for b_id, name in all_boards}
selected_board_name = st.sidebar.selectbox("Active Telemetry Data Stream:", list(board_dict.keys()))
active_board_id = board_dict[selected_board_name]

# Form panel to inject tactical project variables into the matrix pipeline
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧬 Inject New Milestone Node")
with st.sidebar.form("add_perk_form", clear_on_submit=True):
    new_year = st.slider("Target Phase Grid Target (Year Horizon)", min_value=1, max_value=10, value=1)
    new_cat = st.selectbox("Strategic Core Life Pillar", ["💼 Career & Wealth", "🏡 Lifestyle & Home", "💪 Health & Vitality", "❤️ Relationships", "🧠 Personal Growth"])
    new_goal = st.text_input("Core Master Target Objective...")
    submit = st.form_submit_button("Transmit Target To Array")
    
    if submit and new_goal.strip():
        data_weight = new_year * 10
        cursor.execute("INSERT INTO goals (board_id, year, category, goal, data_weight) VALUES (?, ?, ?, ?, ?)",
                       (active_board_id, new_year, new_cat, new_goal.strip(), data_weight))
        conn.commit()
        st.rerun()

with st.sidebar.expander("🛠️ Core Network Server Settings", expanded=False):
    new_board = st.text_input("Create Brand New Roadmap Cluster:")
    if st.button("Initialize Network Sector") and new_board.strip():
        try:
            cursor.execute("INSERT INTO boards (name) VALUES (?)", (new_board.strip(),))
            conn.commit()
            st.rerun()
        except sqlite3.IntegrityError:
            st.error("Vector Identifier Already Exists.")
    st.markdown("---")
    if st.button("🗑️ Purge Active Data Stream Completely"):
        cursor.execute("DELETE FROM boards WHERE id = ?", (active_board_id,))
        cursor.execute("DELETE FROM goals WHERE board_id = ?", (active_board_id,))
        conn.commit()
        st.rerun()

# 4. Main App Interface Header Configuration
st.markdown("<h1 style='text-align: center;'>⚡ HORIZON10 ⚡</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #64748b; text-transform: uppercase; letter-spacing: 3px; font-size: 0.85rem; margin-bottom:30px;'>Live Pipeline Vector Array: {selected_board_name}</p>", unsafe_allow_html=True)

cursor.execute("SELECT id, year, category, goal, data_weight FROM goals WHERE board_id = ? ORDER BY year ASC", (active_board_id,))
df = pd.DataFrame(cursor.fetchall(), columns=["ID", "Year", "Category", "Goal", "DataWeight"])

# Group counting properties to feed performance diagnostics panels
growth_count = len(df[df["Category"] == "🧠 Personal Growth"])
health_count = len(df[df["Category"] == "💪 Health & Vitality"])
career_count = len(df[df["Category"] == "💼 Career & Wealth"])

st.markdown("---")
hud_col1, hud_col2, hud_col3 = st.columns(3)
with hud_col1:
    st.metric(label="📊 DATA CAPACITANCE (Intellect & Skills)", value=f"{min(100, (growth_count * 20) + 10)} GB/s")
with hud_col2:
    st.metric(label="🔋 SYSTEM HEALTH (Biometric Vitality Index)", value=f"{min(100, (health_count * 20) + 30)}% EFF")
with hud_col3:
    st.metric(label="🏎️ LATENCY ENGINE (Career Execution Thruput)", value=f"{max(5, 95 - (career_count * 15))} ms")
st.markdown("---")

def render_nested_node_perk(g_id, g_category, g_goal):
    st.markdown(f"<h5 style='margin:0; color:#ffffff;'>{g_category}</h5>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin:2px 0 8px 0; color:#00bcff; font-weight:bold;'>🎯 Target: {g_goal}</p>", unsafe_allow_html=True)
    
    cursor.execute("SELECT id, step_description FROM action_plans WHERE goal_id = ?", (g_id,))
    steps = cursor.fetchall()
    if steps:
        for s_id, s_desc in steps:
            st.markdown(f"<div class='blueprint-node-item'>🚀 {s_desc}</div>", unsafe_allow_html=True)
    else:
        st.caption("No localized telemetry blueprint steps injected.")

# 5. Electric Blue Interactive Constellation Node Array Track Block
st.subheader("🌐 HORIZON CENTRAL NETWORK DIAGRAM")
st.write("Expand a Node Channel below to preview the data packet target logs and actionable procedures.")

map_cols = st.columns(5)
for i in range(1, 6):
    with map_cols[i-1]:
        year_nodes = df[df["Year"] == i]
        node_lbl = f"🔵 {len(year_nodes)} Channels Link" if not year_nodes.empty else "⚫ Offline"
        with st.expander(f"📶 NODE INDEX {i*10} ({node_lbl})", expanded=False):
            if not year_nodes.empty:
                for idx, row in year_nodes.iterrows():
                    render_nested_node_perk(row['ID'], row['Category'], row['Goal'])
                    st.markdown("<hr style='border-color:#14213d; margin:10px 0;'>", unsafe_allow_html=True)
            else:
                st.caption("No operational parameters registered.")

map_cols_2 = st.columns(5)
for i in range(6, 11):
    with map_cols_2[i-6]:
        year_nodes = df[df["Year"] == i]
        node_lbl = f"🔵 {len(year_nodes)} Channels Link" if not year_nodes.empty else "⚫ Offline"
        with st.expander(f"📶 NODE INDEX {i*10} ({node_lbl})", expanded=False):
            if not year_nodes.empty:
                for idx, row in year_nodes.iterrows():
                    render_nested_node_perk(row['ID'], row['Category'], row['Goal'])
                    st.markdown("<hr style='border-color:#14213d; margin:10px 0;'>", unsafe_allow_html=True)
            else:
                st.caption("No operational parameters registered.")

st.markdown("---")

# 6. Central Architect Laboratory (Completely Simplified Action Injection Processing)
st.subheader("🛠️ CENTRAL ARCHITECT LABORATORY: DEPLOY SUBSYSTEM STRATEGY")
if df.empty:
    st.info("Log an active primary target node on the sidebar console parameters panel to initialize this module.")
else:
    st.write("Select any target node pipeline below to append actionable tactical execution plans.")
    goal_mapping = {f"Node {r['Year']*10} [{r['Category']}] - {r['Goal']}": r['ID'] for idx, r in df.iterrows()}
    chosen_goal_str = st.selectbox("Target Array Pipeline Selector Node Target:", list(goal_mapping.keys()))
    chosen_goal_id = goal_mapping[chosen_goal_str]
    
    sub_action_txt = st.text_input("Enter localized blueprint step (e.g. 'Calorie deficit framework tracking via MyFitnessPal')")
    
    if st.button("⚡ Inject Tactical Sub-Step into Stream"):
        if sub_action_txt.strip():
