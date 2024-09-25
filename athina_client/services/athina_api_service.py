import os
from dotenv import load_dotenv
from pydantic import BaseModel
import pandas as pd
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

    @staticmethod
    def log_eval_results_with_config(eval_results_with_config: dict):
        try:
            endpoint = (
                f"{AthinaApiService._base_url()}/api/v1/eval_run/log-eval-results-sdk"
            )
            response = requests.post(
                endpoint,
                headers=AthinaApiService._headers(),
                json=eval_results_with_config,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = "please check your athina api key and try again"
                raise CustomException(details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get("error", "Unknown Error")
                details_message = response_json.get("details", {}).get(
                    "message", "No Details"
                )
                print(f"ERROR: Failed to log eval results: {error_message}")
                raise CustomException(details_message)
            return response.json()
        except Exception as e:
            raise

    @staticmethod
    def log_eval_results_to_dataset(eval_results_with_config: dict, dataset_id: str):
        try:

            def remove_none_values(data: dict) -> dict:
                return {k: v for k, v in data.items() if v is not None}

            def serialize_metric(metric):
                if isinstance(metric, (int, float, str, bool)):
                    return metric
                elif hasattr(metric, "to_dict"):
                    return metric.to_dict()
                elif hasattr(metric, "__dict__"):
                    return metric.__dict__
                else:
                    return str(metric)

            eval_results = eval_results_with_config.get("eval_results", [])
            # Limit to the first 1000 items
            sliced_eval_results = eval_results[:1000]
            cleaned_eval_results = []

            for eval_result in sliced_eval_results:
                cleaned_metrics = [
                    serialize_metric(metric)
                    for metric in eval_result.get("metrics", [])
                ]
                cleaned_eval_result = {
                    "metrics": cleaned_metrics,
                    "reason": eval_result.get("reason"),
                }
                cleaned_eval_results.append(remove_none_values(cleaned_eval_result))

            development_eval_config = remove_none_values(
                eval_results_with_config.get("development_eval_config", {})
            )

            cleaned_results = {
                "dataset_id": dataset_id,
                "development_eval_config": development_eval_config,
                "eval_results": cleaned_eval_results,
            }

            AthinaApiService.log_eval_results_with_config(cleaned_results)
        except Exception as e:
            print(f"Failed to log eval results: {e}")
            raise e

    @staticmethod
    def log_eval_results(dataset_id: str, config_id: str, results: pd.DataFrame):
        load_dotenv()

        api_base = "https://api.athina.ai"
        api_key = os.getenv("ATHINA_API_KEY")

        if not api_key:
            raise ValueError("ATHINA_API_KEY not found in .env file")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        url = f"{api_base}/log_eval_results"

        payload = {
            "dataset_id": dataset_id,
            "config_id": config_id,
            "results": results.to_dict(orient="records"),
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"API call failed: {str(e)}")

    @staticmethod
    def _convert_eval_to_config(eval_obj: Any) -> Dict[str, Any]:
        if isinstance(eval_obj, BaseModel):
            return eval_obj.dict()
        elif hasattr(eval_obj, "__dict__"):
            return eval_obj.__dict__
        else:
            return {"name": eval_obj.__name__, "type": "function"}
