import streamlit as st
import json
import random
import os
import pandas as pd
import base64

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    a, a:visited {
        color: #FFC0CB !important;
    }
    a:hover {
        color: #ffaad0 !important;
    }
    </style>
""", unsafe_allow_html=True)


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

# -------------------------
# Login page
# -------------------------
def login():
    st.markdown("<h2 style='margin: 0; color: #FC8EAC;'>Login</h2>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in ACCOUNTS and ACCOUNTS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Incorrect username or password.")

    for _ in range(20):
            st.write(" ")
    
    st.markdown(
        """
        <p style='color:#FFC0CB; font-style: italic; opacity: 1; text-align: center; font-family: "Times New Roman", serif; font-size: 20px;'>
        To God be all the glory!
        </p>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# Question display
# -------------------------
def show_question(question, disp_number, section_name, q_idx, answers, answers_key):
    st.markdown(f"<h3><span style='color:#FC8EAC;'>Question {disp_number + 1}</span> </h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:right; font-size:14px; color:gray;'>Section: {section_name}</div>", unsafe_allow_html=True)

    if "image" in question and question["image"]:
        if os.path.exists(question["image"]) and question["image"].lower() != "to_be_added":
            st.image(question["image"], use_container_width=True)

    st.write(question["question"])

    # --- Shuffle options and track correct answer ---
    options = question["options"].copy()
    correct_answer = question["answer"]

    if f"shuffled_{q_idx}" not in st.session_state:
        random.shuffle(options)
        st.session_state[f"shuffled_{q_idx}"] = options
    else:
        options = st.session_state[f"shuffled_{q_idx}"]

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

    if q_idx in answers:
        selected = answers[q_idx]
        st.radio("Your answer:", options, index=options.index(selected), disabled=True, key=f"answer_radio_{q_idx}")
        st.markdown(f"**Correct answer:** {correct_answer}")
        st.info(f"Explanation: {question.get('explanation', 'No explanation provided.')}")
    else:
        selected = st.radio("Choose your answer:", options, key=f"answer_radio_{q_idx}")

        if st.button("Confirm", key=f"confirm_{q_idx}"):
            if q_idx not in answers:
                answers[q_idx] = selected
                st.session_state[answers_key] = answers
                st.rerun()


# -------------------------
# Sidebar navigation
# -------------------------
def question_sidebar(questions, order_list, answers):
    st.sidebar.title("Questions")
    for idx, q_idx in enumerate(order_list):
        btn_label = f"Question {idx + 1}"
        if q_idx in answers:
            correct = questions[q_idx]["answer"]
            chosen = answers[q_idx]
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
                st.session_state[f"question_idx_{div_key}"] = idx
                st.rerun()

# -------------------------
# Load questions per division
# -------------------------
def load_div_questions(div_key, files_sections):
    questions_key = f"questions_{div_key}"
    order_list_key = f"order_list_{div_key}"
    section_map_key = f"section_map_{div_key}"
    answers_key = f"answers_{div_key}"
    question_idx_key = f"question_idx_{div_key}"
    completed_key = f"completed_{div_key}"

    if questions_key not in st.session_state:
        questions = []
        section_names = []
        order_list = []

        for file, sec_name in files_sections:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                sec_questions = data["questions"]
                questions.extend(sec_questions)
                section_names.extend([sec_name] * len(sec_questions))

        order_list = list(range(len(questions)))
        random.shuffle(order_list)

        st.session_state[questions_key] = questions
        st.session_state[section_map_key] = section_names
        st.session_state[order_list_key] = order_list
        st.session_state[answers_key] = {}
        st.session_state[question_idx_key] = 0
        st.session_state[completed_key] = False

    return (
        st.session_state[questions_key],
        st.session_state[order_list_key],
        st.session_state[section_map_key],
        st.session_state[answers_key],
        st.session_state[question_idx_key],
        st.session_state[completed_key]
    )

# -------------------------
# Main logic
# -------------------------
st.sidebar.title("Navigation")
options = st.sidebar.radio("Choose a section:", ["Home", "Mock Exam", "About", "References", "Reviewers and Notes"])

if options == "Home":
    if not st.session_state.logged_in:
        login()
    else:
        st.markdown("<h2 style='margin: 0; color:#FC8EAC;'>Welcome to MTLE Review Web App</h2>", unsafe_allow_html=True)
    
        # ✅ Username in flamingo pink
        st.markdown(f"Hello, <span style='color:#FFC0CB; font-style:italic; font-family:Times New Roman, serif;'>{st.session_state.username}!</span> You are logged in.", unsafe_allow_html=True)

        st.write("Use the sidebar to start your exam or learn more.")
        st.write("This app is still under development, so please check back later for more features and content.")
        st.write("For any issues or suggestions, please contact: daquioagjairodevon@gmail.com.")
        st.write("The contents of this app are for educational purposes only and do not reflect the actual PRC Board of Medical Technology exam in the Philippines. Always refer to official resources and consult with licensed professionals for accurate information.")
        st.write("This app used various sources, such as articles, books, and online resources. Please refer to the 'References' section for more details.")

        # You can remove or reduce these empty writes if you like
        for _ in range(20):
            st.write(" ")

        st.markdown(
            """
            <p style='color:#FFC0CB; font-style: italic; opacity: 1; text-align: center; font-family: "Times New Roman", serif; font-size: 20px;'>
            To God be all the glory!
            </p>
            """,
            unsafe_allow_html=True
        )

elif options == "Mock Exam":
    if not st.session_state.logged_in:
        login()
    else:
        st.markdown("<h2 style='margin: 0; color:#FC8EAC;'>MTLE Mock Exam</h2>", unsafe_allow_html=True)
        st.write("Select a division:")
        div = st.selectbox("", ["Introduction", "Div 1", "Div 2", "Div 3", "Div 4", "Div 5", "Div 6"])

        st.markdown("<p style='color:#FFC0CB;'>Disclaimer: This review web app is for educational purposes only. The 'mock exam' does not directly reflect the actual questions in the MTLE. It is advised to refer to official resources and consult with licensed professionals for accurate information.</p>", unsafe_allow_html=True)

        if div == "Introduction":
            st.write("The developer divided the mock exam into 6 divisions, each with the same distribution of sections/questions.")
            st.write("It is impractical to cram all the questions into one division. It's hard to debug and manage a large number of questions in a single JSON file.")
            st.write("In each division, the distribution of questions per section is as follows:")

            df_dis = pd.read_csv('d1_dis.csv')
            st.dataframe(df_dis, hide_index=True, use_container_width=True)

            st.write("The following are the topics and subtopics covered in each division, based on the syllabi of the PRC Board of Medical Technology:")
            st.write("This data is based on PRC Board of Medical Technology Resolution No. 15 Series of 1996: https://www.prc.gov.ph/sites/default/files/Board%20of%20Medical%20Technology%20-%20Syllabi_0.pdf")
            df_per = pd.read_csv('clinical_microscopy_per.csv')
            st.dataframe(df_per, hide_index=True, use_container_width=True, height=2487)
            st.markdown("<p style='color:#FFC0CB; font-style: italic;'>password: rmtako (huge thanks to Doc Krizza-Almond)</p>", unsafe_allow_html=True)

        elif div in ["Div 1", "Div 2", "Div 3"]:
            div_key = div.lower().replace(" ", "")
            files_map = {
                "div1": [
                    ("d1_clinical_chem.json", "Clinical Chemistry"),
                    ("d1_microb_parasi.json", "Microbiology & Parasitology"),
                    ("d1_hematology.json", "Hematology"),
                    ("d1_blood_banking.json", "Blood Banking & Serology"),
                    ("d1_clinical_microscopy.json", "Clinical Microscopy"),
                    ("d1_histopath_law_ethics.json", "Histopath, Laws & Ethics")
                ],
                "div2": [
                    ("d2_clinical_chem.json", "Clinical Chemistry"),
                    ("d2_microb_parasi.json", "Microbiology & Parasitology"),
                    ("d2_hematology.json", "Hematology"),
                    ("d2_blood_banking.json", "Blood Banking & Serology"),
                    ("d2_clinical_microscopy.json", "Clinical Microscopy"),
                    ("d2_histopath_law_ethics.json", "Histopath, Laws & Ethics")
                ],
                "div3": [
                    ("d3_clinical_chem.json", "Clinical Chemistry"),
                    ("d3_microb_parasi.json", "Microbiology & Parasitology"),
                    ("d3_hematology.json", "Hematology"),
                    ("d3_blood_banking.json", "Blood Banking & Serology"),
                    ("d3_clinical_microscopy.json", "Clinical Microscopy"),
                    ("d3_histopath_law_ethics.json", "Histopath, Laws & Ethics")
                ]
            }

            questions, order_list, section_names, answers, question_idx, completed = load_div_questions(div_key, files_map[div_key])

            question_sidebar(questions, order_list, answers)

            if completed:
                st.success(f"You finished {div}!")
                score = sum(1 for idx, ans in answers.items() if ans == questions[order_list[idx]]["answer"])
                st.write(f"Your score: {score}/{len(questions)}")
            else:
                current_q_idx = question_idx
                if current_q_idx < len(order_list):
                    actual_idx = order_list[current_q_idx]
                    section_name = section_names[actual_idx]
                    show_question(questions[actual_idx], current_q_idx, section_name, actual_idx, answers, f"answers_{div_key}")

                    if st.button("Next"):
                        if current_q_idx + 1 < len(order_list):
                            st.session_state[f"question_idx_{div_key}"] += 1
                        else:
                            st.session_state[f"completed_{div_key}"] = True
                        st.rerun()

                    prev_unanswered = None
                    for i in range(current_q_idx - 1, -1, -1):
                        if order_list[i] not in answers:
                            prev_unanswered = i
                            break
                    if prev_unanswered is not None:
                        if st.button("Previous"):
                            st.session_state[f"question_idx_{div_key}"] = prev_unanswered
                            st.rerun()
                    else:
                        st.button("Previous", disabled=True)

        else:
            st.info(f"{div} content coming soon! Please check back later.")

elif options == "About":
    st.markdown("<h2 style='margin: 0; color:#FC8EAC;'>About</h2>", unsafe_allow_html=True)
    
    st.write("Developed by Devon Daquioag, a Computer Engineering undergraduate from Centro Escolar University, Manila.")
    st.markdown("<p style='color:#FFC0CB; font-style: italic;'>The development of this app was inspired by a certain someone who is currently taking a Bachelor of Science in Medical Technology program at Centro Escolar University Manila, Philippines.</p>", unsafe_allow_html=True)
    st.write("This app is still under development (<30%), so please check back later for more features and content.")
    st.write("For any issues or suggestions, please contact: daquioagjairo30@gmail.com.")
    st.write("This app used various sources, such as articles, books, and online resources. Please refer to the 'References' section for more details.")
    st.write("All rights reserved. This app is not affiliated with the Professional Regulation Commission (PRC) or any official medical technology board review programs.")

    st.markdown("<p style='color:#FFC0CB;'>Disclaimer: This review web app is for educational purposes only. The 'mock exam' does not directly reflect the actual questions in the MTLE. It is advised to refer to official resources and consult with licensed professionals for accurate information.</p>", unsafe_allow_html=True)
    for _ in range(15):
            st.write(" ")
    
    st.markdown(
        """
        <p style='color:#FFC0CB; font-style: italic; opacity: 1; text-align: center; font-family: "Times New Roman", serif; font-size: 20px;'>
        To God be all the glory!
        </p>
        """,
        unsafe_allow_html=True
    )


elif options == "References":
    with open('references.json') as f:
        data = json.load(f)
        st.markdown("<h2 style='margin: 0; color:#FC8EAC;'>References</h2>", unsafe_allow_html=True)
        for ref in data["references"]:
            st.markdown(
                f"<span style='color:#cccccc;'><b>{ref['author']}</b> ({ref['year']}). {ref['title']}.</span> "
                f"<a href='{ref['link']}' target='_blank' style='color:#FC8EAC;'>{ref['link']}</a>",
                unsafe_allow_html=True
            )
 

elif options == "Reviewers and Notes":
    st.markdown("<h2 style='margin: 0; color: #FC8EAC;'>Reviewers and Notes</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#FFC0CB;'>Disclaimer: I do not claim ownership of any of the materials included in this website. This website is for educational purposes only and is not intended for commercial use.</p>", unsafe_allow_html=True)
    st.write("If you ever need more reference materials, you can check out the following files/links: ")
    st.markdown("<p style='color:#FFC0CB; font-style: italic;'>link(s) at the bottom of the page</p>", unsafe_allow_html=True)

    pdf_folder = r"C:\Users\Jairo\Documents\MT Mock Board Review\pdfs"  # Change this to your actual folder

    # ✅ List all PDF files in the folder
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

    if pdf_files:
        selected_pdf = st.selectbox("Select a PDF to view/download:", pdf_files)

        pdf_path = os.path.join(pdf_folder, selected_pdf)

        # Read bytes
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        # Download button
        st.download_button(label="Download PDF", data=pdf_bytes, file_name=selected_pdf, mime="application/pdf")

        # Embed PDF viewer (centered & fullscreen enabled)
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f"""
            <div style="display: flex; justify-content: center;">
                <iframe 
                    src="data:application/pdf;base64,{base64_pdf}" 
                    width="1500" 
                    height="1000" 
                    type="application/pdf"
                    allowfullscreen
                    style="border: none;"
                ></iframe>
            </div>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
        st.write(" ")
        st.write("1. Med Tech Notes by Doc Krizza-Almond https://krizzaalmond.com/2020/05/01/mymedtechnotesforfree/")
        st.markdown("<p style='color:#FFC0CB; font-style: italic;'>The password for Doc Krizza-Almond's PDF files is at the bottom of the Introduction section in the Mock Test Page.</p>", unsafe_allow_html=True)
        st.write("That's why the app requires an exclusive account to access the mock exam page. ")

    else:
        st.warning("No PDF files found in the folder. Please add some PDFs to display.")