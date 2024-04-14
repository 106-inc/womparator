import docx


document = docx.Document(infile)

# for paragraph in document.paragraphs:
for paragraph in document.iter_inner_content():
    if isinstance(paragraph, docx.text.paragraph.Paragraph):
        print("PARAGRAPH")
        print(paragraph.text)
    elif isinstance(paragraph, docx.table.Table):
        for row in paragraph.rows:
            for cell in row.cells:
                print(f"| {cell.text} ", end='')
            print("|")
    # print(paragraph)