import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("career_model.pkl")
features = joblib.load("features.pkl")

st.title("🎓 AI Career Counsellor")

st.write("Answer the questions below to get a recommended academic stream.")

# Academic interest sliders
math = st.slider("Interest in Mathematics",1,5,3)
physics = st.slider("Interest in Physics",1,5,3)
chemistry = st.slider("Interest in Chemistry",1,5,3)
biology = st.slider("Interest in Biology",1,5,3)
economics = st.slider("Interest in Economics",1,5,3)
business_interest = st.slider("I enjoy analysing business topics",1,5,3)
history = st.slider("Interest in History",1,5,3)
numerical = st.slider("I enjoy solving numerical problems",1,5,3)

# Career aspiration
doctor = st.selectbox("Do you want to become a Doctor?",["No","Yes"])
engineer = st.selectbox("Do you want to become an Engineer?",["No","Yes"])

doctor = 1 if doctor=="Yes" else 0
engineer = 1 if engineer=="Yes" else 0


if st.button("Predict Stream"):

    # Improved derived scores
    stem_score = math + physics + chemistry + numerical
    bio_score = biology*2 + doctor*3
    commerce_score = economics*2 + business_interest
    arts_score = history

    student_data = {

        "I enjoyed studying Mathematics": math,
        "I enjoyed studying Physics": physics,
        "I enjoyed studying Chemistry": chemistry,
        "I enjoyed studying Biology": biology,
        "I enjoyed studying Economics": economics,
        "I enjoyed studying History": history,
        "I enjoyed solving numerical problems": numerical,
        "I enjoyed analysing business or financial topics": business_interest,
        "I wanted to become a Doctor": doctor,
        "I wanted to become an Engineer": engineer,

        "stem_score": stem_score,
        "bio_score": bio_score,
        "commerce_score": commerce_score,
        "arts_score": arts_score
    }

    df = pd.DataFrame([student_data])
    df = df.reindex(columns=features, fill_value=0)

    # Rule-based override (Hybrid AI)
    if biology >=4 and doctor==1:
        predicted_stream = "Science (Biology)"
        confidence = 95

    elif math >=4 and physics >=4 and numerical >=4:
        predicted_stream = "Science (Math)"
        confidence = 90

    elif economics >=4 and business_interest >=4:
        predicted_stream = "Commerce"
        confidence = 90

    elif history >=4:
        predicted_stream = "Arts"
        confidence = 85

    else:

        prediction = model.predict(df)[0]

        proba = model.predict_proba(df)
        confidence = max(proba[0])*100

        stream_map = {
            0:"Science (Math)",
            1:"Science (Biology)",
            2:"Commerce",
            3:"Arts"
        }

        predicted_stream = stream_map[prediction]

    st.success(f"Recommended Stream: **{predicted_stream}**")
    st.write(f"Confidence: **{confidence:.2f}%**")

    career_map = {

    "Science (Math)": [
    "Software Engineer",
    "Data Scientist",
    "AI Engineer",
    "Mechanical Engineer",
    "Civil Engineer"
    ],

    "Science (Biology)": [
    "Doctor",
    "Dentist",
    "Pharmacist",
    "Biotechnologist",
    "Medical Researcher"
    ],

    "Commerce": [
    "Chartered Accountant",
    "Investment Banker",
    "Business Analyst",
    "Entrepreneur"
    ],

    "Arts": [
    "Lawyer",
    "Journalist",
    "Psychologist",
    "Graphic Designer"
    ]

    }

    st.subheader("Suggested Careers")

    for career in career_map[predicted_stream]:
        st.write("•", career)