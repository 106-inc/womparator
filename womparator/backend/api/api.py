import abc
import json
import requests
import os
import time

class APIRequest():
    @abc.abstractmethod
    def request(self, text, system_role, max_attempt_count):
        raise NotImplementedError
