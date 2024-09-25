from typing import List, Dict, Optional
from athina_client.app_base_url import AthinaAppBaseUrl
from athina_client.datasets.dataset import Dataset
from athina_client.eval.interface import Eval
from athina_client.services.athina_api_service import AthinaApiService


class EvalLogger:

    @staticmethod
    def create_dataset_and_log_results(
        rows: List[Dict],
        dataset_name: Optional[str],
        evals: List[Eval],
        eval_results: List[Dict],
    ) -> None:
        """Log results to Athina and print the URL for viewing results."""
        if dataset_name is None:
            eval_names = [eval_obj.name for eval_obj in evals]
            dataset_name = f"Batch Eval: {', '.join(eval_names)}"

        try:
            dataset = Dataset.create(
                name=dataset_name,
                description=f"Dataset created for {dataset_name}",
                rows=rows,
            )
            dataset_id = dataset.id
        except Exception as e:
            raise

        for eval_obj in evals:
            EvalLogger._log_results_to_athina(
                dataset_id=dataset_id,
                eval=eval_obj,
                eval_results=[
                    result[f"{eval_obj.display_name}_athina_eval_result"]
                    for result in eval_results
                ],
            )

        APP_BASE_URL = AthinaAppBaseUrl.get_url()
        print(f"View the results at {APP_BASE_URL}/develop/{dataset_id}")

    @staticmethod
    def _log_results_to_athina(
        dataset_id: str,
        eval: Eval,
        eval_results: List[Dict],
    ):

        # Log the results of a single eval to Athina API
        eval_config = eval.to_config()
        llm_engine = getattr(eval, "_model", None)
        development_eval_config = {
            "eval_type_id": eval.name,
            "eval_display_name": eval.display_name,
            "eval_config": eval_config,
            "llm_engine": llm_engine,
        }
        AthinaApiService.log_eval_results_to_dataset(
            eval_results_with_config={
                "eval_results": eval_results,
                "development_eval_config": development_eval_config,
            },
            dataset_id=dataset_id,
        )
