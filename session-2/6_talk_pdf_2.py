from langchain_community.document_loaders import PyPDFLoader
from helpers import get_llm

# 1. LOAD PDF
loader = PyPDFLoader("pdfs/nelson.pdf")
pages = loader.load()
document = "\n\n".join([page.page_content for page in pages])

# 2. ASK QUESTIONS
llm = get_llm()

def ask(question):
    prompt = f"Document: {document}\n\nQuestion: {question}"
    response = llm.invoke(prompt)
    return response.content

# 3. INTERACTIVE CHAT
print("Ask questions about the document (type 'quit' to exit):")
while True:
    question = input("\nQuestion: ")
    if question.lower() == 'quit':
        break
    answer = ask(question)
    print(f"Answer: {answer}")
