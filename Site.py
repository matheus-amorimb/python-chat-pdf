import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

class Site:
    def __init__(self):
        self.side_bar()
        self.title = st.title('Chat with PDF')
        self._pdf_file = reader = st.file_uploader('Upload your PDF', type='pdf')
        self._input = st.text_input('Ask a question related to your PDF file:')
        self._response = None

    def side_bar(self):
        with st.sidebar:
            st.title('PDF Reader Chat App')
            add_vertical_space(2)
            text = """
            <p style="text-align: justify;">
            The PDF Reader Chat App is a web-based application designed to facilitate seamless interaction with PDF documents. It harnesses the power of LangChain, OpenAI, and Streamlit to provide an efficient and user-friendly platform for reading and querying the content of PDF files. This application serves as a versatile tool for individuals and professionals seeking quick answers or insights from PDF documents.
            </p>
            """
            st.markdown(text, unsafe_allow_html=True)
            add_vertical_space(15)
            st.write('Made by [Matheus Amorim](https://github.com/matheus-amorimb/chat-pdf.git)')       

    @property
    def pdf_file(self):
        return self._pdf_file
    
    @property
    def query(self):
        return self._input

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    @staticmethod
    def display_response(value):
        st.write(value)