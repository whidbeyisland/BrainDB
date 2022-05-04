import PyPDF2
import data_func
import csv

reader = PyPDF2.PdfFileReader(
    './ConservancyTurkeyManual-5.pdf')

writer = PyPDF2.PdfFileWriter()

for page in range(2,4):

    writer.addPage(reader.getPage(page))
    
output_filename = './ConservancyTurkeyManual-5 - Copy.pdf'

with open(output_filename, 'wb') as output:
    writer.write(output)
    
text = data_func.convert_pdf_to_string(
    './ConservancyTurkeyManual-5 - Copy.pdf')

print(text)