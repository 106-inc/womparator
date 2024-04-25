from api.api import APIRequest
import re
import logging

#This function create request and describe role. Original text contains technical description 
#role == 0: find technical details in document and to add new clause
#role == 1: briefly summarize this text
#role == 2: compare original_text with clauses
def request(llm_api: APIRequest, text = "", clauses = [], role = -1):
    assert(role >= 0)
    assert(role < 3)
    
    results = []
    if role == 0:
        res = llm_api.request(text, "Ты профессиональный опытный инженер. Твоя задача найти в тексте ниже строгие технические требования к оборудованию. Ответом должен быть список. Техническим требованием считается только строго определенная характеристика оборудования, информация о котором полностью дана в тексте. Если в тексте нет технических требований, напиши `Требований нет`.")
        results.append(res)
    elif role == 1:
        a = llm_api.request(text, "Твоя задача определить является ли текст техническим требованием к оборудованию. Ответь да или нет. Определение: техническим требованием считается только строго определенная характеристика оборудования, полностью данная в тексте.")
        results.append(a)
    else:
        for clause in clauses:
            a = llm_api.request(text, "Ты профессиональный опытный инженер. Ты на вход будешь получать текст с техническим описанием. Твоя задача определить удовлетворяет ли текст пункту строго технического требования. Ответами могут быть: нет информации (о пункте ничего не сказано в тексте или текст неполон), не соответствует (имеется противоречивая информация), частично соответствует, соответствует (информация в пункте полностью соответствует информации текста). Пункт технического требования: " + str(clause))
            results.append(a)
    
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
