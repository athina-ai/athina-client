import requests
from retrying import retry
from typing import Any, Dict, List
from athina_client.errors import CustomException, NoAthinaApiKeyException
from athina_client.keys import AthinaApiKey
from athina_client.constants import API_BASE_URL


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
            endpoint = f"{API_BASE_URL}/api/v1/dataset_v2"
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
            endpoint = f"{API_BASE_URL}/api/v1/dataset_v2/{dataset_id}/add-rows"
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
            endpoint = f"{API_BASE_URL}/api/v1/dataset_v2/all"
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
            endpoint = f"{API_BASE_URL}/api/v1/dataset_v2/{dataset_id}"
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
            endpoint = f"{API_BASE_URL}/api/v1/dataset_v2/fetch-by-id/{dataset_id}"
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
            endpoint = f"{API_BASE_URL}/api/v1/dataset_v2/fetch-by-name"
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
