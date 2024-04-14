import api as api

#This function create request and describe role. Original text contains technical description 
#role == 0: find technical details in document and to add new clause
#role == 1: briefly summarize this text
#role == 2: compare original_text with clauses
def request(text = "", clauses = [], role = -1):
    assert(role >= 0)
    assert(role < 3)
    
    results = []
    if role == 0:
        a = api.APIRequest(text, "Ты професиональный опытный инженер. Твоя задача найти в этом тексте строгие\
                            технические требования компании-закупщика к оборудованию, если они тут есть")
        results.append(a.run())
    elif role == 1:
        a = api.APIRequest(text, "Ты профессиональный опытный инженер. Сделай краткий перессказ данного\
                            технического документа и выдели всю важную информацию.")
        results.append(a.run())
    else:
        for clause in clauses:
            a = api.APIRequest(text, "Ты профессиональный опытный инженер. Тебе нужно найти в этом техническом тексте\
                                соответствие между документом и пунктом ниже и если оно есть, то дать свой коментарий. Пункт: \
                               " + str(clause))
            results.append(a.run())
    
    return results
