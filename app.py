import streamlit as st
import json
import random
import os
import pandas as pd
from fpdf import FPDF

# -------------------------
# Account configuration
# -------------------------
ACCOUNTS = {
    "Rica": "Rica",
    "Nadiya": "Nadiya",
    "Jairo": "Jairo",
    "Guest": "Guest"
}

# -------------------------
# Session initialization
# -------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'question_idx' not in st.session_state:
    st.session_state.question_idx = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'completed' not in st.session_state:
    st.session_state.completed = False
if 'order_list' not in st.session_state:
    st.session_state.order_list = []
if 'section_map' not in st.session_state:
    st.session_state.section_map = []

# -------------------------
# Login page
# -------------------------
def login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in ACCOUNTS and ACCOUNTS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            load_progress()
            st.rerun()
        else:
            st.error("Incorrect username or password.")

# -------------------------
# Save & load progress
# -------------------------
def save_progress():
    save_data = {
        "answers": st.session_state.answers,
        "question_idx": st.session_state.question_idx,
        "completed": st.session_state.completed,
        "order_list": st.session_state.order_list,
        "section_map": st.session_state.section_map
    }
    with open(f"{st.session_state.username}_div1_progress.json", "w") as f:
        json.dump(save_data, f)

def load_progress():
    filename = f"{st.session_state.username}_div1_progress.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            st.session_state.answers = data.get("answers", {})
            st.session_state.question_idx = data.get("question_idx", 0)
            st.session_state.completed = data.get("completed", False)
            st.session_state.order_list = data.get("order_list", [])
            st.session_state.section_map = data.get("section_map", [])
    else:
        st.session_state.answers = {}
        st.session_state.question_idx = 0
        st.session_state.completed = False
        st.session_state.order_list = []
        st.session_state.section_map = []

# -------------------------
# Question display
# -------------------------
def show_question(question, disp_number, section_name, q_idx):
    st.subheader(f"Question {disp_number + 1}")
    st.markdown(f"<div style='text-align:right; font-size:14px; color:gray;'>Section: {section_name}</div>", unsafe_allow_html=True)

    if "image" in question and question["image"]:
        if os.path.exists(question["image"]) and question["image"].lower() != "to_be_added":
            st.image(question["image"], use_container_width=True)

    st.write(question["question"])
    options = question["options"]
    correct = question["answer"]

    css = """
    <style>
    div[role="radiogroup"] > label.correct span {
        color: #2E8B57 !important;
        font-weight: bold;
    }
    div[role="radiogroup"] > label.wrong span {
        color: #DC143C !important;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    if q_idx in st.session_state.answers:
        selected = st.session_state.answers[q_idx]
        st.radio("Your answer:", options, index=options.index(selected), disabled=True, key=f"answer_radio_{q_idx}")
        st.markdown(f"**Correct answer:** {correct}")
        st.info(f"Explanation: {question.get('explanation', 'No explanation provided.')}")
    else:
        selected = st.radio("Choose your answer:", options, key=f"answer_radio_{q_idx}")

        if st.button("Confirm", key=f"confirm_{q_idx}"):
            if q_idx not in st.session_state.answers:
                st.session_state.answers[q_idx] = selected
                save_progress()
                st.rerun()

# -------------------------
# Sidebar navigation
# -------------------------
def question_sidebar(questions):
    st.sidebar.title("Questions")
    for idx, q_idx in enumerate(st.session_state.order_list):
        btn_label = f"Question {idx + 1}"
        if q_idx in st.session_state.answers:
            correct = questions[q_idx]["answer"]
            chosen = st.session_state.answers[q_idx]
            color = "#2E8B57" if chosen == correct else "#DC143C"
            st.sidebar.markdown(
                f"""
                <button style='
                    background-color: transparent;
                    border: 2px solid {color};
                    color: white;
                    width: 100%;
                    border-radius: 5px;
                    padding: 5px;
                    cursor: not-allowed;
                ' disabled>{btn_label}</button>
                """,
                unsafe_allow_html=True,
            )
        else:
            if st.sidebar.button(btn_label, key=f"nav_{idx}"):
                st.session_state.question_idx = idx
                st.rerun()

# -------------------------
# PDF Export
# -------------------------
def generate_pdf(questions, section_names):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for idx, q_idx in enumerate(st.session_state.order_list):
        q = questions[q_idx]
        section = section_names[q_idx]
        pdf.multi_cell(0, 10, f"Section: {section}")
        pdf.multi_cell(0, 10, f"Q{idx + 1}: {q['question']}")
        pdf.multi_cell(0, 10, f"Correct answer: {q['answer']}")
        pdf.multi_cell(0, 10, f"Explanation: {q.get('explanation', 'No explanation provided.')}")
        pdf.ln()

    filename = f"{st.session_state.username}_div1_results.pdf"
    pdf.output(filename)
    return filename

# -------------------------
# Main logic
# -------------------------
st.sidebar.title("Navigation")
options = st.sidebar.radio("Choose a section:", ["Home", "Mock Exam", "About", "References"])

if options == "Home":
    if not st.session_state.logged_in:
        login()
    else:
        st.header("Welcome to the MT Review - Mock Exam")
        st.write(f"Hello, {st.session_state.username}! You are logged in.")
        st.write("Use the sidebar to start your exam or learn more.")
        st.write("This app is still under development, so please check back later for more features and content.")
        st.write("For any issues or suggestions, please contact: daquiogjairo30@gmail.com.")
        st.write("The contents of this app are for educational purposes only and do not reflect the actual PRC Board of Medical Technology exam in the Philippines." \
                 "Always refer to official resources and consult with licensed professionals for accurate information." \
                 "This app used various sources, such as articles, books, and online resources. Please refer to the 'References' section for more details.")
        st.markdown(
        """
        <style>
        .footer-text {
            position: fixed;
            bottom: 30px;
            width: 36%;
            text-align: center;
            font-family: "Playfair Display", serif;
            font-style: italic;
            opacity: 0.08;
            font-size: 18px;
        }
        </style>
        <div class="footer-text">
            R
        </div>
        """,
        unsafe_allow_html=True
    )

elif options == "Mock Exam":
    if not st.session_state.logged_in:
        login()
    else:
        st.header("Mock Exam")
        div = st.selectbox("Select div", ["Introduction", "Div 1", "Div 2", "Div 3", "Div 4", "Div 5", "Div 6"])

        st.write("Disclaimer: This is a mock exam for educational purposes only. The exam does not directly reflect the actual questions in the MTLE. It is advised to refer to official resources and consult with licensed professionals for accurate information.")

        if div == "Introduction":
            st.write("The developer divided the mock exam into 6 divisions, each with the same distribution of questions sections.")
            st.write("WHY? Because it's difficult to cram all the questions into one division, and it would be too long to answer in one sitting and I don't actually know the actual distribution of questions in the PRC Board of Medical Technology exam.")
            st.write("In each division, the distribution of sections/questions is as follows:")

            df_dis = pd.read_csv('d1_dis.csv')
            st.dataframe(df_dis, hide_index=True)

            st.write("This data is based from PRC Board of Medical Technology Resolution No. 15 Series of 1996 https://www.prc.gov.ph/sites/default/files/Board%20of%20Medical%20Technology%20-%20Syllabi_0.pdf")

        elif div == "Div 1":
            st.subheader("Div 1: Mock Exam Questions")
            files_sections = [
                ("d1_clinical_chem.json", "Clinical Chemistry"),
                ("d1_microb_parasi.json", "Microbiology & Parasitology"),
                ("d1_hematology.json", "Hematology"),
                ("d1_blood_banking.json", "Blood Banking & Serology"),
                ("d1_clinical_microscopy.json", "Clinical Microscopy"),
                ("d1_histopath_law_ethics.json", "Histopath, Laws & Ethics")
            ]

            if not st.session_state.questions or not st.session_state.order_list:
                questions = []
                section_names = []
                order_list = []

                for file, sec_name in files_sections:
                    with open(file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        sec_questions = data["questions"]
                        sec_indices = list(range(len(questions), len(questions) + len(sec_questions)))
                        random.shuffle(sec_indices)
                        questions.extend(sec_questions)
                        section_names.extend([sec_name] * len(sec_questions))
                        order_list.extend(sec_indices)

                st.session_state.questions = questions
                st.session_state.section_map = section_names
                st.session_state.order_list = order_list
                st.session_state.answers = {}
                st.session_state.question_idx = 0
                st.session_state.completed = False
                save_progress()

            questions = st.session_state.questions
            section_names = st.session_state.section_map
            order_list = st.session_state.order_list

            question_sidebar(questions)

            if st.session_state.completed:
                st.success("You finished Div 1!")
                score = sum(1 for idx, ans in st.session_state.answers.items() if ans == questions[order_list[idx]]["answer"])
                st.write(f"Your score: {score}/{len(questions)}")

                if st.button("Retake Exam"):
                    st.session_state.questions = []
                    st.session_state.order_list = []
                    st.session_state.section_map = []
                    st.session_state.answers = {}
                    st.session_state.question_idx = 0
                    st.session_state.completed = False
                    save_progress()
                    st.experimental_rerun()

                if st.button("Download Results as PDF"):
                    filename = generate_pdf(questions, section_names)
                    with open(filename, "rb") as f:
                        st.download_button("Download PDF", f, file_name=filename)
            else:
                current_q_idx = st.session_state.question_idx
                actual_idx = order_list[current_q_idx]
                section_name = section_names[actual_idx]

                show_question(questions[actual_idx], current_q_idx, section_name, actual_idx)

                if st.button("Next"):
                    if current_q_idx + 1 < len(order_list):
                        st.session_state.question_idx += 1
                    else:
                        st.session_state.completed = True
                    save_progress()
                    st.rerun()

                prev_unanswered = None
                for i in range(current_q_idx - 1, -1, -1):
                    if order_list[i] not in st.session_state.answers:
                        prev_unanswered = i
                        break

                if prev_unanswered is not None:
                    if st.button("Previous"):
                        st.session_state.question_idx = prev_unanswered
                        save_progress()
                        st.rerun()
                else:
                    st.button("Previous", disabled=True)

        else:
            st.info(f"{div} content coming soon!")

elif options == "About":
    st.header("About")
    st.write("Developed by Devon Daquioag, a Computer Engineering undergraduate at Centro Escolar University, Manila.")
    st.write("This app was developed with the hopes of helping the developer's friends in the Medical Technology program with their endeavors in their field.")
    st.write("This app is still under development (<10%), so please check back later for more features and content.")
    st.write("For any issues or suggestions, please contact: daquiogjairo30@gmail.com.")
    st.write("Disclaimer: This is a mock exam for educational purposes only. The exam does not directly reflect the actual questions in the MTLE. It is advised to refer to official resources and consult with licensed professionals for accurate information.")
    st.write("This app used various sources, such as articles, books, and online resources. Please refer to the 'References' section for more details.")
    st.write("All rights reserved. This app is not affiliated with the Professional Regulation Commission (PRC) or any official medical technology board review programs.")

    st.markdown(
        """
        <p style='font-style: italic; opacity: 0.5; text-align: center; font-family: "Times New Roman", serif; font-size: 12px;'>
        To God be all the glory!
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .footer-text {
            position: fixed;
            bottom: 30px;
            width: 36%;
            text-align: center;
            font-family: "Playfair Display", serif;
            font-style: italic;
            opacity: 0.08;
            font-size: 18px;
        }
        </style>
        <div class="footer-text">
            R
        </div>
        """,
        unsafe_allow_html=True
    )

elif options == "References":
    with open('references.json') as f:
        data = json.load(f)
        st.header("References")
        for ref in data["references"]:
            st.markdown(f"- **{ref['author']}** ({ref['year']}). {ref['title']}. {ref['link']}")