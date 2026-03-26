import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

st.set_page_config(
page_title="AI Career Counsellor",
page_icon="🎓",
layout="wide"
)

st.markdown("""

<h1 style='text-align:center;
background: linear-gradient(90deg,#4facfe,#00f2fe);
padding:18px;
border-radius:10px;
color:white'>
AI Career Counsellor
</h1>
""", unsafe_allow_html=True)

st.write("Discover the best academic stream and career path based on your interests.")

model = joblib.load("career_model.pkl")
features = joblib.load("features.pkl")

st.sidebar.header("Student Interests")

math = st.sidebar.slider("Interest in Mathematics",1,5,3)
physics = st.sidebar.slider("Interest in Physics",1,5,3)
chemistry = st.sidebar.slider("Interest in Chemistry",1,5,3)
biology = st.sidebar.slider("Interest in Biology",1,5,3)

economics = st.sidebar.slider("Interest in Economics",1,5,3)
business_interest = st.sidebar.slider("Interest in Business Topics",1,5,3)

history = st.sidebar.slider("Interest in Humanities / History",1,5,3)
numerical = st.sidebar.slider("Interest in solving numerical problems",1,5,3)

doctor = st.sidebar.selectbox("Want to become a Doctor?",["No","Yes"])
engineer = st.sidebar.selectbox("Want to become an Engineer?",["No","Yes"])

doctor = 1 if doctor=="Yes" else 0
engineer = 1 if engineer=="Yes" else 0

predict_button = st.sidebar.button("Predict Stream")

if predict_button:
    # FEATURE ENGINEERING
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

    # HYBRID AI PREDICTION
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

        stream_map = {
            0:"Science (Math)",
            1:"Science (Biology)",
            2:"Commerce",
            3:"Arts"
        }

        predicted_stream = stream_map[prediction]

        proba = model.predict_proba(df)
        confidence = max(proba[0]) * 100

    st.success(f"Recommended Stream: **{predicted_stream}**")

    st.write("Confidence Level")
    st.progress(int(confidence))
    st.write(f"{confidence:.2f}%")

    st.subheader("Why this stream?")

    explanation = []

    if predicted_stream == "Science (Biology)":
        explanation.append("You have strong interest in Biology.")
        if doctor:
            explanation.append("You indicated interest in becoming a Doctor.")

    if predicted_stream == "Science (Math)":
        explanation.append("You show strong interest in Mathematics and Physics.")
        explanation.append("You enjoy solving numerical problems.")

    if predicted_stream == "Commerce":
        explanation.append("You show interest in Economics and Business topics.")

    if predicted_stream == "Arts":
        explanation.append("You show interest in Humanities subjects.")

    for e in explanation:
        st.write("•", e)

    st.subheader("Interest Profile")

    scores = {
        "STEM": stem_score,
        "Biology": bio_score,
        "Commerce": commerce_score,
        "Arts": arts_score
    }

    fig = px.line_polar(
        r=list(scores.values()),
        theta=list(scores.keys()),
        line_close=True
    )

    st.plotly_chart(fig)

    st.subheader("Suggested Careers")

    career_map = {

        "Science (Math)": {

        "Engineering":[
        "Civil Engineer",
        "Mechanical Engineer",
        "Electrical Engineer",
        "Software Engineer",
        "Aerospace Engineer"
        ],

        "Information Technology":[
        "IT Consultant",
        "Cybersecurity Expert",
        "Software Developer",
        "Cloud Architect",
        "Data Scientist",
        "AI Specialist"
        ],

        "Mathematics & Statistics":[
        "Mathematician",
        "Statistician",
        "Operations Research Analyst",
        "Actuary"
        ],

        "Physical Sciences":[
        "Physicist",
        "Chemist",
        "Meteorologist",
        "Astrophysicist"
        ]

        },

        "Science (Biology)": {

        "Medical Sciences":[
        "Doctor",
        "Surgeon",
        "Radiologist",
        "Psychiatrist",
        "Medical Researcher"
        ],

        "Biological Sciences":[
        "Biotechnologist",
        "Microbiologist",
        "Geneticist",
        "Pharmacologist",
        "Forensic Scientist"
        ],

        "Healthcare":[
        "Physiotherapist",
        "Nutritionist",
        "Public Health Expert",
        "Medical Lab Technician",
        "Optometrist"
        ],

        "Environmental Sciences":[
        "Environmental Consultant",
        "Climate Change Analyst",
        "Marine Biologist",
        "Wildlife Biologist"
        ]

        },

        "Commerce": {

        "Entrepreneurship":[
        "Startup Founder",
        "Small Business Owner",
        "Social Entrepreneur",
        "Franchise Owner"
        ],

        "Corporate Careers":[
        "Business Development Manager",
        "HR Manager",
        "Operations Manager",
        "Marketing Manager",
        "Sales Manager",
        "Financial Manager"
        ]

        },

        "Arts": {

        "Humanities":[
        "Historian",
        "Archaeologist",
        "Anthropologist",
        "Philosopher"
        ],

        "Languages & Literature":[
        "Writer",
        "Linguist",
        "Translator",
        "Editor",
        "Poet"
        ],

        "Performing Arts":[
        "Actor",
        "Musician",
        "Dancer",
        "Choreographer",
        "Stage Director"
        ],

        "Design":[
        "Architect",
        "Interior Designer",
        "Graphic Designer",
        "Urban Planner"
        ],

        "Psychology":[
        "Clinical Psychologist",
        "Therapist",
        "School Counselor",
        "Career Counselor"
        ]

        }

        }
    
    st.subheader("Suggested Career Paths")
    sections = career_map[predicted_stream]

    for section, careers in sections.items():

        st.markdown(f"### {section}")

        for career in careers:

            st.markdown(
                f"""
                <div style="padding:8px;
                border-radius:8px;
                margin-bottom:5px;
                background:#f4f6f7">
                {career}
                </div>
                """,
                unsafe_allow_html=True
            )

    # ---------- PDF REPORT ---------- 
    styles = getSampleStyleSheet() 
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp: 
        doc = SimpleDocTemplate(tmp.name, pagesize=letter) 
        story = [] 
        story.append(Paragraph("AI Career Counselling Report", styles["Title"])) 
        story.append(Spacer(1,20)) 
        story.append(Paragraph(f"Recommended Stream: {predicted_stream}", styles["Normal"])) 
        story.append(Paragraph(f"Confidence: {confidence:.2f}%", styles["Normal"])) 
        story.append(Spacer(1,20)) 
        story.append(Paragraph("Explanation:", styles["Heading2"])) 
        for e in explanation: 
            story.append(Paragraph(e, styles["Normal"])) 
        story.append(Spacer(1,20)) 
        story.append(Paragraph("Career Suggestions:", styles["Heading2"])) 
        for career in career_map[predicted_stream]: 
            story.append(Paragraph(career, styles["Normal"])) 
        doc.build(story) 
        with open(tmp.name,"rb") as f: 
            st.download_button( 
                label="Download Career Report (PDF)", 
                data=f, file_name="career_report.pdf", 
                mime="application/pdf" 
            )    