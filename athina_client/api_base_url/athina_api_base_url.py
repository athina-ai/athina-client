from abc import ABC


class AthinaApiBaseUrl(ABC):
    _athina_api_base_url = None

    @classmethod
    def set_url(cls, url):
        cls._athina_api_base_url = url

    @classmethod
    def get_url(cls):
        return cls._athina_api_base_url

    @classmethod
    def is_set(cls):
        return cls._athina_api_base_url is not None
