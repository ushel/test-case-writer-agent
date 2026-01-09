from langsmith import Client
from langsmith.utils import LangSmithError
import logging

client = Client()

def upload_test_cases(dataset_name: str, test_cases: list):
    """
    Attempts to upload test cases to LangSmith dataset.
    If forbidden, logs warning and continues gracefully.
    """
    try:
        # Try to find or create dataset
        dataset = None
        for ds in client.list_datasets():
            if ds.name == dataset_name:
                dataset = ds
                break

        if dataset is None:
            dataset = client.create_dataset(
                dataset_name=dataset_name,
                description="Auto-generated test cases for agent evaluation"
            )

        for tc in test_cases:
            client.create_example(
                dataset_id=dataset.id,
                inputs={"input": tc["input"]},
                outputs={
                    "expected_tool": tc.get("expected_tool"),
                    "expected_behavior": tc.get("expected_behavior")
                }
            )

        return {
            "dataset_name": dataset_name,
            "dataset_uploaded": True
        }

    except LangSmithError as e:
        logging.warning(
            f"LangSmith dataset upload skipped (permission issue): {e}"
        )
        return {
            "dataset_name": dataset_name,
            "dataset_uploaded": False
        }
