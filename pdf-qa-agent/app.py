
import argparse
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

load_dotenv()

llm = Groq(
    model="llama-3.3-70b-versatile",
    temperature=0.4,
)



Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def build_index_from_pdf(pdf_path:str)->VectorStoreIndex:
    """
    Build a vector store index from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.
    """

    reader = SimpleDirectoryReader(input_files=[pdf_path])
    documents = reader.load_data()
    index=VectorStoreIndex.from_documents(documents)
    return index

def Q_A_from_pdf(index:VectorStoreIndex):
    memory=ChatMemoryBuffer.from_defaults(token_limit=4096)

    chat_engine=index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        llm=llm,
        verbose=False)

    print("\n PDF Q&A Agent ready. Type 'quit' to exit.\n")

    while True:
        Query=input("Enter your question: ")
        if Query.lower() in ["quit", "exit"]:
            print("Exiting PDF Q&A Agent.")
            break
        if not Query:
            print("Please enter a valid question.")
            continue

        res=chat_engine.chat(Query)
        print(f"\nAgent: {res.response}\n")

def from_pdf(index:VectorStoreIndex,Query:str):
    """
    Start the Q&A session from a PDF file.

    Args:
        vectorstore_index (VectorStoreIndex): The vector store index built from the PDF.
    """
    query_engine = index.as_query_engine(
    llm=llm,
    similarity_top_k=5,)
    res=query_engine.query(Query)
    print("\n" + "=" * 60)
    print("📋 ANSWER")
    print("=" * 60)
    print(res.response)
    if hasattr(res, "source_nodes"):
        print(f"\n📚 Sources: {len(res.source_nodes)} chunk(s) referenced")



def main():
    parser=argparse.ArgumentParser(description="PDF Q&A Agent")
    parser.add_argument("--pdf", type=str, required=True, help="Path to the PDF file")
    parser.add_argument("--query", type=str, help="Question to ask about the PDF")
    args=parser.parse_args()

    index=build_index_from_pdf(args.pdf)

    if args.query:
        from_pdf(index, args.query)
    else:
        Q_A_from_pdf(index)

if __name__ == "__main__":
    main()

