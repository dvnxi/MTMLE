import os
from pdf_utils import extract_text_from_pdf, split_text
from vector_utils import create_vectorstore, save_vectorstore

pdf_folder = "ai_trainer_pdfs"
all_text = ""

for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        text = extract_text_from_pdf(pdf_path)
        all_text += text + "\n"

chunks = split_text(all_text)

print(f"Total chunks: {len(chunks)}")

vectorstore = create_vectorstore(chunks)
save_vectorstore(vectorstore, path="faiss_index")
print("✅ Vector store created and saved!")