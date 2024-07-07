import requests
from retrying import retry
from typing import Any, Dict, List
from athina_client.errors import CustomException, NoAthinaApiKeyException
from athina_client.keys import AthinaApiKey
from athina_client.constants import ATHINA_API_BASE_URL
from athina_client.api_base_url import AthinaApiBaseUrl


class AthinaApiService:
    @staticmethod
    def _headers():
        athina_api_key = AthinaApiKey.get_key()
        if not athina_api_key:
            raise NoAthinaApiKeyException(
                "Athina API Key is not set. Please set the key using AthinaApiKey.set_key(<ATHINA_API_KEY>)"
            )
        return {
            "athina-api-key": athina_api_key,
        }

    @staticmethod
    def _base_url():
        base_url = AthinaApiBaseUrl.get_url()
        return base_url if base_url else ATHINA_API_BASE_URL

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def create_dataset(dataset: Dict):
        """
        Creates a dataset by calling the Athina API

        Parameters:
        - dataset (Dict): A dictionary containing the dataset details.

        Returns:
        - The newly created dataset object.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/dataset_v2"
            response = requests.post(
                endpoint,
                headers=AthinaApiService._headers(),
                json=dataset,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["data"]["dataset"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def add_dataset_rows(dataset_id: str, rows: List[Dict[str, Any]]):
        """
        Adds rows to a dataset by calling the Athina API.

        Parameters:
        - dataset_id (str): The ID of the dataset to which rows are added.
        - rows (List[Dict]): A list of rows to add to the dataset, where each row is represented as a dictionary.

        Returns:
        The API response data for the dataset after adding the rows.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/dataset_v2/{dataset_id}/add-rows"
            response = requests.post(
                endpoint,
                headers=AthinaApiService._headers(),
                json={"dataset_rows": rows},
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["data"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def list_datasets():
        """
        Lists all datasets by calling the Athina API.

        Returns:
        - A list of dataset objects.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/dataset_v2/all"
            response = requests.get(endpoint, headers=AthinaApiService._headers())
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["datasets"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def delete_dataset_by_id(dataset_id: str):
        """
        Deletes a dataset by calling the Athina API.

        Parameters:
        - dataset_id (str): The ID of the dataset to delete.

        Returns:
        - Message indicating the success of the deletion.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/dataset_v2/{dataset_id}"
            response = requests.delete(endpoint, headers=AthinaApiService._headers())
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["data"]["message"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def get_dataset_by_id(dataset_id: str):
        """
        Get a dataset by calling the Athina API.

        Parameters:
        - dataset_id (str): The ID of the dataset to get.

        Returns:
        - The dataset object along with metrics and eval configs.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/dataset_v2/fetch-by-id/{dataset_id}"
            params = {"offset": 0, "limit": 1000, "include_dataset_rows": "true"}
            response = requests.post(
                endpoint, headers=AthinaApiService._headers(), params=params
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["data"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def get_dataset_by_name(name: str):
        """
        Get a dataset by calling the Athina API.

        Parameters:
        - name (str): The name of the dataset to get.

        Returns:
        - The dataset object along with metrics and eval configs

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/dataset_v2/fetch-by-name"
            params = {"offset": 0, "limit": 1000, "include_dataset_rows": "true"}
            response = requests.post(
                endpoint,
                headers=AthinaApiService._headers(),
                params=params,
                json={"name": name},
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["data"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def get_default_prompt(slug: str):
        """
        Get a default prompt by calling the Athina API.

        Parameters:
        - slug (str): The slug of the prompt to get.

        Returns:
        - The prompt object.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/prompt/{slug}/default"
            response = requests.get(endpoint, headers=AthinaApiService._headers())
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["data"]["prompt"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def get_all_prompt_slugs():
        """
        Get all prompt slugs by calling the Athina API.

        Returns:
        - A list of prompt slugs.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/prompt/slug/all"
            response = requests.get(endpoint, headers=AthinaApiService._headers())
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["data"]["slugs"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def delete_prompt_slug(slug: str):
        """
        Delete a prompt slug and its templates by calling the Athina API.

        Parameters:
        - slug (str): The slug to delete.

        Returns:
        - A message indicating the success of the deletion.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/prompt/slug/{slug}"
            response = requests.delete(endpoint, headers=AthinaApiService._headers())
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["message"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def duplicate_prompt_slug(slug: str, name: str):
        """
        Duplicate a prompt slug by calling the Athina API.

        Parameters:
        - slug (str): The slug to duplicate.
        - name (str): The new name for the duplicated slug.

        Returns:
        - The duplicated prompt slug object and the default/latest version/latest prompt of the slug

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = (
                f"{AthinaApiService._base_url()}/api/v1/prompt/slug/{slug}/duplicate"
            )
            response = requests.post(
                endpoint,
                headers=AthinaApiService._headers(),
                json={"name": name},
            )
            response_json = response.json()

            if response.status_code == 401:
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)

            return response_json["data"]["slug"]
        except requests.RequestException as e:
            raise CustomException("Request failed", str(e))
        except Exception as e:
            raise CustomException("Unexpected error occurred", str(e))

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def create_prompt(slug: str, prompt_data: Dict[str, Any]):
        """
        Creates a prompt by calling the Athina API.

        Parameters:
        - slug (str): The slug of the prompt.
        - prompt_data (Dict): The prompt data to be created.

        Returns:
        - The newly created prompt object.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/prompt/{slug}"
            response = requests.post(
                endpoint,
                headers=AthinaApiService._headers(),
                json=prompt_data,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["data"]["prompt"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def run_prompt(slug: str, request_data: Dict[str, Any]):
        """
        Runs a prompt by calling the Athina API.

        Parameters:
        - slug (str): The slug of the prompt.
        - request_data (Dict): The request data to run the prompt

        Returns:
        - The prompt execution object

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/prompt/{slug}/run"
            response = requests.post(
                endpoint,
                headers=AthinaApiService._headers(),
                json=request_data,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["data"]
        except Exception as e:
            raise

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def mark_prompt_as_default(slug: str, version: int):
        """
        Set a prompt version as the default by calling the Athina API.

        Parameters:
        - slug (str): The slug of the prompt.
        - version (int): The version to set as default.

        Returns:
        - The prompt object.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/prompt/{slug}/{version}/set-default"
            response = requests.patch(endpoint, headers=AthinaApiService._headers())
            response_json = response.json()

            if response.status_code == 401:
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)

            return response_json["data"]["prompt"]
        except requests.RequestException as e:
            raise CustomException("Request failed", str(e))
        except Exception as e:
            raise CustomException("Unexpected error occurred", str(e))

    @staticmethod
    @retry(stop_max_attempt_number=2, wait_fixed=1000)
    def update_prompt_template_slug(slug: str, update_data: Dict[str, Any]):
        """
        Updates a prompt template slug by calling the Athina API.

        Parameters:
        - slug (str): The slug of the prompt to update.
        - update_data (Dict): The data to update the prompt template slug.

        Returns:
        - The updated prompt template slug object.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{AthinaApiService._base_url()}/api/v1/prompt/slug/{slug}"
            response = requests.patch(
                endpoint,
                headers=AthinaApiService._headers(),
                json=update_data,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                raise CustomException(error_message, details_message)
            return response.json()["data"]["slug"]
        except Exception as e:
            raise CustomException("Error updating prompt template slug", str(e))
