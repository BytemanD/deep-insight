"""
企业私有知识库问答系统
支持 PDF、TXT、DOCX 文档，自动向量化存储
"""

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_community.document_loaders import ObsidianLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

# 假设你的Markdown文件存放在 './documents' 目录下
loader = ObsidianLoader("./documents")
# 加载所有Markdown文件
documents = loader.load()


embeddings = OpenAIEmbeddings(model="text-embedding-v1")

vectorstore = Chroma.from_documents(
    documents, embedding=embeddings, persist_directory="./chroma_db"
)


retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True   # 可选：返回引用的源文档
)


qa_chain("What are autonomous agents?")

