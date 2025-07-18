import streamlit as st
import json
import random
import os
import pandas as pd
import base64

from PIL import Image

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

# Account configuration
ACCOUNTS = {
    "Rica": "Rica",
    "Nadiya": "Nadiya",
    "Jairo": "Jairo",
    "Guest": "Guest"
}

# Session initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Login page
def login():
    # Load the image
    image = Image.open("M4.png")

    # Layout with two columns
    col1, col2 = st.columns([1, 4])  # Adjust width ratio as needed

    with col1:
        st.image(image, width=200)  # Resize image if needed
    
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
    st.write("")
    st.markdown("Exclusively made. Not intended for public use.")
    st.write("")
    st.write("Works best on PC, iPad, or Tablet. It is not optimized for mobile devices yet, although it will still run.")
    st.write("For suggestions, issues, and/or corrections, please contact the developer.")

    for _ in range(3):
            st.write(" ")
    
    st.markdown(
        """
        <p style='color:#FFC0CB; font-style: italic; opacity: 1; text-align: center; font-family: "Times New Roman", serif; font-size: 20px;'>
        To God be all the glory!
        </p>
        """,
        unsafe_allow_html=True
    )

# Question display
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


# Sidebar navigation
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

# Load questions per division
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
if st.session_state.logged_in and st.session_state.username == "Rica":
    options = st.sidebar.radio(
        "Choose a section:",
        ["Home", "Mock Exam", "About", "References", "Reviewers and Notes", "NemaBot", "Timeline/Milestones", "Dedication/Letters (accessible only to Rica's account)"]
    )
    # Main logic
else:
    st.sidebar.title("Navigation")
    options = st.sidebar.radio("Choose a section:", ["Home", "Mock Exam", "About", "References", "Timeline/Milestones", "Reviewers and Notes", "NemaBot"])

if options == "Home":
    if not st.session_state.logged_in:
        login()
    else:
        st.markdown("<h2 style='margin: 0; color:#FC8EAC;'>Welcome to MTLE Review Web App</h2>", unsafe_allow_html=True)
        st.markdown(f"Hello, <span style='color:#FFC0CB; font-style:italic; font-family:Times New Roman, serif;'>{st.session_state.username}!</span> You are logged in.", unsafe_allow_html=True)
        st.write("Use the sidebar to start your exam or learn more.")
        st.write("For any issues or suggestions, please contact: daquioagjairodevon@gmail.com.")
        st.write("The contents of this app are for educational purposes only and do not reflect the actual PRC Board of Medical Technology exam in the Philippines. Always refer to official resources and consult with licensed professionals for accurate information.")
        st.write("This app used various sources, such as articles, books, and online resources. Please refer to the 'References' section for more details.")


        for _ in range(10):
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
        st.markdown("<h2 style='margin: 0; color:#FC8EAC;'>Mock Exam/Review</h2>", unsafe_allow_html=True)

        st.write("")
        st.write("Select a division:")
        div = st.selectbox("", ["Introduction", "Div 1", "Div 2", "Div 3", "Div 4", "Div 5", "Div 6", "Additional Questions"])

        st.markdown("<p style='color:#FFC0CB;'>Disclaimer: This review web app is for educational purposes only. The 'mock exam' does not directly reflect the actual questions in the MTLE. It is advised to refer to official resources and consult with licensed professionals for accurate information.</p>", unsafe_allow_html=True)
        st.write("Do not refresh or exit the browser while taking the mock exam as it will restart your progress.")

        if div == "Introduction":
            st.write("The mock exam is divided into 6 divisions, each with the same distribution of sections/questions.")
            st.write("In each division, the distribution of questions per section is as follows:")

            df_dis = pd.read_csv('d1_dis.csv')
            st.dataframe(df_dis, hide_index=True, use_container_width=True)

            st.write("The following are the topics and subtopics covered in each division, following the syllabi of the PRC Board of Medical Technology:")
            st.write("PRC Board of Medical Technology Resolution No. 15 Series of 1996: https://www.prc.gov.ph/sites/default/files/Board%20of%20Medical%20Technology%20-%20Syllabi_0.pdf")
            df_per = pd.read_csv('clinical_microscopy_per.csv')
            st.dataframe(df_per, hide_index=True, use_container_width=True, height=2487)
            st.markdown("Med Tech Notes by Doc Krizza-Almond https://krizzaalmond.com/2020/05/01/mymedtechnotesforfree/")
            st.markdown("<p style='color:#FFC0CB; font-style: italic;'>password: rmtako (Courtesy: Doc Krizza-Almond)</p>", unsafe_allow_html=True)

        elif div in ["Div 1", "Div 2", "Div 3", "Div 4", "Div 5", "Div 6", "Div 7"]:
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
                ],
                "div4": [
                    ("d4_clinical_chem.json", "Clinical Chemistry"),
                    ("d4_microb_parasi.json", "Microbiology & Parasitology"),
                    ("d4_hematology.json", "Hematology"),
                    ("d4_blood_banking.json", "Blood Banking & Serology"),
                    ("d4_clinical_microscopy.json", "Clinical Microscopy"),
                    ("d4_histopath_law_ethics.json", "Histopath, Laws & Ethics")
                ],
                "div5": [
                    ("d5_clinical_chem.json", "Clinical Chemistry"),
                    ("d5_microb_parasi.json", "Microbiology & Parasitology"),
                    ("d5_hematology.json", "Hematology"),
                    ("d5_blood_banking.json", "Blood Banking & Serology"),
                    ("d5_clinical_microscopy.json", "Clinical Microscopy"),
                    ("d5_histopath_law_ethics.json", "Histopath, Laws & Ethics")
                ],
                "div6": [
                    ("d6_clinical_chem.json", "Clinical Chemistry"),
                    ("d6_microb_parasi.json", "Microbiology & Parasitology"),
                    ("d6_hematology.json", "Hematology"),
                    ("d6_blood_banking.json", "Blood Banking & Serology"),
                    ("d6_clinical_microscopy.json", "Clinical Microscopy"),
                    ("d6_histopath_law_ethics.json", "Histopath, Laws & Ethics")
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
    st.write("The MTLE Review Web App is an interactive, self-paced mock examination and review platform designed for various purposes such as preparation for the MTLE.")
    st.markdown("<p style='color:#FFC0CB; font-style: italic;'>The development of this app was inspired by a certain individual who is currently taking a Bachelor of Science in Medical Technology program at Centro Escolar University Manila.</p>", unsafe_allow_html=True)
    st.write("For any issues or suggestions, please contact the developer.")
    st.write("This app used various sources, such as articles, books, and online resources. Please refer to the 'References' section for more details.")
    st.write("All rights reserved. This app is not affiliated with the Professional Regulation Commission (PRC) or any official medical technology board review programs.")
    st.markdown("<p style='color:#FFC0CB; font-style: italic;'>This review web app is for educational purposes only. The 'mock exam' does not directly reflect the actual questions in the MTLE. It is advised to refer to official resources and consult with licensed professionals for accurate information.</p>", unsafe_allow_html=True)
    for _ in range(2):
            st.write(" ")
    st.markdown(
        """
        <p style='color:#FFC0CB; font-style: italic; opacity: 1; text-align: center; font-family: "Times New Roman", serif; font-size: 20px;'>
        To God be all the glory!
        </p>
        """,
        unsafe_allow_html=True
    )
    for _ in range(2):
        st.write(" ")
    st.markdown(f"<p style='color:#FFC0CB; font-style: italic;'>Sincerely,<br>Devon Daquioag</p>Developer<br>AWS Academy Graduate - Data Engineering<br>Undergraduate, BSCpE<br>Centro Escolar University Manila", unsafe_allow_html=True)
    
elif options == "References":
    with open('references.json') as f:
        data = json.load(f)
        st.markdown("<h2 style='margin: 0; color:#FC8EAC;'>References</h2>", unsafe_allow_html=True)

        st.markdown("<p style='color:#FFC0CB; font-style: italic;'>This section is incomplete, there was an instance when the developer was dozing off and forgot to cite the other sources. He'll do his best to retrieve every resources used.</p>", unsafe_allow_html=True)

        st.write("")
        for ref in data["references"]:
            st.markdown(
                f"<span style='color:#cccccc;'><b>{ref['author']}</b> ({ref['year']}). {ref['title']}.</span> "
                f"<a href='{ref['link']}' target='_blank' style='color:#FC8EAC;'>{ref['link']}</a>",
                unsafe_allow_html=True
            )

elif options == "Reviewers and Notes":
    st.markdown("<h2 style='margin: 0; color: #FC8EAC;'>Reviewers and Notes</h2>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<p style='color:#FFC0CB; font-style: italic;'>Disclaimer: I do not claim ownership of any of the materials included in this website. This website is for educational purposes only and is not intended for commercial use.</p>", unsafe_allow_html=True)
    st.write("If you ever need more reference materials, you can check out the following files/links: ")
    st.markdown("1. Med Tech Notes by Doc Krizza-Almond https://krizzaalmond.com/2020/05/01/mymedtechnotesforfree/")
    st.markdown("<p style='color:#FFC0CB; font-style: italic;'>The password for Doc Krizza-Almond's PDF files is at the bottom of the Introduction section in the Mock Test Page. That's why the app requires an exclusive account to access the mock exam page. </p>", unsafe_allow_html=True)
    st.markdown("2. Other materials: https://drive.google.com/drive/u/0/folders/18eTwXcgZGYX6zsa6pnd6AbWeGZz5JNyf")
    st.markdown("<p style='color:#FFC0CB; font-style: italic;'>or</p>", unsafe_allow_html=True)

    pdf_folder = "pdfs"
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

    if pdf_files:
        selected_pdf = st.selectbox("Select a PDF to view/download:", pdf_files)

        pdf_path = os.path.join(pdf_folder, selected_pdf)

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        st.download_button(label="Download PDF", data=pdf_bytes, file_name=selected_pdf, mime="application/pdf")

        github_raw_base = "https://raw.githubusercontent.com/dvnxi/MTMLE/main/pdfs/"
        pdf_url = github_raw_base + selected_pdf

        # Use PDF.js viewer with responsive iframe
        viewer_url = f"https://mozilla.github.io/pdf.js/web/viewer.html?file={pdf_url}"

        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <iframe 
                    src="{viewer_url}" 
                    width="100%" 
                    height="700px" 
                    style="border: none; max-width: 100%;"
                ></iframe>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("No PDF files found in the folder. Please add some PDFs to display.")

elif options == "NemaBot":
    st.markdown("<h2 style='margin: 0; color:#FC8EAC;'>NemaBot is still under development</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#FFC0CB; font-style: italic;'>This feature requires intensive effort and resources like API (if necessary). Rest assured, the developer is doing his best to produce this page soon.</p>", unsafe_allow_html=True)
    st.write("In the meantime, you can try the NemaBot prototype by opening the link below. The chatbot is powered by Ollama, a local LLM server.")
    st.markdown("<p style='color:#FFC0CB;'>https://c049e17a33ae.ngrok-free.app/</p>", unsafe_allow_html=True)
    st.write("Note: If the link does not work, it means my pc is turned off or the server is not running. You can try again later or use the mainstream and powerful chatbots like ChatGPT or Copilot.")
    for _ in range(2):
            st.write(" ")
    
    st.markdown(
        """
        <p style='color:#FFC0CB; font-style: italic; opacity: 1; text-align: center; font-family: "Times New Roman", serif; font-size: 20px;'>
        To God be all the glory!
        </p>
        """,
        unsafe_allow_html=True
    )
    for _ in range(1):
        st.write(" ")
    st.markdown(f"<p style='color:#FFC0CB; font-style: italic;'>Sincerely,<br>Devon Daquioag</p>Developer<br>AWS Academy Graduate - Data Engineering<br>Undergraduate, BSCpE<br>Centro Escolar University Manila", unsafe_allow_html=True)

elif options == "Timeline/Milestones":
    st.markdown("<h2 style='margin: 0; color:#FC8EAC;'>Timeline</h2>", unsafe_allow_html=True)

    st.markdown("""
        <p style='color:#FFC0CB;'>
        The timeline below shows the key dates and events in the development of this app:
        </p>
    """, unsafe_allow_html=True)

    st.markdown("""
        <ul>
            <li>May 31, 2025 - Brainstorming</li>
            <li>June 2, 2025 - Flowcharting</li>
            <li>June 2, 2025 - Initial design and layout created.</li>
            <li>June 2, 2025 - Started gathering data </li>
            <li>June 4, 2025 - Frontend development started</li>
            <li>June 27, 2025 - Mock Question: Div 1-3 (300 Questions Accomplished *phew*)</li>
            <li>July 4, 2025 - Mock Question: Div 4 (100 Questions Accomplished)</li>
            <li>July 5, 2025 - Started developing a side feature "NemaBot" chatbot</li>
            <li>July 10, 2025 - Started developing a side feature "Lab Companion App"</li>
            <li>July 10, 2025 - Initial Testing</li>
            <li>July 11, 2025 - Put the side feature "Lab Companion App" on hold (Lack of Resources)</li>
            <li>July 11, 2025 - Backend development started</li>
            <li>July 12, 2025 - Mock Question: Div 5 (100 Questions Accomplished)</li>
            <li>July 16, 2025 - NemaBot prototype accomplished; actual feature put on hold (Lack of Resources).</li>
            <li>July 19, 2025 - Mock Question: Div 6 (100 Questions Accomplished)</li>
            <li>July 19, 2025 - Secondary Testing and Alpha Release</li>
        </ul>
    """, unsafe_allow_html=True)

elif options == "Dedication/Letters (accessible only to Rica's account)":
    st.markdown(""" 
        July 10, 2025 <br>
        Thursday, 2:52 AM <br>
                """, unsafe_allow_html=True)
    for _ in range(2):
        st.write(" ")
    st.markdown("<p style='margin: 0; color: #FFC0CB; font-family: Times New Roman, serif; font-style: italic; font-size: 18px'>Dear Rica,</p>", unsafe_allow_html=True)
    for _ in range(2):
        st.write("")
    st.markdown("""
    <p style='text-align: start;'>
        I am developing this app with the thought of you in mind.<br><br>
        I usually struggle with finding the right words to say and I might blurt out things I shouldn't so, please bear with me. <br><br>
        I hope this doesn't upset you in any way but, <br>
        I just wanted to say how much I admire everything about you—who you are now and who you're becoming,<br>
        and I would like to see you win in everything you set your mind to. <br>
        You've been such an inspiration, allowing me to do my best in everything I do, even more. I'm really grateful for that.<br>
        I made this interactive web application hoping that, however small, I may be able to support you and Nozomi in your endeavors—
        the MTLE, <br>
        and maybe even in your future as RMTs, should you decide to keep going that path. <br>
        (hopefully in your 4th year subjects too. However, I reviewed your curriculum and I don't know... was this app too late for that?) <br>
        I genuinely believe you'll do well wherever you go and in whatever you do, and I'd always be happy to cheer you on, in any way I can.<br>
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='color: #FFC0CB;'>
        I hope you find this app useful and that it helps you in every way possible. <br>
        This web app is full of imperfections and limitations so if you have any suggestions or feedback, please let me know.<br><br>
        This page will be updated frequently.<br><br>
        May you always be well, safe, and happy. <br>
        God bless!
    </p>""", unsafe_allow_html=True)

    for _ in range(1):
        st.write(" ")
    st.markdown(f"<p style='color:#FFC0CB; font-family: Times New Roman, serif; font-style: italic; font-size: 18px;'>Sincerely,<br>Jai</p>", unsafe_allow_html=True)

    for _ in range(1):
        st.write(" ")

    st.markdown("""
        P.S. <br>
        If you have ideas about a problem you wanted to be solved using technology, or if you have an idea/ideas for anything you would want to exist as a website/application, <br> 
        please let me know as it could also help me hone my skills as an engineer. I'll do my best and develop it for you.<br><br>
        """,
        unsafe_allow_html=True
    )