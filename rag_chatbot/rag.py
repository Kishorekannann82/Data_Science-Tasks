import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
load_dotenv()
llm=ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)
embeddings=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
prompt=ChatPromptTemplate.from_template(
    """ 
    Answer the question only using the provided context.
    Context:
    {context}
    Question:
    {question}
    """
)
parser=StrOutputParser()
def ask_rag(file_path,question):
    if file_path.endswith(".pdf"):
        loader=PyPDFLoader(file_path)
    elif file_path.endswith(".csv"):
        loader=CSVLoader(file_path=file_path)
    else:
        return "Unsupported File Content"
    documents=loader.load()
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    split_docs=splitter.split_documents(
        documents
    )
    vector_store=Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings
    )
    retriever=vector_store.as_retriever()
    retrieved_docs=retriever.invoke(
        question
    )
    context="\n\n".join(
        doc.page_content for doc in retrieved_docs
    )
    chain=prompt|llm|parser
    response=chain.invoke(
        {
            "context":context,
            "question":question
        }
    )
    return response
