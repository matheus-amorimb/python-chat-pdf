import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv, find_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from streamlit import Site 

def main():
    # Load environment variables from .env file
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    # Get the OpenAI API key
    my_openai_api_key = os.getenv('MY_OPENAI_API_KEY')

    # Set the OpenAI API key as an environment variable
    os.environ['OPENAI_API_KEY'] = my_openai_api_key

    # Create a Site instance
    my_site = Site()

    # Get the user's query
    query = my_site.query

    if my_site.pdf_file and query:
        # Read the PDF file
        reader = PdfReader(my_site.pdf_file)

        raw_text = ''
        for i, page in enumerate(reader.pages):
            content = page.extract_text()
            if content:
                raw_text += f'\n\n Page {i} \n\n {content}'

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            separators='\n',
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(raw_text)

        # Create OpenAI embeddings
        embeddings = OpenAIEmbeddings()
        doc_search = FAISS.from_texts(chunks, embeddings)

        # Initialize ChatOpenAI and the QA chain
        llm = ChatOpenAI(model='gpt-3.5-turbo')
        chain = load_qa_chain(llm=llm, chain_type='stuff')

        # Search for similar documents and get an answer to the query
        docs = doc_search.similarity_search(query)
        answer = chain.run(input_documents=docs, question=query)

        # Display the answer using the Site class
        Site.display_response(answer)

if __name__ == '__main__':
    main()