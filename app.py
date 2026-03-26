import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import os
import tempfile

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Academic Kundali",
    page_icon="🎓",
    layout="wide"
)

# ---------------- HEADER WITH LOGO ----------------

col1, col2 = st.columns([1,5])

with col1:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=120)

with col2:
    st.markdown(""" <h1 style='background: linear-gradient(90deg,#4facfe,#00f2fe);
     padding:18px;border-radius:10px;color:white'>
    Academic Kundali </h1>
    """, unsafe_allow_html=True)

st.write("Discover the best academic stream and career path based on your interests.")

#------------------FOOTER----------------

def add_footer(canvas, doc):

    canvas.saveState()

    width, height = letter

    canvas.setFont("Helvetica",9)

    # canvas.drawString(250,40,"End")

    canvas.drawString(200,25,"Address:")

    canvas.drawString(
        80,
        12,
        "Gurgaon-Badli Road Chandu, Budhera, Gurugram, Haryana 122505"
    )

    canvas.restoreState()

# ---------------- STUDENT INFO ----------------

st.subheader("Student Information")

c1,c2,c3 = st.columns(3)

with c1:
    student_name = st.text_input("Full Name")

with c2:
    student_email = st.text_input("Email")

with c3:
    student_phone = st.text_input("Phone")

# ---------------- LOAD MODEL ----------------

model = joblib.load("career_model.pkl")
features = joblib.load("features.pkl")

# ---------------- SIDEBAR ----------------

st.sidebar.header("Student Interests")

math = st.sidebar.slider("Interest in Mathematics",1,5,3)
physics = st.sidebar.slider("Interest in Physics",1,5,3)
chemistry = st.sidebar.slider("Interest in Chemistry",1,5,3)
biology = st.sidebar.slider("Interest in Biology",1,5,3)

economics = st.sidebar.slider("Interest in Economics",1,5,3)
business_interest = st.sidebar.slider("Interest in Business Topics",1,5,3)

history = st.sidebar.slider("Interest in History",1,5,3)
numerical = st.sidebar.slider("Interest in solving numerical problems",1,5,3)

doctor = st.sidebar.selectbox("Want to become a Doctor?",["No","Yes"])
engineer = st.sidebar.selectbox("Want to become an Engineer?",["No","Yes"])

doctor_val = 1 if doctor=="Yes" else 0
engineer_val = 1 if engineer=="Yes" else 0

generate_report = st.sidebar.button("Generate Report")

# ---------------- MAIN LOGIC ----------------

if generate_report:
    if student_name=="" or student_email=="" or student_phone=="":
        st.error("Please fill Name, Email and Phone before generating report.")
        st.stop()

    stem_score = math + physics + chemistry + numerical
    bio_score = biology*2 + doctor_val*3
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
        "I wanted to become a Doctor": doctor_val,
        "I wanted to become an Engineer": engineer_val,
        "stem_score": stem_score,
        "bio_score": bio_score,
        "commerce_score": commerce_score,
        "arts_score": arts_score
    }

    df = pd.DataFrame([student_data])
    df = df.reindex(columns=features, fill_value=0)

    # Rule based override

    stream_map = {
        0:"Science (Math)",
        1:"Science (Biology)",
        2:"Commerce",
        3:"Arts"
    }

    if math >=4 and physics >=4 and numerical >=4:
        predicted_stream = "Science (Math)"
        confidence = 95

    elif biology >=4 and doctor_val == 1:
        predicted_stream = "Science (Biology)"
        confidence = 95

    elif economics >=4 and business_interest >=4:
        predicted_stream = "Commerce"
        confidence = 90

    elif history >=4:
        predicted_stream = "Arts"
        confidence = 85

    else:
        prediction = model.predict(df)[0]
        predicted_stream = stream_map[prediction]
        proba = model.predict_proba(df)
        confidence = max(proba[0])*100

    st.success(f"Recommended Stream: {predicted_stream}")
    st.write(f"Confidence: {confidence:.2f}%")

    # ---------------- GRAPH ----------------

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

    graph_path = os.path.join(tempfile.gettempdir(),"graph.png")
    fig.write_image(graph_path)

    # ---------------- CAREERS ----------------

    career_map = {
    "Science (Math)": {

    "Engineering":[
    "Civil Engineer",
    "Mechanical Engineer",
    "Electrical Engineer",
    "Software Engineer",
    "Chemical Engineer",
    "Environmental Engineer",
    "Aerospace Engineer"
    ],

    "Information Technology":[
    "IT Consultant",
    "Cybersecurity Expert",
    "Software Developer",
    "Cloud Architect",
    "Data Scientist",
    "Artificial Intelligence (AI) Specialist"
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
    "Astrophysicist",
    "Geophysicist"
    ]

    },

    "Science (Biology)": {

    "Biological Sciences":[
    "Biotechnologist",
    "Microbiologist",
    "Geneticist",
    "Pharmacologist",
    "Forensic Scientist"
    ],

    "Environmental Sciences":[
    "Environmental Consultant",
    "Climate Change Analyst",
    "Marine Biologist",
    "Wildlife Biologist"
    ],

    "Medical Sciences":[
    "Doctor (General Practitioner)",
    "Surgeon",
    "Radiologist",
    "Medical Researcher",
    "Psychiatrist"
    ],

    "Healthcare & Wellness":[
    "Physiotherapist",
    "Nutritionist/Dietitian",
    "Public Health Expert",
    "Medical Lab Technician",
    "Optometrist"
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

    "Fine Arts":[
    "Artist",
    "Animator",
    "Art Curator",
    "Gallery Director",
    "Fashion Designer"
    ],

    "Humanities":[
    "Historian",
    "Archaeologist",
    "Anthropologist",
    "Philosopher"
    ],

    "Languages & Literature":[
    "Writer/Author",
    "Linguist",
    "Translator/Interpreter",
    "Editor",
    "Poet",
    "Literary Critic"
    ],

    "Performing Arts":[
    "Actor",
    "Musician",
    "Dancer",
    "Choreographer",
    "Stage Director"
    ],

    "Design & Architecture":[
    "Architect",
    "Interior Designer",
    "Graphic Designer",
    "Urban Planner"
    ],

    "Social Work & Psychology":[
    "Social Worker",
    "Clinical Psychologist",
    "School Counselor",
    "Therapist",
    "Career Counselor"
    ]

    }

    }

    # ---------------- SAVE STUDENT DATA ----------------

    data_row = {
        "Name":student_name,
        "Email":student_email,
        "Phone":student_phone,
        "Predicted Stream":predicted_stream,
        "Confidence":confidence
    }

    excel_file = "students_data.xlsx"
    if os.path.exists(excel_file):
        old = pd.read_excel(excel_file)
        new = pd.concat([old,pd.DataFrame([data_row])],ignore_index=True)
    else:
        new = pd.DataFrame([data_row])
    new.to_excel(excel_file,index=False)
    
    sections = career_map.get(predicted_stream, {})
    st.subheader("Suggested Careers")
    for section, careers in sections.items():
        st.markdown(f"### {section}")
        for career in careers:
            st.markdown(
                f"""
                <div style="padding:8px;border-radius:8px;margin-bottom:5px;background:#f4f6f7">
                {career}
                </div>
                """,
                unsafe_allow_html=True
            )
    # ---------------- PDF GENERATION ----------------
    # Indentation fixed here so button works correctly
    styles = getSampleStyleSheet()
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp:
        doc = SimpleDocTemplate(tmp.name,pagesize=letter)
        story = []
        logo_path = os.path.join(os.getcwd(),"logo.jpg")

        if os.path.exists(logo_path):
            story.append(Image(logo_path,width=120,height=50))

        story.append(Spacer(1,20))
        story.append(Paragraph("Academic Kundali",styles["Title"]))
        story.append(Spacer(1,20))
        story.append(Paragraph(f"Name: {student_name}",styles["Normal"]))
        story.append(Paragraph(f"Email: {student_email}",styles["Normal"]))
        story.append(Paragraph(f"Phone: {student_phone}",styles["Normal"]))
        story.append(Spacer(1,20))
        story.append(Paragraph(f"Recommended Stream: {predicted_stream}",styles["Normal"]))
        story.append(Paragraph(f"Confidence: {confidence:.2f}%",styles["Normal"]))
        story.append(Spacer(1,20))

        if os.path.exists(graph_path):
            story.append(Image(graph_path,width=350,height=250))

        story.append(Spacer(1,20))
        story.append(Paragraph("Suggested Career Paths", styles["Heading2"]))
        for section, careers in sections.items():
            story.append(Spacer(1,10))
            story.append(Paragraph(section, styles["Heading3"]))
            
            for career in careers:
                story.append(Paragraph(f"• {career}", styles["Normal"]))

        story.append(Spacer(1,40))

        doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

        with open(tmp.name,"rb") as f:
            st.download_button(
                "Download Career Report",
                f,
                file_name=f"SGT_{student_name}_Academic_Kundali.pdf",
                mime="application/pdf"
            )