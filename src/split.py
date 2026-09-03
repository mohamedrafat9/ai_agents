from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter

loader = PyPDFLoader(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain." \
    "cloud/96-FDF8f7coh0ooim7NyEQ/langchain-paper.pdf"
    )
document = loader.load()

loaderweb = WebBaseLoader(
    "https://python.langchain.com/v0.2/docs/introduction/"
)

web_data = loaderweb.load()

text_splitter = CharacterTextSplitter(
    chunk_size=200, 
    chunk_overlap=20,
    separator="\n"
    )
chunks = text_splitter.split_documents(document)
