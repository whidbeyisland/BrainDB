import fitz
from pprint import pprint

def extract_pdf_text_blocks(filename):
    doc = fitz.open(filename)
    return extract_doc_text_blocks(doc)

def extract_doc_text_blocks(doc):
    text_blocks = list()
    for page_number in range(doc.page_count):
        page        = doc.load_page(page_number)
        text_blocks += extract_page_text_blocks(page) 
    return text_blocks

def extract_page_text_blocks(page):
    page_blocks     = page.get_text('blocks')
    page_text_blocks= map(lambda b: b[4], page_blocks)
    return list(page_text_blocks)


filename= 'example.pdf'
blocks  = extract_pdf_text_blocks(filename)
for b in blocks: print(b)
