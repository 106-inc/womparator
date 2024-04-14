import json
import requests
import os

class APIRequest():
    def __init__(self, text = "", system_role = "") -> None:
        self.text = text
        self.system_role = system_role
        self.prompt = {}
        self.folder_id = os.getenv("YC_FOLDER_ID", "")
        self.api = os.getenv("YC_IAM_TOKEN", "")
    def createURLModel(self):
        model = "gpt://" + self.folder_id + "/yandexgpt-lite"
        return model

    def createCompleteOptions(self):
        completeOptions = {}
        completeOptions["stream"] = False
        completeOptions["temperatute"] = 0.6
        completeOptions["maxTokens"] = 2000
        return completeOptions

    def createMessages(self):
        message1 = {}
        message2 = {}
        message1["role"] = "system"
        message1["text"] = self.system_role
        message2["role"] = "user"
        message2["text"] = self.text
        return [message1, message2]

    def createJSON(self):
        print(self.text)
        json_file = {}

        json_file["modelUri"] = self.createURLModel()
        json_file["completionOptions"] = self.createCompleteOptions()
        json_file["messages"] = self.createMessages()
        
        json_data = json.dumps(json_file, ensure_ascii=False, indent=4)

        self.json = json_file
        self.prompt = json_data
        #with open("request.json", "w") as outfile:
        #    outfile.write(json_data)

    def send_request(self):

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

        headers = {}
        headers["Content-Type"] = "application/json"
        headers['Authorization'] = 'Bearer ' + str(self.api)
        headers['x-folder-id'] = self.folder_id

        response = requests.post(url, headers=headers, json=self.json)
        result = response.text
        return result

    def run(self):
        self.createJSON()
        self.send_request()

a = APIRequest("Превед медвед", "Найди ошибки в тексте")
a.run()