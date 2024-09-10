import pdfplumber

def read_pdf(file_path):
    # Open the PDF file
    with pdfplumber.open(file_path) as pdf:
        # Initialize a variable to store all the text
        text = ""
        
        # Iterate through all the pages and extract text
        for page in pdf.pages:
            text += page.extract_text()
        
        return text

# Example usage
pdf_file_path = r"C:\Users\Allys\source\repos\dotnet-course\dotnet\books\Ultimate ASP.NET Core Web API - Premium.pdf"  # Replace with your PDF file path
#pdf_text = read_pdf(pdf_file_path)
#print(pdf_text)

####

print("Part 2")

import PyPDF2

def read_pdf(file_path):
    # Open the PDF file in binary mode
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Initialize a variable to store all the text
        text = ""

        # Iterate through all the pages and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        
        return text

# Example usage
#pdf_file_path = "example.pdf"  # Replace with your PDF file path
#pdf_text = read_pdf(pdf_file_path)
#print(pdf_text)


import pdfplumber

def extract_text_from_pdf(file_path):
    # Open the PDF file
    with pdfplumber.open(file_path) as pdf:
        # Initialize a variable to store all the text
        full_text = []
        
        # Iterate through all the pages and extract text
        for page_num, page in enumerate(pdf.pages):
            # Extract text from the current page
            page_text = page.extract_text()
            if page_text:
                full_text.append(page_text)
            else:
                # If no text is extracted, attempt to use a different method (like table extraction)
                print(f"Warning: No text found on page {page_num + 1}.")
                # Optionally, try extracting tables or other elements here
                # tables = page.extract_tables()  # Uncomment to extract tables
                # if tables:
                #     # Handle the tables or add to the text in a structured way
                #     for table in tables:
                #         full_text.append("\n".join(["\t".join(row) for row in table]))
        
        # Join all the text into a single string
        return "\n".join(full_text)

# Example usage
#df_file_path = "example.pdf"  # Replace with your PDF file path
pdf_text = extract_text_from_pdf(pdf_file_path)

# Write the extracted text to a text file (optional)
with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
    text_file.write(pdf_text)

print("Text extraction complete.")
