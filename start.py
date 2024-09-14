import streamlit as st
from PIL import Image
import pytesseract
import ollama

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'PATH'

def main():
    st.title("Safe Label")

    st.header("Know What You Consume")

    st.write("Our app lets you uncover the truth behind every product you consume. Simply upload a picture of the ingredient list, and we’ll tell you whether it's good or bad for your health. Empower your choices by understanding what's really in the products you use every day.")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open and display the image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Extract text from image
        extracted_text = pytesseract.image_to_string(image)

        # Display the extracted text
        st.subheader("Result")
        # st.write(extracted_text)

        # Call Ollama to get details about the ingredients
        stream = ollama.chat(
            model='llama3.1',
            messages=[{
                'role': 'user', 
                'content': f'PROMPT'
            }],
            stream=True,
        )

        # Create a placeholder for the result
        result_placeholder = st.empty()
        
        # Collect and display the result from Ollama 
        # st.subheader("Result")
        result_content = ""
        for chunk in stream:
            result_content += chunk['message']['content']  # Accumulate content
            
            # Update the placeholder with the current content
            result_placeholder.markdown(f"<div style='width: 100%;'>{result_content}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()