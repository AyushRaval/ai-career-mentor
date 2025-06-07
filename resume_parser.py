import fitz #pyMuPDF
def parse_resume(uploaded_file):
    with fitz.open(stream=uploaded_file.read(),filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text