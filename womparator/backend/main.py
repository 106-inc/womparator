from flask import Flask, Response
from flask_cors import CORS
from flask import request
from werkzeug.datastructures import FileStorage
import docx
import pandas as pd

womparator = Flask(__name__)
CORS(womparator)


def parse(file : FileStorage) -> str:
    doc = docx.Document(file)
    req_text = ""
    for content in doc.iter_inner_content():
        if isinstance(content, docx.text.paragraph.Paragraph):
            par_text = content.text
            if len(par_text) > 0 and not par_text.isspace():
                req_text += par_text
        elif isinstance(content, docx.table.Table):
            for row in content.rows:
                for cell in row.cells:
                    req_text += f"| {cell.text} "
                req_text += "|\n"
    return req_text

@womparator.route("/get_csv", methods=["GET"])
def export_csv():
    # Sample Data
    data = pd.read_csv("result.csv")
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)

    return Response(
        csv_data,
        mimetype='text/csv',
        headers={"Content-disposition":
                 "attachment; filename=mydata.csv"})

@womparator.route("/upload", methods=["POST"])
def upload():
    req = parse(request.files['Requirements'])
    desc = parse(request.files['Description'])
    print(f"Requirements\n{req}")
    print(f"Description\n{desc}")
    return "OK"


if __name__ == "__main__":
    womparator.run(port=8080, host="0.0.0.0")
