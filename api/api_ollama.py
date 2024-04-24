from api import APIRequest
import ollama
import logging


class LlamaAPIRequest(APIRequest):
    """
    Instruction (tested on Windows):
        1. Go to https://ollama.com/ and download ollama for your os. Then install it.
        2. In terminal ('llama3' can be replaced with 'llama2'):
            $ ollama pull llama3
            $ ollama serve
           NOTE: if you have: Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.
                 define env variable 'OLLAMA_HOST' then relaunch:
                 Linux: 'export OLLAMA_HOST="127.0.0.1:11435"'
                 Windows: '$Env:OLLAMA_HOST="127.0.0.1:11435"'
           NOTE: 'ollama serve' launch server (do it in second terminal). 
        3. pip install ollama
    """
    def __init__(self, model_name: str = "llama3") -> None:
        self.model_name = model_name

    def request(self, text, system_role):
        message = [
            {'role': 'system', 'content': system_role},
            {'role': 'user', 'content': text}
        ]
        response = ollama.chat(model=self.model_name, messages=message)

        logging.debug(f"Ollama response: {response}")
        assert response['done']
        return response['message']['content']
