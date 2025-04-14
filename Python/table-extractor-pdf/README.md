# Table Extractor PDF
In this project, we will extract table from the PDF file. Originally, I wanted to run the code from the freeCodeCamp tutorial; however, the code could not extract the tables from the PDF file I wanted to use. Below are some of the adjustments I made:
* In freeCodeCamp, the tutorial used Economic and Human Development Indicators for India from UN DP, which has simpler and cleaner table. I used Human Development Report 2023/2024 from UNDP, which had more complicated tables. Below are the issues I ran into when I tried to apply the freeCodeCamp program:
    - Camelot did not work. I used stream and lattice modes, but neither worked wiht Camelot. Since the table in the PDF file has multiple columns and is spread across multiple lines, there is not enough spacing so Camelot would find the tables, but will end up displaying a messy, unwanted chunk of texts
    - The tutorial used seaborn. I did not use it since I could not even use Camelot in the first place
    - Instead, I opted for using pdfplumber and pandas
* You can either run the code by downloading the PDF file or extracting the link. I opted for the latter since I did not want to download the 50+ page file into my computer
* Like the tutorial, I used Jupyter but via VS Code
* An issue I could not solve was extracting the column headers. The headers in the PDF files do not show up as part of the table when I run the code; therefore, I had to create separate list containing the column names.

## Set up Jupyter environment on VS Code, install pdfplumber and requests
* This is optional. You can work on Jupyter directly but if you prefer VS Code follow the next steps:
    - Install Jupyter extension on your VS Code 
    - From VS Code, Create: New Jupyter Notebook. This should create a new .ipynb file
    - On the top right hand corner where it says "Select Kernel", select Python
* Install pdfplumber and requests in your Jupyter environment
    - pip install pdfplumber
    - pip install requests

## Fetch the PDF file from the web (to avoid downloading directly)
* Send GET request to the URL and store the content into a file-like object by using BytesIO()

## List out the column names and pages from the tables in the PDF 
* The PDF file we'll be using have the headers organized in a weird format that makes it hard for our code to detect them (the headers do not show up as part of the table)
* A workaround is to list them manually
* List out the pages that you'll be extracting the table from. In this case, we want to extract the tables from page 41 to 44

## Extract the table
* Open the PDF file with pdfplumber and start looping through the page
    - Use the extract_tables() function to look for tables
* Convert the table into Pandas DataFrame
    - Skip the first row of the table since extract_tables() often includes extra header rows that aren't part of the data
    - Only keep as many columns as defined and assign headers. 
        - Use Pandas int location method to select data..
        - Use df.shape[1] to get the number of columns. Take a slice of the column names list that matches the number of columns in the DataFrame
        - We do this to prevent error in cases where the customColumns has more headers than the DataFrame. This helps us to dynamically apply headers to DataFrame
    - Replace placeholder values
    - Append the extracted data

## Combine all tables into one
* Combine all the tables from the selected pages into one
* You can either show the first few rows or display all the rows