import api as api
import re

#This function create request and describe role. Original text contains technical description 
#role == 0: find technical details in document and to add new clause
#role == 1: briefly summarize this text
#role == 2: compare original_text with clauses
def request(text = "", clauses = [], role = -1):
    assert(role >= 0)
    assert(role < 3)
    
    results = []
    if role == 0:
        a = api.APIRequest(text, "Ты професиональный опытный инженер. Твоя задача найти в тексте ниже строгие\
                            технические требования компании-закупщика к оборудованию. \
                            Если в тексте нет технических требований, напиши `Требований нет`. \
                            Ответом должен быть список. \
                            Ответ не должен содержать юридическую информацию. \
                            Ответ должен быть максимально лаконичным и содержать только техническую информацию.")
        results.append(a.run())
    elif role == 1:
        a = api.APIRequest(text, "Ты профессиональный опытный инженер. Сделай краткий перессказ данного\
                            технического документа и выдели всю важную информацию. Ответ должен быть максимально лаконичным.")
        results.append(a.run())
    else:
        for clause in clauses:
            a = api.APIRequest(text, "Ты профессиональный опытный инженер. Ты на вход будешь получать текст с техническим описанием. \
                Определи удовлетворяет ли текст пункту технического требования. Ответами могут быть: нет информации (о пункте ничего не сказано в тексте), несоответствует (имеется противоречивая информация), частично соответствует (нехватает информации), соответствует (информация в пункте полностью соответствует информации текста).\
                    Пункт технического требования: " + str(clause))
            results.append(a.run())
    
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
