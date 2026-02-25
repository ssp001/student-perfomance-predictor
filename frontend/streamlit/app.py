import streamlit as st
import httpx

API_URL = "http://127.0.0.1:8000/model_service_api_server/predict/"

st.set_page_config(page_title="Student Performance Predictor")

st.title("🎓 Student Performance Prediction System")

st.markdown("Fill the details below to predict exam score")

# ---------------- Numeric Inputs ----------------

Hours_Studied = st.number_input("Hours Studied", 0, 100, 20)
Attendance = st.number_input("Attendance (%)", 0, 100, 85)
Sleep_Hours = st.number_input("Sleep Hours", 0, 12, 7)
Previous_Scores = st.number_input("Previous Scores", 0, 100, 70)
Tutoring_Sessions = st.number_input("Tutoring Sessions", 0, 20, 1)
Physical_Activity = st.number_input("Physical Activity (hrs/week)", 0, 20, 3)

# ---------------- Ordinal ----------------

Parental_Involvement = st.selectbox(
    "Parental Involvement", ["Low", "Medium", "High"])
Access_to_Resources = st.selectbox(
    "Access to Resources", ["Low", "Medium", "High"])
Motivation_Level = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
Family_Income = st.selectbox("Family Income", ["Low", "Medium", "High"])
Teacher_Quality = st.selectbox("Teacher Quality", ["Low", "Medium", "High"])
Peer_Influence = st.selectbox(
    "Peer Influence", ["Negative", "Neutral", "Positive"])
Parental_Education_Level = st.selectbox("Parental Education Level", [
                                        "High School", "College", "Postgraduate"])
Distance_from_Home = st.selectbox(
    "Distance From Home", ["Near", "Moderate", "Far"])

# ---------------- One Hot ----------------

Extracurricular_Activities = st.selectbox(
    "Extracurricular Activities", ["Yes", "No"])
Internet_Access = st.selectbox("Internet Access", ["Yes", "No"])
School_Type = st.selectbox("School Type", ["Public", "Private"])
Learning_Disabilities = st.selectbox("Learning Disabilities", ["Yes", "No"])
Gender = st.selectbox("Gender", ["Male", "Female"])

# ---------------- Predict Button ----------------

if st.button("Predict Score"):

    payload = {
        "Hours_Studied": Hours_Studied,
        "Attendance": Attendance,
        "Sleep_Hours": Sleep_Hours,
        "Previous_Scores": Previous_Scores,
        "Tutoring_Sessions": Tutoring_Sessions,
        "Physical_Activity": Physical_Activity,
        "Parental_Involvement": Parental_Involvement,
        "Access_to_Resources": Access_to_Resources,
        "Motivation_Level": Motivation_Level,
        "Family_Income": Family_Income,
        "Teacher_Quality": Teacher_Quality,
        "Peer_Influence": Peer_Influence,
        "Parental_Education_Level": Parental_Education_Level,
        "Distance_from_Home": Distance_from_Home,
        "Extracurricular_Activities": Extracurricular_Activities,
        "Internet_Access": Internet_Access,
        "School_Type": School_Type,
        "Learning_Disabilities": Learning_Disabilities,
        "Gender": Gender
    }

    try:
        response = httpx.post(API_URL, json=payload, timeout=10.0)

        if response.status_code == 200:
            result = response.json()
            st.success(
                f"🎯 Predicted Exam Score: {result['Predicted_Score']:.2f}")
        else:
            st.error("Model service error")

    except Exception:
        st.error("Cannot connect to API Gateway")
