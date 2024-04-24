import json
import requests
import os
import time
import numpy as np
from api import APIRequest
import logging


class YandexAPIRequest(APIRequest):
    def __init__(self, model_name: str = "yandexgpt") -> None:
        self.model_name = model_name
        self.prompt = {}
        self.folder_id = os.getenv("YC_FOLDER_ID")
        assert self.folder_id and "env variable 'YC_FOLDER_ID' undefined"
        self.api = os.getenv("YC_IAM_TOKEN")
        assert self.api and "env variable 'YC_IAM_TOKEN' undefined"

    def createURLModel(self):
        model = "gpt://" + self.folder_id + f"/{self.model_name}/latest"
        return model

    def createCompleteOptions(self):
        completeOptions = {}
        completeOptions["stream"] = False
        completeOptions["temperatute"] = 0
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
        json_file = {}

        json_file["modelUri"] = self.createURLModel()
        json_file["completionOptions"] = self.createCompleteOptions()
        json_file["messages"] = self.createMessages()

        json_data = json.dumps(json_file, ensure_ascii=False, indent=4)

        self.json = json_file
        self.prompt = json_data

    def send_request(self):
        response = requests.post(
            self.url, headers=self.headers, json=self.json)
        result = self.handle_error(response, 0)
        return result

    def handle_error(self, prev_response, attempt_number: int):
        if prev_response.status_code == requests.codes.ok:
            return prev_response

        if attempt_number >= self.max_attempt_count:
            raise RuntimeError(
                f"Can't get answer from LLM. Attempts exited. Error code: {prev_response.status_code}. Last response: {prev_response.text}")

        if prev_response.status_code == requests.codes.too_many_requests:
            logging.info(f"Yandex:{self.model_name} retry attempt {attempt_number}")
            time.sleep(attempt_number)
            response = requests.post(
                self.url, headers=self.headers, json=self.json)
            return self.handle_error(response, attempt_number + 1)
        raise RuntimeError(
            f"Can't get answer from LLM. Error code: {prev_response.status_code}. Last response: {prev_response.text}")

    def request(self, text, system_role, max_attempt_count=10):
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.headers['Authorization'] = 'Bearer ' + str(self.api)
        self.headers['x-folder-id'] = self.folder_id

        self.text = text
        self.system_role = system_role
        self.max_attempt_count = max_attempt_count
        self.createJSON()

        logging.info(f"Yandex:{self.model_name} request: {self.prompt}")
        res = self.send_request()

        logging.info(f"Yandex:{self.model_name} response: {res.text}")
        return res.json()['result']['alternatives'][0]['message']['text']

    def get_embedding(self, text: str):
        self.url = "https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding"
        # doc_uri = f"emb://{FOLDER_ID}/text-search-doc/latest"
        query_uri = f"emb://{self.folder_id}/text-search-query/latest"

        self.headers = {"Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api}", "x-folder-id": f"{self.folder_id}"}

        self.json = {
            "modelUri": query_uri,
            "text": text,
        }

        logging.info(f"Yandex:{self.model_name} request embed: {self.json}")
        return np.array(self.send_request().json()["embedding"])
