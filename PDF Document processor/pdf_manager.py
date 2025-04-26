"""   
    This module helps to manipulate pdf documents.
    Read, extract content(page number, text, image, table), split, merge, rotate, watermark)
    use visitor function for partial extraction. 
    It is used for reading PDF files.
    It is used for extracting text and metadata.
    It is used for merging, splitting, and rotating pages.
    It is used for encrypting and decrypting PDF files.
    It is also used for making and adding watermarks and modifying PDF content.           
"""
# Necessary modules
from PyPDF2 import PdfReader, PdfWriter
from typing import Dict, Optional
import os
from pathlib import Path
import pikepdf
from pikepdf import PasswordError, Pdf
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.pdfgen import canvas
 
# class to manage pdf files   
class PDF_manager:   
    # Possible choices for pdf manipulation
    choices = [
        "Page count and text extraction",
        "display pdf metadata",
        "Split PDF document",
        "Merge pdf documents",
        "rotate pdf document",
        "Encrypt pdf document with AES 256",
        "Decrypt pdf document",
        "Extract images",
        "crop pdf document",
        "watermark pdf document"        
    ]
        
    # Open the pdf file for reading, page count, and text extraction.
    def read_pdf_document(self, filename: str) -> tuple:
        """
        Reads a PDF document, counts the number of pages, and extracts text from each page.

        Args:
            filename (str): Path to the PDF file.

        Returns:
            tuple: A tuple containing:
                - pages_count (int): Total number of pages in the PDF.
                - pages_content (list): A list of tuples where each tuple contains:
                    - page_number (int): The page number (starting from 1).
                    - text (str): The extracted text from the page.
        """
        # Variables to return
        pages_content = []  # List of tuples for page number and text
        pages_count = 0  # Total number of pages

        try:
            with open(filename, "rb") as pdf_file:
                reader = PdfReader(pdf_file)
                
                # Get the total number of pages
                pages_count = len(reader.pages)
                
                # Read the content of all pages
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    pages_content.append((i + 1, text))  # Page numbers start from 1

        except Exception as e:
            print(f"An error occurred while reading the PDF: {e}")
            return (0, [])
       
        return (pages_count, pages_content)

                   
    # open pdf file for metadata extraction   
    def display_pdf_metadata(self, filename: str) -> Dict[str, Optional[str]]:
        """
        Extracts and displays metadata from a PDF file.

        Args:
            filename (str): Path to the PDF file.

        Returns:
            Dict[str, Optional[str]]: A dictionary containing the PDF metadata.
                Keys: "creator", "producer", "subject", "author", "title", "creation_date".
                Values: Corresponding metadata values (or None if not available).
        """
        # Dictionary to contain the metadata
        metadatas = {
            "creator": None,
            "producer": None,
            "subject": None,
            "author": None,
            "title": None,
            "creation_date": None,
        }

        try:
            with open(filename, "rb") as pdf_file:
                reader = PdfReader(pdf_file)
                
                # Extract metadata
                metadata = reader.metadata
                
                # Populate the metadata dictionary
                if metadata:
                    metadatas["creator"] = metadata.get("/Creator")
                    metadatas["producer"] = metadata.get("/Producer")
                    metadatas["subject"] = metadata.get("/Subject")
                    metadatas["author"] = metadata.get("/Author")
                    metadatas["title"] = metadata.get("/Title")
                    metadatas["creation_date"] = metadata.get("/CreationDate")

        except Exception as e:
            print(f"An error occurred while reading the PDF: {e}")
            return metadatas
        
        return metadatas
        ## End display_metadata() function ##
 
    # splitting pdf document and create a list of splitted files.
    def splitting_pdf_document(self, filename: str) -> list:
        """
        Splits a PDF document into individual pages and saves each page as a separate PDF file.

        Args:
            filename (str): Path to the input PDF file.

        Returns:
            list: A list of file paths for the split PDF files.
        """
        splitted_files = []  # List to store paths of the split PDF files
        
        # Create the output directory if it doesn't exist
        os.makedirs("./treated_documents", exist_ok=True)

        try:
            with open(filename, 'rb') as pdf_file:
                reader = PdfReader(pdf_file)
                
                print(f"Splitting PDF file: {filename}")
                print(f"Number of pages: {len(reader.pages)}")

                for i, page in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)

                    # Create a new filename for the split PDF
                    base_name = os.path.basename(filename)  # Extract the file name (e.g., "document.pdf")
                    name_without_ext = os.path.splitext(base_name)[0]  # Remove the extension (e.g., "document")
                    new_filename = f'./treated_documents/{name_without_ext}_page_{i + 1}.pdf'

                    # Save the new PDF file
                    with open(new_filename, 'wb') as output_pdf:
                        writer.write(output_pdf)
                        
                    # Add the new file path to the list
                    splitted_files.append(new_filename)  

        except Exception as e:
            print(f"An error occurred while splitting the PDF: {e}")
            return []

        print(f"Split files list length: {len(splitted_files)}")
        
        return splitted_files
    ## End function ##
    
    # Merging  pdf documents with PdfWriter    
    def merge_pdf_documents(self, file_list: list, output_filename: str ) -> None:
        """
        Merges multiple PDF documents into a single PDF file.

        Args:
            file_list (list): List of file paths for the PDFs to merge.
            output_filename (str): Path to save the merged PDF file..
        """
        # Create a PDF writer
        pdf_writer = PdfWriter()
        try:
            # Add PDFs to merge
            for pdf_file in file_list:
                print(f"Adding {pdf_file} to the merge list...")
                # create a reader for each page to merge
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    pdf_writer.add_page(page) # each page read is added to the writer object.

            # Save the merged PDF
            os.makedirs(os.path.dirname(output_filename), exist_ok=True)  # Create output directory if it doesn't exist
            with open(output_filename, 'wb') as output_file:
                pdf_writer.write(output_file)

            print(f"Merged PDF saved as {output_filename}")

        except Exception as e:
            print(f"An error occurred while merging PDFs: {e}")                    
    ## End merge function
        
    # Rotating pdf documents
    def rotate_pdf(self, input_pdf_path: str, output_pdf_path: str, rotation_angle: float) -> None:
        # Open the PDF file
        with open(input_pdf_path, 'rb') as file:
            reader = PdfReader(file)
            writer = PdfWriter()

            # Iterate through each page and rotate it
            for page in reader.pages:
                page.rotate(rotation_angle)
                writer.add_page(page)

            # Write the rotated pages to a new PDF
            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)
            ## End rotate_pdf function
                     
    # Encrypts a PDF file using AES-256 encryption more secure for sensitive data than PyPDF2 AES-128
    # Require the installation of pikepdf module 
    def encrypt_pdf_aes256(self, filename: str) -> None:
        """
        Encrypts a PDF file using AES-256 encryption.

        Args:
            filename (str): Path to the input PDF file.
        """
        # Prompt user for password
        password = input("Enter your password: ")

        try:
            # Open the PDF
            with Pdf.open(filename) as pdf:
                # Prompt user for output file path
                output_pdf_path = input("Enter the output PDF document path: ")

                # Encrypt the PDF with AES-256
                pdf.save(
                    output_pdf_path,
                    encryption=pikepdf.Encryption(
                        owner=password,  # Owner password (for permissions)
                        user=password,   # User password (to open the file)
                        R=6,             # Use AES-256 encryption (R=6)
                    ),
                )
                print(f"PDF encrypted with AES-256 and saved as {output_pdf_path}")

        except PasswordError as e:
            print(f"Password error: {e}")
        except FileNotFoundError:
            print(f"Error: The file '{filename}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
        ## End function 
                        
   
    # decrypting pdf
    def decrypt_pdf_aes256(self, filename: str) -> None:
        """
            Decrypts a PDF file encrypted with AES-256.

            Args:
                filename (str): Path to the encrypted PDF file.
        """
        # Prompt user for password
        password = input("Enter the password to decrypt the PDF: ")

        try:
            # Open the encrypted PDF
            with Pdf.open(filename, password=password) as pdf:
                # Prompt user for output file path
                output_pdf_path = input("Enter the output PDF document path: ")

                # Save the decrypted PDF
                pdf.save(output_pdf_path)
                print(f"PDF decrypted and saved as {output_pdf_path}")

        except PasswordError:
            print("Error: Incorrect password. Decryption failed.")
        except FileNotFoundError:
            print(f"Error: The file '{filename}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
        ## End of function ##
            
    # extract images from pdf documents
    def extract_images_from_pdf(self, filename: str, output_dir: str = "extracted_images") -> None:
        """
            Extracts images from a PDF document and saves them to a specified directory.
            Args:
                filename (str): Path to the PDF file.
                output_dir (str): Directory to save the extracted images. Defaults to "extracted_images".
        """
        # Create the output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate PDF file reader
        try:
            reader = PdfReader(filename)
        except Exception as e:
            print(f"Failed to read the PDF file: {e}")
            return

        print(f"PDF document contains {len(reader.pages)} pages to search for images.")

        total_images_extracted = 0

        # Iterate through each page in the PDF
        for page_num, page in enumerate(reader.pages, start=1):
            print(f"Processing page {page_num}...")
            image_count = 0  # Image count for the current page

            # Iterate through each image in the page
            for image_file_object in page.images:
                try:
                    # Create a unique filename for the image
                    image_filename = f"page{page_num}_image{image_count}_{image_file_object.name}"
                    image_path = output_path / image_filename

                    # Save the image to the output directory
                    with open(image_path, "wb") as fp:
                        fp.write(image_file_object.data)
                        print(f"Image saved: {image_filename}")
                        image_count += 1
                        total_images_extracted += 1
                except Exception as e:
                    print(f"Failed to save image {image_file_object.name} from page {page_num}: {e}")
        print(f"Extraction complete. Total images extracted: {total_images_extracted}")
            
    # Cropping pdf document
    def cropping_pdf_document(self, filename: str) -> None:
        # filename access
        filename = input("Enter the filename of the pdf document: ")
        # Reading the pdf file
        reader = PdfReader(filename)
        writer = PdfWriter()

        # add page 1 from reader to output document, unchanged:
        writer.add_page(reader.pages[0])

        # add page 2 from reader, but rotated clockwise 90 degrees:
        writer.add_page(reader.pages[1].rotate(90))

        # add page 3 from reader, but crop it to half size:
        page3 = reader.pages[2]
        page3.mediabox.upper_right = (
            page3.mediabox.right / 2,
            page3.mediabox.top / 2,
        )
        writer.add_page(page3)
        writer.add_js("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")
        ## End of the function croppin_pdf_document() ##
        
    # Create a watermark pdf page   
    def create_watermark_pdf(self, text: str) -> BytesIO:
        "Create a PDF with the watermark text."
        # Create a canvas
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # Set font, size, and opacity of the watermark text
        can.setFont("Helvetica", 50)
        can.setFillColorRGB(0.5, 0, 0, alpha=0.3)  # Gray color with 30% opacity
        
        # Calculate the center of the page
        page_width, page_height = letter
        text_width = can.stringWidth(text, "Helvetica", 50)
        text_height = 50  # Approximate height of the text
        
        # Rotate the text and position it in the center of the canvas
        can.saveState()
        can.translate(page_width / 2, page_height / 2)  # Move to the center of the page
        can.rotate(45)  # Rotate the text
        can.drawString(-text_width / 2, -text_height / 2, text)  # Draw the watermark text centered
        can.restoreState()
        
        # saving canvas
        can.save()
        packet.seek(0)
        return packet
    
    # adding watermark to pdf pages
    def add_watermark(self, input_pdf_path, output_pdf_path):
        # Create the watermark PDF
        watermark_text = input("Type watermark text here: ")
        watermark_pdf = self.create_watermark_pdf(watermark_text)
        
        # Add the watermark to each page of the input PDF.
        # retrieve watermark page
        watermark_reader = PdfReader(watermark_pdf)
        watermark_page = watermark_reader.pages[0]

        # retrieveing pdf document to watermark
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        # Watermark each page of the original pdf document
        for page in reader.pages:
            # Merge the watermark with the page
            page.merge_page(watermark_page)
            writer.add_page(page)

        # Save the watermarked PDF to a file
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)
            
    ## pdf manipulation choice
    def display_pdf_handling_choice(self):
        print("\nPossible pdf handling choices:")           
        for i, choice  in enumerate(self.choices):
            print(i+1, "_", choice)
        print()
        
    ## End of PDF_file_manager class      