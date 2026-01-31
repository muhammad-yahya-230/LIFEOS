import streamlit as st
from datetime import datetime, timedelta
from src.core.planner import create_or_update_plan, get_daily_plan
from src.core.execution import log_execution, get_execution, calculate_day_score
from src.analytics.dashboard import get_dashboard_metrics
from src.utils.date_utils import get_today_str

# UI IMPORTS
from src.ui.styles import apply_custom_styles
from src.ui.components import render_sidebar, render_card

# Configure Page
st.set_page_config(
    page_title="LifeOS",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS
apply_custom_styles()

# Navigation
page = render_sidebar()

# Command Bar (Global)
with st.sidebar:
    st.divider()
    cmd_input = st.text_input("💻 Command Bar", key="cmd_input", placeholder="$ 20 lunch | gym squat 100 5")
    if cmd_input:
        from src.systems.command_parser import parse_and_execute
        res = parse_and_execute(cmd_input)
        if "Unknown" not in res:
             st.success(res)
        else:
             st.error(res)

# Quick Log (Sidebar) - Collapsed by default as Command Bar is faster
with st.sidebar:
    with st.expander("⚡ Quick Log", expanded=False):
        ql_type = st.selectbox("Type", ["Expense", "Note", "Gym Set"])
        if ql_type == "Expense":
            from src.finance.manager import add_transaction, get_categories
            q_amt = st.number_input("Amount", key="ql_amt")
            q_cat = st.selectbox("Category", get_categories(), key="ql_cat")
            q_desc = st.text_input("Desc", key="ql_desc")
            if st.button("Add"):
                add_transaction(datetime.now().strftime("%Y-%m-%d"), q_amt, "Expense", q_cat, q_desc)
                st.success("Saved!")
        elif ql_type == "Note":
            from src.knowledge.notes import add_note
            q_title = st.text_input("Title", key="ql_title")
            q_note = st.text_area("Note", key="ql_note")
            if st.button("Save Note"):
                add_note(q_title, q_note, "quick-log")
                st.success("Note Saved!")
        elif ql_type == "Gym Set":
             st.caption("Go to Gym tab for full logger")

    st.divider()
    date_sel = st.date_input("Date Access", datetime.now())
    date_str = date_sel.strftime("%Y-%m-%d")

# Main Content
st.markdown(f"## {page}")

if page == "Dashboard":
    # Gamification Header
    from src.gamification.engine import calculate_rpg_stats
    rpg = calculate_rpg_stats()
    
    st.markdown(f"""
    <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin:0; color: #FF4B4B;">Level {rpg['level']}</h2>
            <div style="color: #AAA;">{rpg['total_xp']} XP</div>
        </div>
        <div style="background-color: #333; height: 10px; border-radius: 5px; margin-top: 10px;">
            <div style="background-color: #FF4B4B; height: 100%; width: {rpg['xp_progress']*100}%; border-radius: 5px;"></div>
        </div>
        <div style="display: flex; justify-content: space-around; margin-top: 15px; color: #DDD; font-size: 0.9rem;">
            <div>💪 STR: {rpg['attributes']['STR']}</div>
            <div>🧠 INT: {rpg['attributes']['INT']}</div>
            <div>🦉 WIS: {rpg['attributes']['WIS']}</div>
            <div>🎯 DIS: {rpg['attributes']['DIS']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    metrics = get_dashboard_metrics()
    from src.core.sleep import calculate_sleep_debt_days
    from src.core.execution import calculate_day_score
    
    sleep_debt = calculate_sleep_debt_days()
    day_score = calculate_day_score(date_str)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_card("Weekly Study", f"{metrics['study_total']}h")
    with col2:
        render_card("Gym Sessions", metrics['gym_sessions'])
    with col3:
        render_card("Day Score", f"{day_score}%")
    with col4:
        render_card("Sleep Debt", f"{sleep_debt}h", delta="Careful" if sleep_debt > 2 else "Good", color="inverse" if sleep_debt > 2 else "normal")
    
    st.subheader("Weekly Trends")
    # Placeholder
    st.bar_chart({"Study": [3, 4, 3, 5, 2, 0, 0], "Gym": [1, 0, 1, 0, 1, 0, 0]})

elif page == "Planner":
    # Load existing
    plan = get_daily_plan(date_str) or {}
    
    with st.container():
        st.caption(f"Planning for: {date_str}")
        with st.form("planning_form"):
            c1, c2 = st.columns(2)
            wake = c1.time_input("Wake Time", value=datetime.strptime(plan.get("wake_time_planned", "07:00"), "%H:%M").time())
            sleep = c2.time_input("Sleep Time", value=datetime.strptime(plan.get("sleep_time_planned", "23:00"), "%H:%M").time())
            
            study = st.number_input("Study Hours Target", min_value=0.0, step=0.5, value=float(plan.get("study_hours_planned", 0.0)))
            
            routine = st.checkbox("Morning Routine", value=str(plan.get("morning_routine_planned", "False")).lower() == "true")
            gym = st.checkbox("Gym Planned", value=str(plan.get("gym_planned", "False")).lower() == "true")
            
            priorities = st.text_area("Top Priorities", value=plan.get("priorities", ""))
            
            if st.form_submit_button("Save Plan"):
                data = {
                    "wake_time_planned": wake.strftime("%H:%M"),
                    "sleep_time_planned": sleep.strftime("%H:%M"),
                    "study_hours_planned": study,
                    "morning_routine_planned": routine,
                    "gym_planned": gym,
                    "priorities": priorities
                }
                create_or_update_plan(date_str, data)
                st.success("Plan Saved!")

elif page == "Execution":
    existing = get_execution(date_str) or {}
    
    with st.form("execution_form"):
        study_act = st.number_input("Actual Study Hours", min_value=0.0, step=0.5, value=float(existing.get("study_hours_actual", 0.0)))
        
        c1, c2 = st.columns(2)
        routine_done = c1.checkbox("Morning Routine Done", value=str(existing.get("morning_routine_done", "False")).lower() == "true")
        gym_done = c2.checkbox("Gym Done", value=str(existing.get("gym_done", "False")).lower() == "true")
        
        mood = st.slider("Mood", 1, 10, int(existing.get("mood_score", 5)))
        notes = st.text_area("Daily Notes", value=existing.get("notes", ""))
        
        if st.form_submit_button("Log Day"):
            data = {
                "study_hours_actual": study_act,
                "morning_routine_done": routine_done,
                "gym_done": gym_done,
                "mood_score": mood,
                "notes": notes
            }
            log_execution(date_str, data)
            score = calculate_day_score(date_str)
            st.success(f"Logged! Day Score: {score}")

elif page == "Gym":
    from src.gym.library import get_exercises
    from src.gym.workouts import log_set, get_exercise_history
    from src.gym.analytics import check_progressive_overload
    
    tab1, tab2 = st.tabs(["Log Workout", "History"])
    
    with tab1:
        exercises = get_exercises()
        ex_names = [e["name"] for e in exercises]
        
        c1, c2 = st.columns(2)
        selected_ex = c1.selectbox("Exercise", ex_names)
        
        # history context
        last_stats = get_exercise_history(selected_ex)
        if not last_stats.empty:
            last = last_stats.iloc[0]
            render_card("Last Best", f"{last['weight_kg']}kg x {last['reps']}")
        
        with st.form("gym_logger"):
            r1, r2, r3 = st.columns(3)
            weight = r1.number_input("Weight (kg)", step=2.5)
            reps = r2.number_input("Reps", step=1, min_value=1)
            rpe = r3.slider("RPE", 1, 10, 8)
            
            if st.form_submit_button("Log Set"):
                status = check_progressive_overload(selected_ex, weight, reps)
                log_set(date_str, selected_ex, weight, reps, rpe)
                st.success(f"Set Logged! {status}")
                
    with tab2:
        ex_view = st.selectbox("View Exercise", ex_names, key="hist_select")
        hist = get_exercise_history(ex_view)
        if not hist.empty:
            st.dataframe(hist[["date", "weight_kg", "reps", "rpe", "notes"]])
            st.line_chart(hist.set_index("date")["weight_kg"])
        else:
            st.info("No history yet.")

elif page == "Finance":
    from src.finance.manager import add_transaction, get_monthly_summary, get_category_breakdown, get_categories, add_category
    
    current_month = datetime.now().strftime("%Y-%m")
    summary = get_monthly_summary(current_month)
    
    c1, c2, c3 = st.columns(3)
    with c1: render_card("Income", f"${summary['income']}")
    with c2: render_card("Expenses", f"${summary['expense']}")
    with c3: render_card("Savings", f"${summary['savings']}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Add Transaction", "Analysis", "Budgets", "Settings"])
    
    with tab1:
        with st.form("finance_form"):
            d1, d2 = st.columns(2)
            date = d1.date_input("Date", datetime.now())
            amount = d2.number_input("Amount", min_value=0.01, step=1.0)
            
            t1, t2 = st.columns(2)
            trans_type = t1.selectbox("Type", ["Expense", "Income"])
            
            # Dynamic Categories
            cats = get_categories()
            category = t2.selectbox("Category", cats)
            
            desc = st.text_input("Description")
            
            if st.form_submit_button("Log Transaction"):
                add_transaction(date.strftime("%Y-%m-%d"), amount, trans_type, category, desc)
                st.success("Transaction Logged!")
                
    with tab2:
        st.subheader(f"Spending by Category ({current_month})")
        breakdown = get_category_breakdown(current_month)
        if not breakdown.empty:
            st.bar_chart(breakdown.set_index("category"))
            st.dataframe(breakdown)
        else:
            st.info("No expenses this month.")
            
        st.divider()
        st.subheader("Cashflow Trend (Coming Soon)")
        st.info("Trend chart will be implemented in Phase 12 (Insights).")

    with tab3:
        st.subheader("Budget Tracking")
        from src.finance.manager import get_budget_status, set_budget
        
        with st.expander("Set Budget"):
            with st.form("budget_form"):
                cats = get_categories()
                b_cat = st.selectbox("Category", cats)
                b_lim = st.number_input("Monthly Limit ($)", min_value=0.0)
                if st.form_submit_button("Set Limit"):
                    set_budget(b_cat, b_lim)
                    st.success("Budget Updated")
        
        status = get_budget_status(current_month)
        if not status.empty:
            for _, row in status.iterrows():
                st.write(f"**{row['category']}**")
                st.progress(row['percent'])
                st.caption(f"${row['spent']} / ${row['limit']} (Left: ${row['remaining']})")
        else:
            st.info("No budgets set.")
            
    with tab4:
        st.subheader("Manage Categories")
        with st.form("add_cat_form"):
            new_cat = st.text_input("New Category Name")
            if st.form_submit_button("Add Category"):
                if new_cat:
                    add_category(new_cat)
                    st.success(f"Added {new_cat}!")
                    st.experimental_rerun()

elif page == "Knowledge":
    from src.knowledge.notes import add_note, get_notes
    
    tab1, tab2 = st.tabs(["Library", "Capture"])
    
    with tab1:
        search = st.text_input("Search Notes", "")
        notes = get_notes(search)
        
        if not notes:
            st.info("No notes found.")
        else:
            for note in notes:
                with st.expander(f"{note['title']} ({note.get('tags', '')})"):
                    st.markdown(note['content'])
                    st.caption(f"Created: {note.get('created_at', '')[:10]}")

    with tab2:
        with st.form("note_form"):
            title = st.text_input("Title")
            tags = st.text_input("Tags (comma separated)")
            content = st.text_area("Content (Markdown supported)", height=200)
            
            if st.form_submit_button("Save Note"):
                if title and content:
                    add_note(title, content, tags)
                    st.success("Note Saved!")
                else:
                    st.error("Title and Content are required.")

elif page == "Systems":
    from src.systems.reviews import get_weekly_review_data, save_review, save_okr, get_okrs
    
    tab1, tab2 = st.tabs(["Weekly Review", "OKRs"])
    
    with tab1:
        st.subheader("Weekly Review Wizard")
        # Context
        data = get_weekly_review_data()
        c1, c2, c3 = st.columns(3)
        with c1: render_card("Study Hours", f"{data['study_hours']}h")
        with c2: render_card("Gym", data['gym_count'])
        with c3: render_card("Avg Mood", data['avg_mood'])
        
        with st.form("review_form"):
            c1, c2 = st.columns(2)
            week_start = c1.date_input("Week Starting", datetime.now() - timedelta(days=datetime.now().weekday()))
            score = c2.slider("Week Score (1-10)", 1, 10, 7)
            
            wins = st.text_area("Wins")
            challenges = st.text_area("Challenges")
            focus = st.text_area("Next Week Focus")
            
            if st.form_submit_button("Complete Review"):
                save_review(week_start.strftime("%Y-%m-%d"), wins, challenges, focus, score)
                st.success("Review Saved!")
    
    with tab2:
        st.subheader("OKRs")
        with st.expander("Add OKR"):
            with st.form("okr_form"):
                q = st.text_input("Quarter", "Q1 2026")
                obj = st.text_input("Objective")
                krs = st.text_area("Key Results")
                status = st.selectbox("Status", ["On Track", "At Risk", "Completed"])
                
                if st.form_submit_button("Save Goal"):
                    save_okr(q, obj, krs, status)
                    st.success("Goal Set!")
        
        df = get_okrs()
        if not df.empty:
            st.table(df[["quarter", "objective", "key_results", "status"]])

elif page == "Analytics":
    st.header("Analytics & Insights 🔍")
    
    from src.analytics.insights import get_insights
    
    insights = get_insights()
    
    st.subheader("Correlations (The Insight Engine)")
    
    if not insights:
        st.info("Not enough data yet to find correlations. Keep logging!")
    else:
        c1, c2 = st.columns(2)
        for i, ins in enumerate(insights):
            col = c1 if i % 2 == 0 else c2
            with col:
                with st.container():
                     st.markdown(f"**{ins['question']}**")
                     color = "green" if ins['impact'] == "positive" else "red" if ins['impact'] == "negative" else "gray"
                     st.markdown(f":{color}[{ins['answer']}]")
                     st.divider()
    
    st.subheader("Raw Data Export")
    # Placeholder for export
    st.caption("Export to CSV coming soon.")
