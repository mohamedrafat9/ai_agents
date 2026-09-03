from .test import ch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

chunk1, chunk2 = ch()

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

docsearch = Chroma.from_documents(
    documents=chunk1,
    embedding=embedding_model,
    collection_name="langchain_docs"
)

query = "LangChain"

docs = docsearch.similarity_search(
    query,
    k=3
)

for i, doc in enumerate(docs, start=1):

    print(f"\n===== Result {i} =====")

    print(doc.page_content)

    print("\nMetadata:")
    print(doc.metadata)