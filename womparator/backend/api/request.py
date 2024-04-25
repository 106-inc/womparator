from api.api import APIRequest
import re
import logging

#This function create request and describe role. Original text contains technical description 
#role == 0: find technical details in document and to add new clause
#role == 1: briefly summarize this text
#role == 2: compare original_text with clauses
#role == 3: additional checker for strict tech details
def request(llm_api: APIRequest, text = "", clauses = [], role = -1):
    assert(role >= 0)
    assert(role < 4)
    
    results = []
    if role == 0:
        res = llm_api.request(text, "Ты профессиональный опытный инженер. Твоя задача найти в тексте ниже строгие технические требования компании-закупщика к оборудованию. Если в тексте нет технических требований, напиши `Требований нет`. Ответом должен быть список. Ответ не должен содержать юридическую информацию. Ответ должен быть максимально лаконичным и содержать только техническую информацию. Ответ должен быть на русском языке.")
        results.append(res)
    elif role == 1:
        a = llm_api.request(text, "Ты профессиональный опытный инженер. Сделай краткий пересказ данного технического документа и выдели всю важную информацию. Ответ должен быть максимально лаконичным. Ответ должен быть на русском языке.")
        results.append(a)
    elif role == 2:
        for clause in clauses:
            a = llm_api.request(text, "Ты профессиональный опытный инженер. Ты на вход будешь получать текст с техническим описанием. Определи удовлетворяет ли текст пункту технического требования. Ответами могут быть: нет информации (о пункте ничего не сказано в тексте), несоответствует (имеется противоречивая информация), частично соответствует (нехватает информации), соответствует (информация в пункте полностью соответствует информации текста). Ответ должен быть на русском языке. Пункт технического требования: " + str(clause))
            results.append(a)
    elif role == 3:
        res = llm_api.request(text, "Ты профессиональный опытный инженер. Соответствует ли данный текст строгим техническим требованиям. Ты должент ответить строго 'соответствует' или 'не соответствует'")
        results.append(res)
    return results


def extract_points(text):
    """
    Extracts a list of points from a text, handling a variety of point markers
    including numbers and asterisks.

    Args:
        text (str): The input text containing the points.

    Returns:
        list: A list of extracted points as strings.
    """
    if "требований нет" in text.lower():
        return []
    
    points = []
    for line in text.splitlines():
        # Match numbered points (1., 2., etc.)
        number_matches = re.findall(r"(\d+)\.\s+(.*?)(?=\s+\d+\.|\s*$)", line)
        for match in number_matches:
            points.append(f"{match[1]}")

        # Match asterisk-marked points (* Point text)
        asterisk_matches = re.findall(r"\*\s+(.*?)(?=\s+\*|\s*$)", line)
        for match in asterisk_matches:
            points.append(match)
    return points
