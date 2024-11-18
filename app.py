import streamlit as st
from openai import OpenAI
import PyPDF2
from io import BytesIO
import time

# Initialize OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Get Assistant ID from secrets
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# Configure Streamlit page
st.set_page_config(
    page_title="PDF Journal Creator",
    page_icon="📚",
    layout="wide"
)

def extract_text_from_pdf(pdf_file):
    """Extract text content from uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.getvalue()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def process_pdf_content(pdf_content):
    """Process PDF content using OpenAI Assistant"""
    try:
        # Create a thread
        thread = client.beta.threads.create()
        
        # Add the PDF content as a message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Please create a journal entry based on the following content: {pdf_content}"
        )
        
        # Create and run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )
        
        # Wait for completion
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            elif run_status.status == 'failed':
                raise Exception("Assistant failed to process the content")
            elif run_status.status == 'expired':
                raise Exception("Request expired")
            time.sleep(1)
        
        # Get the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
    
    except Exception as e:
        st.error(f"Error in processing content: {str(e)}")
        return None

def main():
    st.title("📚 PDF Journal Creator")
    st.write("Upload a PDF and let AI create a structured journal entry!")
    
    # Add GitHub repository link
    st.sidebar.markdown("### About")
    st.sidebar.markdown(
        "This app uses OpenAI's Assistant API to create journal entries from PDF documents. "
        "View the source code on [GitHub](https://github.com/yourusername/pdf-journal-creator)."
    )
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Display PDF info
        st.info(f"Uploaded: {uploaded_file.name}")
        
        if st.button("Create Journal", type="primary"):
            try:
                # Create expander for PDF content
                with st.expander("PDF Content"):
                    with st.spinner("Extracting text from PDF..."):
                        pdf_content = extract_text_from_pdf(uploaded_file)
                        st.text_area("Extracted Text", pdf_content, height=200)
                
                # Process with OpenAI Assistant
                with st.spinner("Creating journal entry..."):
                    journal_entry = process_pdf_content(pdf_content)
                    
                    if journal_entry:
                        # Display journal entry in a nice format
                        st.subheader("📝 Journal Entry")
                        st.markdown(journal_entry)
                        
                        # Add download button for the journal entry
                        st.download_button(
                            label="Download Journal Entry",
                            data=journal_entry,
                            file_name="journal_entry.txt",
                            mime="text/plain"
                        )
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Please try again or contact support if the problem persists.")

if __name__ == "__main__":
    main()
