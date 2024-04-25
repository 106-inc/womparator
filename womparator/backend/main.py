from flask import Flask, Response
from flask_cors import CORS
from flask import request
from werkzeug.datastructures import FileStorage
import pandas as pd
import logging

import api.docx_parser as docx_parser
import api.request as req
# import api.api_ollama as api_ollama
import api.api_yandex as api_yandex
import api.driver

womparator = Flask(__name__)
CORS(womparator)

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
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Step 1: Parsing
    req_parts = docx_parser.parse_docx_parts(request.files['Requirements'])
    desc_parts = docx_parser.parse_docx_parts(request.files['Description'])
    print(f"Requirements parts count: {len(req_parts)}")
    print(f"Description  parts count: {len(desc_parts)}")

    # Step 2: Technical requirement points finding
    logging.debug(f"Step 2")
    llm_embed = api_yandex.YandexAPIRequest(model_name="yandexgpt")
    llm_api = api_yandex.YandexAPIRequest(model_name="yandexgpt")
    # llm_api = api_ollama.LlamaAPIRequest(model_name="llama3")
    
    points = api.driver.extract_points(llm_embed, llm_api, req_parts)
    
    # Step 3: Match requirements with description
    logging.debug(f"Step 3")
    points = api.driver.match_desc_points(llm_embed, llm_api, points, desc_parts)
    
    # Step 4: Save csv
    logging.debug(f"Step 4")
    csv_str = api.driver.points_to_csv(points, desc_parts)
    with open("result.csv", 'w', newline='', encoding='utf-8') as f:
        f.write(csv_str)
    
    return "OK"


if __name__ == "__main__":
    womparator.run(port=8080, host="0.0.0.0")
