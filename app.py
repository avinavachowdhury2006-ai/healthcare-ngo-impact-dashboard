import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------------
st.set_page_config(page_title="NGO Impact Dashboard", page_icon="🌟", layout="wide")

# --------------------------------------------------------
# 2. LOAD & CLEAN ENRICHED DATABASE
# --------------------------------------------------------
@st.cache_data
def load_data():
    # 1. Load the raw dataset
    df = pd.read_csv("healthcare_ngo_india_enriched.csv")
    
    # 2. Convert and construct time-series columns
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month_Year'] = df['Date'].dt.to_period('M').astype(str)
    
    # 3. FIX DATA QUALITY ISSUES (New additions)
    # Handle missing or corrupted outcomes safely
    df['Outcome'] = df['Outcome'].fillna('Under Observation')

    # Standardize case sensitivity and accidental spacing issues from manual entry
    df['Village'] = df['Village'].str.strip().str.title()

    # Cap absurd outliers in financial columns due to field typos (e.g., extra zeros)
    median_cost = df['Cost'].median()
    df.loc[df['Cost'] > (median_cost * 10), 'Cost'] = median_cost
    
    return df

df = load_data()

# --------------------------------------------------------
# 3. SIDEBAR CONTROLS
# --------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2833/2833315.png", width=80) # Add a generic health icon
st.sidebar.title("Dashboard Controls")
st.sidebar.markdown("Use these filters to slice the data.")

selected_villages = st.sidebar.multiselect("📍 Select Villages", options=df["Village"].unique(), default=df["Village"].unique()[:3])
selected_programs = st.sidebar.multiselect("🩺 Select Programs", options=df["Program"].unique(), default=df["Program"].unique())
selected_gender = st.sidebar.multiselect("👥 Select Gender", options=df["Gender"].unique(), default=df["Gender"].unique())

filtered_df = df[(df["Village"].isin(selected_villages)) & 
                 (df["Program"].isin(selected_programs)) & 
                 (df["Gender"].isin(selected_gender))]

# --------------------------------------------------------
# 4. APP HEADER & KPIS
# --------------------------------------------------------
st.title("🌟 Field-to-KPI: NGO Impact Dashboard")
st.markdown("Going beyond numbers to track event engagement, financial efficiency, and real human impact.")
# Calculate KPIs
total_patients = len(filtered_df)
total_cost = filtered_df["Cost"].sum()
recovered_patients = len(filtered_df[filtered_df["Outcome"] == "Recovered"])
recovery_rate = (recovered_patients / total_patients * 100) if total_patients > 0 else 0
avg_follow_up = filtered_df["Follow_Up"].mean()

# NEW: Calculate Cost per Impact
cost_per_recovery = (total_cost / recovered_patients) if recovered_patients > 0 else 0

# Display KPIs in a visually appealing way (Now using 5 columns)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Beneficiaries", f"{total_patients:,}")
col2.metric("Program Expenditure", f"₹{total_cost:,.0f}")
col3.metric("Successful Recoveries", f"{recovered_patients:,}", delta=f"{recovery_rate:.1f}% Rate")
col4.metric("Avg. Follow-up Visits", f"{avg_follow_up:.1f}")
# NEW: Displaying the crucial efficiency metric
col5.metric("Cost per Recovery", f"₹{cost_per_recovery:,.0f}", delta="Efficiency KPI", delta_color="off")
# --------------------------------------------------------
# 5. THE IMPACT FUNNEL (From previous addition)
# --------------------------------------------------------
treated_patients = len(filtered_df[filtered_df['Treatment_Status'].isin(['Completed', 'On Treatment'])])

funnel_data = pd.DataFrame({
    "Stage": ["1. Screened", "2. Treated", "3. Recovered"],
    "Count": [total_patients, treated_patients, recovered_patients]
})
fig_funnel = px.funnel(funnel_data, x="Count", y="Stage", title="🛤️ Patient Intervention Funnel")

# --------------------------------------------------------
# 6. EXCITING NEW VISUALIZATIONS (PIE & BAR)
# --------------------------------------------------------
chart_row1_col1, chart_row1_col2 = st.columns(2)

with chart_row1_col1:
    # PIE CHART: Breakdown of Diagnosis
    st.subheader("🧩 Patient Diagnosis Breakdown")
    fig_pie = px.pie(
        filtered_df, 
        names='Diagnosis', 
        hole=0.4, # Makes it a cool donut chart!
        color_discrete_sequence=px.colors.sequential.Teal
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_row1_col2:
    # BAR GRAPH: Event Attendance Percentages
    st.subheader("📊 Average Community Event Attendance")
    # Calculate average attendance for the three events
    avg_att_1 = filtered_df['Event1_Attendance_pct'].mean()
    avg_att_2 = filtered_df['Event2_Attendance_pct'].mean()
    avg_att_3 = filtered_df['Event3_Attendance_pct'].mean()
    
    attendance_data = pd.DataFrame({
        "Event": ["Health Awareness", "Nutrition Workshop", "Mental Health Outreach"],
        "Avg Attendance (%)": [avg_att_1, avg_att_2, avg_att_3]
    })
    
    fig_bar = px.bar(
        attendance_data, 
        x="Event", 
        y="Avg Attendance (%)", 
        color="Avg Attendance (%)",
        color_continuous_scale="Blues",
        text_auto='.1f'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
# --------------------------------------------------------
# NEW SECTION: TRENDS OVER TIME
# --------------------------------------------------------
st.subheader("📈 Monthly Impact Trends")
st.markdown("Tracking successful recoveries and overall patient intake over time.")

# Group data by Month_Year
trend_data = filtered_df.groupby('Month_Year').agg(
    Total_Treated=('Patient_ID', 'count'),
    Recoveries=('Outcome', lambda x: (x == 'Recovered').sum())
).reset_index()

# Sort chronologically if Month_Year is in YYYY-MM format
trend_data = trend_data.sort_values('Month_Year')

fig_trend = px.line(
    trend_data, 
    x='Month_Year', 
    y=['Total_Treated', 'Recoveries'],
    labels={'value': 'Number of Patients', 'Month_Year': 'Month', 'variable': 'Metric'},
    color_discrete_map={"Total_Treated": "#1f77b4", "Recoveries": "#2ca02c"}
)
st.plotly_chart(fig_trend, use_container_width=True)
# --------------------------------------------------------
# 7. FUNNEL & OUTCOMES ROW
# --------------------------------------------------------
chart_row2_col1, chart_row2_col2 = st.columns(2)

with chart_row2_col1:
    st.plotly_chart(fig_funnel, use_container_width=True)

with chart_row2_col2:
    st.subheader("📈 Recovery Rate by Program")
    # Group bar chart showing total patients vs recovered by program
    prog_stats = filtered_df.groupby("Program")["Outcome"].value_counts().unstack().fillna(0).reset_index()
    if 'Recovered' in prog_stats.columns and 'Deceased' in prog_stats.columns:
        fig_prog = px.bar(
            prog_stats, x="Program", y=["Recovered", "Deceased"], 
            barmode="group",
            color_discrete_map={"Recovered": "#2ca02c", "Deceased": "#d62728"}
        )
        st.plotly_chart(fig_prog, use_container_width=True)

st.markdown("---")

# --------------------------------------------------------
# 8. QUALITATIVE IMPACT (HUMAN STORIES)
# --------------------------------------------------------
st.subheader("❤️ Real Lives Improved")
st.markdown("Beyond the numbers, here are the actual field notes describing the human impact of our work.")

# Show 3 random human stories using Streamlit expanders
sample_stories = filtered_df[filtered_df["Outcome"] == "Recovered"].sample(min(3, len(filtered_df)))
for index, row in sample_stories.iterrows():
    with st.expander(f"Patient {row['Patient_ID']} from {row['Village']} ({row['Program']})"):
        st.write(f"**Diagnosis:** {row['Diagnosis']}")
        st.write(f"**Impact Story:** {row['Lives_Improved_Description']}")
        st.write(f"**Total Follow-ups:** {row['Follow_Up']}")
