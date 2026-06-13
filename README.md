COMPREHENSIVE USER GUIDE FOR NGO STAFF
Target Audience: Executive Directors, Program Managers, and Field Coordinators (Non-technical).
NGO Impact Dashboard: Operational Guide
Welcome to the NGO Impact Dashboard. This tool transforms raw field data into actionable insights, helping you prove impact to donors, course-correct failing programs, and celebrate your successes.
Part 1: Setting Your Focus (The Sidebar) On the left side of your screen, you will find the Dashboard Controls. These filters allow you to slice the data to answer specific questions.
•	Select Villages: Preparing for a town hall in a specific community? Deselect all other villages to see data only for that location.
•	Select Programs: Writing a grant report for a specific funder? Filter by the program they fund (e.g., only select "Malaria Control").
•	Select Gender: Use this to ensure your programs are reaching demographics equitably.
Part 2: The "Monday Morning" Metrics (Top Row KPIs) These five numbers are the vital signs of your NGO. Check them weekly.
•	Total Beneficiaries: The absolute reach of your filtered parameters.
•	Program Expenditure: How much capital has been deployed.
•	Successful Recoveries: The absolute number of people whose health has definitively improved.
•	Avg. Follow-up Visits: A measure of your field workers' effort. If this drops below 2.0, it may indicate field staff are overstretched.
•	Cost per Recovery (The Golden Metric): This is your efficiency score. It divides your total expenditure by your successful recoveries. Use this number in pitch decks to tell donors exactly how far their rupee goes.
Part 3: Diagnosing Program Health (The Visuals)
•	Patient Intervention Funnel: This shows the drop-off from Screening to Treatment to Recovery. If the gap between "Treated" and "Recovered" is unusually large, your treatment protocol may need review.
•	Diagnosis Breakdown (Donut Chart): Shows community disease prevalence at a glance. Use this to order medical supplies proactively.
•	Event Attendance (Bar Chart): Shows which community events draw the largest crowds. Stop funding events with consistently low attendance.
•	Recovery Rate by Program: Compares the effectiveness of different initiatives side-by-side.
Part 4: The Human Element Scroll to the bottom section titled "Real Lives Improved". Here, the dashboard randomly selects three successfully recovered patients and displays the actual notes from your field workers.







DATA DICTIONARY
Column Name	Data Type	Description & Business Logic	Allowed Values / Formatting	Dashboard Usage
Patient_ID	String	Unique alphanumeric identifier assigned to each beneficiary upon first contact.	E.g., PT-10042	Primary key; used to count Total Beneficiaries.
Date	Datetime	The exact date of the beneficiary's initial screening or enrollment.	YYYY-MM-DD	Converted to Month_Year for time-series tracking.
Month_Year	String	Derived column grouping Date into monthly periods for trend analysis.	YYYY-MM	X-axis for the "Monthly Impact Trends" chart.
Village	String	The specific geographic community where the intervention occurred.	Categorical (e.g., Village A)	Global Filter (Sidebar).
Program	String	The specific health initiative the patient is enrolled in.	Categorical (e.g., Maternal Health)	Global Filter (Sidebar); X-axis for Recovery grouping.
Gender	String	The identified gender of the beneficiary.	Male, Female, Other	Global Filter (Sidebar).
Diagnosis	String	The primary medical issue identified during the screening phase.	Categorical (e.g., Anemia)	Plotted in the "Patient Diagnosis Breakdown" Donut Chart.
Treatment_Status	String	The current operational phase of the patient's medical journey.	Screened, On Treatment, Completed	Drives the middle stages of the Patient Intervention Funnel.
Outcome	String	The definitive health result of the intervention.	Recovered, Under Observation, Deceased	Drives the "Successful Recoveries" KPI and Recovery Rate.
Cost	Float	The total program expenditure allocated to this specific patient in Indian Rupees (₹).	Numeric (0.0 to ∞)	Drives "Program Expenditure" and "Cost per Recovery" KPIs.
Follow_Up	Integer	The total number of physical follow-up visits conducted by field workers.	Numeric (0 to ∞)	Averaged for the "Avg. Follow-up Visits" KPI.
Event1_Attendance_pct	Float	The percentage of localized "Health Awareness" events the patient attended.	Numeric (0.0 to 100.0)	Averaged in the "Community Event Attendance" Bar Graph.
Event2_Attendance_pct	Float	The percentage of localized "Nutrition Workshop" events the patient attended.	Numeric (0.0 to 100.0)	Averaged in the "Community Event Attendance" Bar Graph.
Event3_Attendance_pct	Float	The percentage of localized "Mental Health" outreach events attended.	Numeric (0.0 to 100.0)	Averaged in the "Community Event Attendance" Bar Graph.
Lives_Improved_Description	Text	Qualitative, unstructured field notes written by the community health worker detailing the human impact.	Free-form text	Displayed inside the "Real Lives Improved" expander toggles.







Answers to Key Questions to Explore
1. What is the ONE number the ED should check every Monday?
•	The Answer: The Rolling 30-Day Cost-per-Recovery (Efficiency Score).
•	Why this number? While total patient count indicates scale, and total expenditure indicates budget burn, neither tells the ED if the programs are working efficiently. If the cost-per-recovery spikes on a Monday morning, it acts as an immediate smoke detector for the ED. It means either:
1.	Field expenses are rising without producing clinical results (Cost is increasing).
2.	Patients are dropping out of the treatment funnel before crossing the finish line (Recovered is decreasing).
•	How it looks in your data: It is calculated by filtering the dataset for the last 30 days based on the Date column, summing the total Cost, and dividing it by the count of records where Outcome == 'Recovered'.
2. How do you handle data quality issues from field workers?
Data coming from rural or semi-urban field operations in India often suffers from typos, delayed entries, or missing clinical statuses. To hit your success metric of Page load time < 3 seconds and ensure data integrity, implement a three-tiered programmatic and operational defense strategy:
•	Operational Defense (Front-End Constraints): Do not let field workers type open text into a Google Sheet or app for critical fields. Use drop-down validation for columns like Village, Program, Gender, Diagnosis, Treatment_Status, and Outcome.
•	Programmatic Cleaning (The Streamlit Translation Layer): In your Python backend, implement data-cleaning overrides during the data-loading step .
•	The "Data Anomaly" Flagged View: We add a hidden or collapsible tab in your dashboard accessible only to the data manager. This allows the team to pinpoint exactly which field worker submitted incomplete data for a quick verification call.
3. What's the right cadence — real-time, weekly, or monthly?
A common mistake is assuming everything needs to be "real-time." For an Indian healthcare NGO, a hybrid approach based on stakeholder roles is the industry best practice:
Cadence	Targeted Stakeholder	Actionable Purpose	Metrics Tracked
Real-Time	Frontline Field Workers & Supervisors	Immediate clinical follow-ups and coordination.	Individual Patient_ID tracking, mapping who is due for a Follow_Up visit this week.
Weekly (Recommended Dashboard Default)	Program Managers & Executive Director	Mid-course correction of active field operations.	The Monday Morning Metric (Cost-per-recovery tracking), shifting inventory of medical supplies based on Diagnosis trends.
Monthly	Board Members & Institutional Donors	Strategic resource allocation, grant utilization reporting, and macro impact proof.	Time-series trends (Month_Year), overall village-by-village comparative Recovery Rate reports.







M&E (Monitoring and Evaluation) Validated KPI Logic Tree
To satisfy standard Monitoring & Evaluation (M&E) protocols (often required by large foundations like Catalyst 2030 or Sattva), your metrics must ladder up logically. This tree maps your NGO's daily activities to long-term systemic change, explicitly referencing the Streamlit dashboard calculations.
Level 1: Inputs (Resources Invested)
•	Metric: Total Financial Capital Deployed.
•	Dashboard Calculation: Sum of [Cost] across filtered parameters.
•	M&E Question: What resources are we putting into the field?
Level 2: Activities (What the NGO Does)
•	Metric: Field Worker Effort & Community Engagement.
•	Dashboard Calculation: Average of [Follow_Up] and Average of [Event1/2/3_Attendance_pct].
•	M&E Question: Are our field teams actively engaging the community?
Level 3: Outputs (Direct Products of Activities)
•	Metric: Total Reach & Pipeline Volume.
•	Dashboard Calculation: Count of [Patient_ID] (Total Beneficiaries) and Funnel Stage 2 (Count of Treatment_Status == 'On Treatment').
•	M&E Question: How many people are accessing our services?
Level 4: Outcomes (Short/Medium-Term Changes)
•	Metric: Clinical Success.
•	Dashboard Calculation: Count of [Outcome] == 'Recovered' and Recovery Rate % (Recovered / Total Patients).
•	M&E Question: Are our interventions actually curing/helping people?
Level 5: Impact (Long-Term Value & Efficiency)
•	Metric: Financial Efficiency of Life Improvement.
•	Dashboard Calculation: Total Cost / Recovered Patients (Cost per Recovery).
•	M&E Question: Are we translating donor capital into saved lives in a highly efficient, scalable way?

