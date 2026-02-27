import streamlit as st
import requests

API_URL = "http://127.0.0.1:8002/api/v1/router_endpoint"

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide"
)

# ----------------------
# Custom Styling
# ----------------------
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------
# Title
# ----------------------
st.title("🎓 Student Performance Prediction System")
st.markdown("### Predict student academic performance using ML")

# ----------------------
# Sidebar Inputs
# ----------------------
st.sidebar.header("📊 Academic Factors")

Hours_Studied = st.sidebar.slider("Hours Studied", 0, 12, 5)
Attendance = st.sidebar.slider("Attendance (%)", 0, 100, 75)
Previous_Scores = st.sidebar.slider("Previous Scores", 0, 100, 60)
Sleep_Hours = st.sidebar.slider("Sleep Hours", 0, 12, 7)
Tutoring_Sessions = st.sidebar.slider("Tutoring Sessions per Month", 0, 20, 2)
Physical_Activity = st.sidebar.slider("Physical Activity (hrs/week)", 0, 15, 3)

# ----------------------
# Personal & Environment
# ----------------------
st.sidebar.header("🏠 Environment & Background")

Parental_Involvement = st.sidebar.selectbox(
    "Parental Involvement", ["low", "Midium", "High"])
Access_to_Resources = st.sidebar.selectbox(
    "Access to Resources", ["low", "Midium", "High"])
Extracurricular_Activities = st.sidebar.selectbox(
    "Extracurricular Activities", ["Yes", "No"])
Motivation_Level = st.sidebar.selectbox(
    "Motivation Level", ["low", "Midium", "High"])
Internet_Access = st.sidebar.selectbox("Internet Access", ["Yes", "No"])
Family_Income = st.sidebar.selectbox(
    "Family Income", ["low", "Midium", "High"])
Teacher_Quality = st.sidebar.selectbox(
    "Teacher Quality", ["low", "Midium", "High"])
School_Type = st.sidebar.selectbox("School Type", ["Private", "Public"])
Peer_Influence = st.sidebar.selectbox(
    "Peer Influence", ["Positive", "Negative", "Neutral"])
Learning_Disabilities = st.sidebar.selectbox(
    "Learning Disabilities", ["Yes", "No"])
Parental_Education_Level = st.sidebar.selectbox(
    "Parental Education Level",
    ["High School", "Collage", "Postgraduate"]
)
Distance_from_Home = st.sidebar.selectbox(
    "Distance from Home", ["Near", "Moderate", "Far"])
Gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

# ----------------------
# Create Payload
# ----------------------
payload = {
    "Hours_Studied": Hours_Studied,
    "Attendance": Attendance,
    "Parental_Involvement": Parental_Involvement,
    "Access_to_Resources": Access_to_Resources,
    "Extracurricular_Activities": Extracurricular_Activities,
    "Sleep_Hours": Sleep_Hours,
    "Previous_Scores": Previous_Scores,
    "Motivation_Level": Motivation_Level,
    "Internet_Access": Internet_Access,
    "Tutoring_Sessions": Tutoring_Sessions,
    "Family_Income": Family_Income,
    "Teacher_Quality": Teacher_Quality,
    "School_Type": School_Type,
    "Peer_Influence": Peer_Influence,
    "Physical_Activity": Physical_Activity,
    "Learning_Disabilities": Learning_Disabilities,
    "Parental_Education_Level": Parental_Education_Level,
    "Distance_from_Home": Distance_from_Home,
    "Gender": Gender
}

# ----------------------
# Prediction Button
# ----------------------
if st.button("🚀 Predict Performance"):

    with st.spinner("Analyzing student data..."):
        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                prediction = response.json()

                st.success("Prediction Successful!")

                st.markdown("## 📈 Predicted Performance Score")
                st.metric(label="Student Score",
                          value=f"{round(prediction, 2)}")

                if prediction >= 75:
                    st.info("🌟 Excellent Performance Expected")
                elif prediction >= 50:
                    st.warning("⚖️ Average Performance Expected")
                else:
                    st.error("⚠️ Performance Needs Improvement")

            else:
                st.error(f"API Error: {response.text}")

        except Exception as e:
            st.error(f"Connection Error: {e}")
