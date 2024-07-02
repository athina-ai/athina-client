from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from athina_client.services import AthinaApiService
from athina_client.errors import CustomException


@dataclass
class ModelOptions:
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None


@dataclass
class OrgModelConfig:
    id: str
    org_id: str
    workspace_slug: str
    provider_id: str
    model_id: str
    config: Dict[str, Any]
    created_at: str
    updated_at: str
    input_tokens_cost: Optional[Any] = None
    output_tokens_cost: Optional[Any] = None


@dataclass
class PromptRunMetadata:
    environment: Optional[str] = None
    customer_id: Optional[str] = None
    customer_user_id: Optional[str] = None
    session_id: Optional[str] = None
    external_reference_id: Optional[str] = None
    topic: Optional[str] = None
    custom_attributes: Optional[Dict[str, Any]] = None


@dataclass
class PromptExecution:
    id: str
    user_id: str
    org_id: str
    workspace_slug: str
    prompt_template_id: str
    variables: Dict[str, Any]
    language_model_id: Optional[str]
    org_model_config_id: Optional[str]
    prompt_sent: List[Dict[str, str]]
    prompt_response: str
    tools: Optional[Any]
    tool_choice: Optional[str]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: Optional[Any]
    response_time: int
    options: Optional[ModelOptions]
    grader_feedback: Optional[int]
    created_at: str
    updated_at: str


@dataclass
class Prompt:
    id: str
    user_id: str
    org_id: str
    workspace_slug: str
    prompt_template_slug_id: str
    commit_message: str
    prompt: List[Dict[str, str]]
    version: int
    tools: Optional[Any] = None
    tool_choice: Optional[Any] = None
    is_default: bool = False
    model: Optional[str] = None
    org_model_config_id: Optional[str] = None
    parameters: Optional[ModelOptions] = None
    hash: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    org_model_config: Optional[OrgModelConfig] = None

    @staticmethod
    def create(
        slug: str,
        prompt: List[Dict[str, str]],
        model: Optional[str] = None,
        provider: Optional[str] = None,
        parameters: Optional[ModelOptions] = None,
        commit_message: Optional[str] = None,
    ) -> "Prompt":
        """
        Creates a new prompt.

        Parameters:
        - slug (str): The slug of the prompt.
        - prompt (List[Dict[str, str]]): The prompt template data.
        - model (Optional[str]): Optional model for the prompt.
        - provider (Optional[str]): Optional provider.
        - parameters (Optional[Dict[str, Any]]): Optional parameters.
        - commit_message (Optional[str]): Optional commit message.

        Returns:
        - The newly created prompt object.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        prompt_data = {
            "prompt": prompt,
            "model": model,
            "provider": provider,
            "parameters": parameters,
            "commit_message": commit_message,
        }

        # Remove keys where the value is None
        prompt_data = {k: v for k, v in prompt_data.items() if v is not None}

        try:
            created_prompt_data: Dict[str, Any] = AthinaApiService.create_prompt(
                slug, prompt_data
            )
        except Exception as e:
            raise CustomException("Error creating prompt", str(e))

        return Prompt(
            id=created_prompt_data["id"],
            user_id=created_prompt_data["user_id"],
            org_id=created_prompt_data["org_id"],
            workspace_slug=created_prompt_data["workspace_slug"],
            prompt_template_slug_id=created_prompt_data["prompt_template_slug_id"],
            commit_message=created_prompt_data["commit_message"],
            prompt=created_prompt_data["prompt"],
            tools=created_prompt_data.get("tools"),
            tool_choice=created_prompt_data.get("tool_choice"),
            version=created_prompt_data["version"],
            is_default=created_prompt_data["is_default"],
            model=created_prompt_data.get("model"),
            org_model_config_id=created_prompt_data.get("org_model_config_id"),
            parameters=created_prompt_data.get("parameters"),
            hash=created_prompt_data.get("hash"),
            created_at=created_prompt_data.get("created_at"),
            updated_at=created_prompt_data.get("updated_at"),
        )

    @staticmethod
    def get_default(slug: str) -> "Prompt":
        """
        Get default prompt by calling the Athina API.

        Parameters:
        - slug (str): The slug of the prompt to get.

        Returns:
        - The prompt object.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            prompt_data: Dict[str, Any] = AthinaApiService.get_default_prompt(slug)
        except Exception as e:
            raise CustomException("Error fetching default prompt", str(e))

        org_model_config_data = prompt_data.get("org_model_config")
        org_model_config = None
        if org_model_config_data:
            org_model_config = OrgModelConfig(
                id=org_model_config_data["id"],
                org_id=org_model_config_data["org_id"],
                workspace_slug=org_model_config_data["workspace_slug"],
                provider_id=org_model_config_data["provider_id"],
                model_id=org_model_config_data["model_id"],
                config=org_model_config_data["config"],
                input_tokens_cost=org_model_config_data["input_tokens_cost"],
                output_tokens_cost=org_model_config_data["output_tokens_cost"],
                created_at=org_model_config_data["created_at"],
                updated_at=org_model_config_data["updated_at"],
            )

        return Prompt(
            id=prompt_data["id"],
            user_id=prompt_data["user_id"],
            org_id=prompt_data["org_id"],
            workspace_slug=prompt_data["workspace_slug"],
            prompt_template_slug_id=prompt_data["prompt_template_slug_id"],
            commit_message=prompt_data["commit_message"],
            prompt=prompt_data["prompt"],
            tools=prompt_data.get("tools"),
            tool_choice=prompt_data.get("tool_choice"),
            version=prompt_data["version"],
            is_default=prompt_data["is_default"],
            model=prompt_data.get("model"),
            org_model_config_id=prompt_data.get("org_model_config_id"),
            parameters=prompt_data.get("parameters"),
            hash=prompt_data.get("hash"),
            created_at=prompt_data.get("created_at"),
            updated_at=prompt_data.get("updated_at"),
            org_model_config=org_model_config,
        )

    @staticmethod
    def run(
        slug: str,
        variables: Dict[str, Any],
        version: Optional[int] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        parameters: Optional[ModelOptions] = None,
        log_prompt_run: Optional[bool] = None,
        metadata: Optional[PromptRunMetadata] = None,
    ) -> PromptExecution:
        """
        Runs a prompt.

        Parameters:
        - slug (str): The slug of the prompt.
        - variables ([Dict[str, Any]): The variables to use for the prompt.
        - version (Optional[int]): Optional version of the prompt.
        - model (Optional[str]): Optional model for the prompt.
        - provider (Optional[str]): Optional provider.
        - parameters (Optional[Dict[str, Any]]): Optional parameters.
        - log_prompt_run (Optional[bool]): Optional boolean to log prompt run or not. By default, on every prompt execution, prompt run is logged.
        - metadata (Optional[PromptRunMetadata]): Optional metadata for the prompt run.

        Returns:
        - The prompt execution object.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        request_data = {
            "variables": variables,
            "version": version,
            "provider": provider,
            "model": model,
            "parameters": parameters,
            "log_prompt_run": log_prompt_run,
            "metadata": metadata,
        }

        request_data = {k: v for k, v in request_data.items() if v is not None}

        try:
            response_data = AthinaApiService.run_prompt(slug, request_data)
        except Exception as e:
            raise CustomException("Error running prompt", str(e))

        return PromptExecution(
            id=response_data["prompt"]["id"],
            user_id=response_data["prompt"]["user_id"],
            org_id=response_data["prompt"]["org_id"],
            workspace_slug=response_data["prompt"]["workspace_slug"],
            prompt_template_id=response_data["prompt"]["prompt_template_id"],
            variables=response_data["prompt"]["variables"],
            language_model_id=response_data["prompt"]["language_model_id"],
            org_model_config_id=response_data["prompt"]["org_model_config_id"],
            prompt_sent=response_data["prompt"]["prompt_sent"],
            prompt_response=response_data["prompt"]["prompt_response"],
            tools=response_data["prompt"]["tools"],
            tool_choice=response_data["prompt"]["tool_choice"],
            prompt_tokens=response_data["prompt"]["prompt_tokens"],
            completion_tokens=response_data["prompt"]["completion_tokens"],
            total_tokens=response_data["prompt"]["total_tokens"],
            cost=response_data["prompt"]["cost"],
            response_time=response_data["prompt"]["response_time"],
            options=ModelOptions(**response_data["prompt"].get("options", {})),
            grader_feedback=response_data["prompt"].get("grader_feedback"),
            created_at=response_data["prompt"]["created_at"],
            updated_at=response_data["prompt"]["updated_at"],
        )


@dataclass
class Slug:
    id: str
    org_id: str
    workspace_slug: str
    name: str
    directory: Optional[str] = None
    starred: bool = False
    emoji: Optional[str] = None
    created_by: str = ""
    created_at: str = ""
    updated_at: str = ""
    user: Optional[Dict[str, Any]] = None
    is_default: bool = False

    @staticmethod
    def list() -> List["Slug"]:
        """
        Get all prompt slugs by calling the Athina API.

        Returns:
        - A list of prompt slugs.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            slugs_data = AthinaApiService.get_all_prompt_slugs()
        except Exception as e:
            raise CustomException("Error fetching all prompt slugs", str(e))

        return [
            Slug(
                id=slug["id"],
                org_id=slug["org_id"],
                workspace_slug=slug["workspace_slug"],
                name=slug["name"],
                directory=slug.get("directory"),
                starred=slug["starred"],
                emoji=slug.get("emoji"),
                created_by=slug["created_by"],
                created_at=slug["created_at"],
                updated_at=slug["updated_at"],
                user=slug.get("user"),
                is_default=slug["is_default"],
            )
            for slug in slugs_data
        ]

    @staticmethod
    def delete(slug: str) -> str:
        """
        Delete a prompt slug and its corresponding templates by calling the Athina API.

        Parameters:
        - slug (str): The slug to delete.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            response = AthinaApiService.delete_prompt_slug(slug)
            return response
        except Exception as e:
            raise CustomException("Error deleting prompt slug", str(e))
