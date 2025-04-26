
# Necessary modules
from pdf_manager import PDF_manager

# Driver function
def main():
    
    # instantiate PDF manager
    myPDF_manager = PDF_manager()
    
    # Welcome users
    message_to_users = "Welcome to the PDF Manager Application"
    print("-" * 100)
    print("\t" * 3, message_to_users)
    print("-" * 100)
    
    # display pdf handling possible choices
    myPDF_manager.display_pdf_handling_choice()
    
    # loop for continuous user request
    while True:    
    
        # User's choice for pdf manipulation
        choice = int(input("Choose a number from 1 to 10 corresponding to the above PDF handling or -1 to exit: "))
    
        # Matching choice to PDF manager function
        match choice:
            # exiting the Application.
            case -1:
                print("Thank you for using the App. Come again!")
                exit()
            # text extraction and pages count
            case 1: 
                # pdf documents to use
                filename = input("Enter the pdf filename: ")
                print()
                print("*" * 80)      
                # retrieve total number of pages and pages text
                pages_count, pages_content = myPDF_manager.read_pdf_document(filename)
                print(f"Document total pages: {pages_count}")
                for page_number, text in pages_content:
                    print(f"Page {page_number}:")
                    print(text)
                    print("-" * 70)
                print("*" * 80)
                print()
            
            # Display metadata    
            case 2: 
                # pdf documents to use
                filename = input("Enter the pdf filename: ")                 
                # Display pdf metadata
                metadata = myPDF_manager.display_pdf_metadata(filename)    
                print("PDF Metadata:")
                for key, value in metadata.items():
                    print(f"{key}: {value}")
                print("*" * 80)
                print() 
            
            # splitting pdf
            case 3:
                # pdf documents to use
                filename = input("Enter the pdf filename: ")          
                # splitting pdf document
                split_files = myPDF_manager.splitting_pdf_document(filename)
                print("Split files:")
                for file in split_files:
                    print(file)
                print("*" * 80)
                print() 
            
            # Merge pdf
            case 4:
                # Merge many pdf documents
                pdf_list = input("Enter the pdf document to merge in proper order: ").split()
                merged_pdf = input("Enter file path where to save the file: ")            
                myPDF_manager.merge_pdf_documents(pdf_list, merged_pdf)
                print("*" * 80)
                print()

            # Rotate pdf
            case 5:            
                # Rotate pdf document
                myPDF_manager.rotate_pdf("twopage.pdf", "./treated_documents/rotated_twopage.pdf", 90)
                print("*" * 80)
                print()
            
            # Encrypt pdf
            case 6:   
                # encrytion of PDF documents
                # pdf documents to use
                filename = input("Enter the pdf filename: ")  
                myPDF_manager.encrypt_pdf_aes256(filename)
                print("*" * 80)
                print()
                
            # Decrypt pdf
            case 7:    
                # decrytion of PDF documents
                crypted_pdf_filename = input("Enter the output pdf filename: ")  
                myPDF_manager.decrypt_pdf_aes256(crypted_pdf_filename)
                print("*" * 80)
                print()
            
            # Etract images    
            case 8:   
                # Extracting images from PDF documents
                # Prompts user for pdf file to search
                filename_one = input("Enter the pdf file path or filename for image search:  ")
                myPDF_manager.extract_images_from_pdf(filename_one)
                print("*" * 80)
                print()
            
            # Crop pdf    
            case 9:     
                # Cropping a pdf document
                filename_three = input("Enter the PDF document path: ")
                myPDF_manager.cropping_pdf_document(filename_three)
                print("*" * 80)
                print()

            # Watermark pdf
            case 10:
                # Add the watermark to the target PDF
                input_pdf = input("what is the file path of the pdf you want to watermark: ")  # Replace with your input PDF file
                output_pdf = input("what is the file path of the output pdf you watermarked: ")  # Replace with your desired output file
                myPDF_manager.add_watermark(input_pdf, output_pdf)
                print(f"Watermarked PDF saved as {output_pdf}") 
            
            # Default choice   
            case _:
                print("this choice is unavailable, retry from 1 to 10.") 
                ## End function main() 
            
# Running the driver function
if __name__ == "__main__":
    main()   