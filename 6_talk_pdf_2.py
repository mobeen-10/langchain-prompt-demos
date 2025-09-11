# SIMPLE DOCUMENT CHAT - MINIMAL DEMO
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from helpers import get_llm

# 1. LOAD PDF
loader = PyPDFLoader("pdfs/nelson.pdf")
pages = loader.load()
document = "\n\n".join([page.page_content for page in pages])

# 2. CREATE CHUNKS
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_text(document)

# 3. ASK QUESTIONS
llm = get_llm()
context = "\n\n".join(chunks)

def ask(question):
    prompt = f"Document: {context}\n\nQuestion: {question}"
    response = llm.invoke(prompt)
    return response.content

# 4. INTERACTIVE CHAT
print("Ask questions about the document (type 'quit' to exit):")
while True:
    question = input("\nQuestion: ")
    if question.lower() == 'quit':
        break
    answer = ask(question)
    print(f"Answer: {answer}")
