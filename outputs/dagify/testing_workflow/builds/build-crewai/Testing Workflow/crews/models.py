from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class analyze_test_results_output(BaseModel):
    analysis_results: str  # Analysis results

class document_test_results_output(BaseModel):
    document_id: str  # Document ID
    document_url: str  # Document URL

class get_testing_environment_output(BaseModel):
    environment_type: str  # Type of the testing environment
    test_cases: List[str]  # List of test cases
    test_data: List[str]  # List of test data

class perform_test_cases_output(BaseModel):
    test_results: List[str]  # List of test results

class select_test_cases_output(BaseModel):
    selected_test_cases: List[str]  # List of selected test cases

