from dataclasses import dataclass
import docx

@dataclass
class HeadingInfo:
    text: str
    inheritance_number: int

class HeadingsTracker:
    def __init__(self):
        self.headings_stack = []
        pass

    def next_elem(self, elem) -> bool:
        HEADING_STYLE_NAME = "Heading"
        if isinstance(elem, docx.text.paragraph.Paragraph):
            style_name = elem.style.name
            if style_name.startswith(HEADING_STYLE_NAME):
                inheritance_number = int(style_name[len(HEADING_STYLE_NAME):])

                # remove lover headings from stack
                while(len(self.headings_stack) > 0 and self.headings_stack[-1].inheritance_number >= inheritance_number):
                    del self.headings_stack[-1]

                if len(elem.text) > 0: 
                    self.headings_stack.append(HeadingInfo(elem.text, inheritance_number))
                return True
        return False

    def get_text(self):
        s = ""
        for info in self.headings_stack:
            s += '#'*info.inheritance_number + ' ' + info.text + '\n'
        return s

@dataclass
class TextPartInfo:
    heading: str
    body: str
    id: int
    # TODO:
    # chapter_number: int
    
def parse_docx_parts(file) -> list[TextPartInfo]:  
    document = docx.Document(file)
    htracker = HeadingsTracker()

    # for paragraph in document.paragraphs:
    text_parts = []
    cur_heading = ''
    cur_body = ''
    prev_is_normal = False
    for paragraph in document.iter_inner_content():
        cur_is_normal = False
        if isinstance(paragraph, docx.text.paragraph.Paragraph):
            if not htracker.next_elem(paragraph):
                if not prev_is_normal or len(paragraph.text) > 200:
                    if len(cur_body) > 0:
                        part = TextPartInfo(cur_heading, cur_body, len(text_parts))
                        text_parts.append(part)
                    cur_heading = htracker.get_text()
                    cur_body = ''
                if len(paragraph.text) > 0 and not paragraph.text.isspace():
                    cur_body += paragraph.text + '\n'
                    cur_is_normal = True
        elif isinstance(paragraph, docx.table.Table):
            for row in paragraph.rows:
                for cell in row.cells:
                    cur_body += f"| {cell.text} "
                cur_body += "|\n"
        prev_is_normal = cur_is_normal
    
    return text_parts