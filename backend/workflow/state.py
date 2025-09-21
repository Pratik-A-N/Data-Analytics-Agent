from typing import TypedDict, List, Any, Annotated, Dict
import operator


class WorkflowState(TypedDict):
    # From InputState
    user_query: str
    table_id: str
    
    # Common fields (present in both Input and Output)
    parsed_question: Dict[str, Any]
    unique_nouns: List[str]
    sql_query: str
    results: List[Any]
    visualization: Annotated[str, operator.add]
    
    # From OutputState
    sql_valid: bool
    sql_issues: str
    answer: Annotated[str, operator.add]
    error: str
    visualization_reason: Annotated[str, operator.add]
    formatted_data_for_visualization: Dict[str, Any]