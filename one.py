import os
import fitz  # PyMuPDF
import openai
import sys

# Set up OpenAI API key
openai.api_key = 'set your api key'

def extract_text_from_pdf(pdf_path):
    try:
        # Open the PDF document
        document = fitz.open(pdf_path)
        text = ""

        # Iterate through each page
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()

        return text
    except Exception as e:
        print(f"Error reading PDF file '{pdf_path}': {e}")
        return None

def process_text_with_openai(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that processes text extracted from PDFs."},
                {"role": "user", "content": text}
            ],
            max_tokens=500  # Adjust max_tokens to a lower value
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error processing text with OpenAI: {e}")
        return None

def create_data_model(file_path, extracted_text, processed_text):
    data_model = {
        'file_path': file_path,
        'extracted_text': extracted_text,
        'processed_text': processed_text
    }
    return data_model

def main():
    # Replace with the path to your single PDF file
    pdf_path = r'C:\Users\Vidhyasri\Downloads\Documents.pdf'

    try:
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"File '{pdf_path}' not found.")

        extracted_text = extract_text_from_pdf(pdf_path)
        if extracted_text:
            processed_text = process_text_with_openai(extracted_text)
            if processed_text:
                data_model = create_data_model(pdf_path, extracted_text, processed_text)
                print(f"File Processed: {pdf_path}")
                print(f"Data Model:")
                print(f"File Path: {data_model['file_path']}")
                print(f"Extracted Text: {data_model['extracted_text'][:500]}")  # Display first 500 characters
                sys.stdout.reconfigure(encoding='utf-8')  # Set stdout encoding to utf-8
                print(f"Processed Text: {data_model['processed_text']}")
            else:
                print(f"Failed to process text with OpenAI for file: {pdf_path}")
        else:
            print(f"Failed to extract text from PDF: {pdf_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
