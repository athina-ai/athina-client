from abc import ABC

from athina_client.constants.athina import ATHINA_APP_BASE_URL


class AthinaAppBaseUrl(ABC):
    _athina_app_base_url = None

    @classmethod
    def set_url(cls, url):
        cls._athina_app_base_url = url

    @classmethod
    def get_url(cls):
        return cls._athina_app_base_url or ATHINA_APP_BASE_URL

    @classmethod
    def is_set(cls):
        return cls._athina_app_base_url is not None
