from enum import Enum
from dataclasses import dataclass
import numpy as np
import logging
from api.api import APIRequest
from api.vector_database import VectorDatabase
import csv
import io
import api.request as req
from api.docx_parser import TextPartInfo

class RequirementStatus(Enum):
    NO_INFORMATION = 0
    NOT_SATISFIED = 1
    PARTLY_SATISFIED = 2
    SATISFIED = 3

@dataclass
class RequirementPointInfo:
    text: str
    req_part_id: int
    embedding: np.array
    desc_part_id: int = -1
    status: RequirementStatus = RequirementStatus.NO_INFORMATION
    comment: str = ''
    # TODO:
    # req_chapter_id: int
    # desc_chapter_id: int

def extract_points(llm_embed: APIRequest, llm_api: APIRequest, req_text_parts: list[TextPartInfo]) -> list[RequirementPointInfo]:
    async_res_s = []
    for req_part_id, text_req in enumerate(req_text_parts):
        text = text_req.heading + text_req.body
        async_res_s.append(req.request(llm_api, text=text, role=0)[0])

    points = []
    for req_part_id, async_res in enumerate(async_res_s):
        cur_points = req.extract_points(async_res.get())

        for p in cur_points:
            # create embedding
            emb = llm_embed.get_embedding(p)
            # save point text with embedding
            points.append(RequirementPointInfo(p, req_part_id, emb))

        logging.info(f"Detected points: {cur_points}")
    return points

def classify_response(message) -> RequirementStatus:
    lower_message = message.lower()
    if "нет информации" in lower_message:
        reply = RequirementStatus.NO_INFORMATION
    elif lower_message.find("не соотвеству") != -1 or "противоречивая информация" in lower_message:
        reply = RequirementStatus.NOT_SATISFIED
    elif lower_message.find("частично соответству") != -1:
        reply = RequirementStatus.PARTLY_SATISFIED
    elif lower_message.find("соответству") != -1:
        reply = RequirementStatus.SATISFIED
    else:
        logging.warn(f"Message without clear answer: {message}")
        reply = RequirementStatus.NO_INFORMATION
    return reply

def match_desc_points(llm_embed: APIRequest, llm_api: APIRequest, points: list[RequirementPointInfo], desc_text_parts: list[TextPartInfo]):
    # get embeddings for description parts
    desc_embeddings_db = VectorDatabase()
    for desc in desc_text_parts:
        emb = llm_embed.get_embedding(desc.heading + desc.body)
        desc_embeddings_db.add_embedding(emb, desc)
    
    # now database is full and we prepare for search    
    desc_embeddings_db.build_index()
    
    async_responses = []
    for point_id in range(len(points)):
        cur_point = points[point_id]

        # search k most common parts in description
        # TODO: adjust K
        K = 1
        kn_s = desc_embeddings_db.search(cur_point.embedding)

        cur_async_responses = []
        for neighbor in kn_s:
            desc = neighbor[0]
            desc_text = desc.heading + desc.body
            res = req.request(llm_api, text=desc_text, clauses=[cur_point.text], role=2)[0]
            cur_async_responses.append((res, desc))
        async_responses.append(cur_async_responses)
        
    for point_id, async_res_s in zip(range(len(points)), async_responses):
        cur_point = points[point_id]

        for neighbor_res in async_res_s:
            desc = neighbor_res[1]
            response = neighbor_res[0].get()
            cur_status = classify_response(response)
            if cur_status.value > cur_point.status.value:
                cur_point.status = cur_status
                cur_point.desc_part_id = desc.id
                cur_point.comment = response
            if cur_status == RequirementStatus.SATISFIED:
                break
        points[point_id] = cur_point        

    return points

def points_to_csv(points: list[RequirementPointInfo], desc_text_parts: list[TextPartInfo]) -> str:
    headers = ['Пункт СТО ИНТИ', 'Требование', 'Пункт ТУ/СТО', 'Формулировка ТУ/СТО', 'Статус (С/Ч/Н)', 'Комментарий']
    
    output = io.StringIO()
    writer = csv.writer(output)
    # Write headers
    writer.writerow(headers)
    # Write data rows
    for p in points:
        status = ('С' if p.status == RequirementStatus.SATISFIED 
                  else 'Ч' if p.status == RequirementStatus.PARTLY_SATISFIED else 'Н')
        desc_text = desc_text_parts[p.desc_part_id].heading + desc_text_parts[p.desc_part_id].body if p.desc_part_id != -1 else ''
        writer.writerow([p.req_part_id, p.text, p.desc_part_id, desc_text, status, p.comment])
    return output.getvalue()
    