import json

class APIRequest():
    def __init__(self, text = "") -> None:
        self.text = text
        self.folder_id = #your folder id
        self.api = #your api

    def createURLModel(self):
        model = "gpt://" + self.folder_id + "/yandexgpt-lite"
        return model

    def createCompleteOptions(self):
        completeOptions = {}
        completeOptions["stream"] = False
        completeOptions["temperatute"] = 0.6
        completeOptions["maxTokens"] = 2000

    def createMessages(self):
        message1 = {}
        message2 = {}
        message1["role"] = "system"
        message1["text"] = "Ты профессионал"
        message2["role"] = "user"
        message2["text"] = self.text
        return message1, message2

    def createJSON(self):
        print(self.text)
        json_file = {}

        json_file["modelUri"] = self.createURLModel()
        json_file["completionOptions"] = self.createCompleteOptions()
        json_file["messages"] = [self.createMessages()]
        
        json_data = json.dumps(json_file, ensure_ascii=False, indent=4)

        with open("request.json", "w") as outfile:
            outfile.write(json_data)

a = APIRequest("try")
a.createJSON()