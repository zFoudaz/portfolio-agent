from langchain_community.document_loaders import PyPDFLoader

print()

def parse_resume(resume_path):
    loader = PyPDFLoader(file_path = resume_path)
    docs = loader.load()
    return "\n\n".join([doc.page_content for doc in docs])