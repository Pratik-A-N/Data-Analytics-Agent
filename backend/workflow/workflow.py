from langgraph.graph import StateGraph, END
from workflow.state import WorkflowState
from workflow.SQLProcessor import SQLAgent
from workflow.DataProcessor import DataProcessor

class Workflow:
    def __init__(self):
        self.sql_agent = SQLAgent()
        self.data_formatter = DataProcessor()

    def initiate_workflow(self) -> StateGraph:
        """
        Initiates a new workflow and returns the initial state graph.
        """
        
        workflow = StateGraph(state_schema=WorkflowState)

        # Add nodes to the graph
        workflow.add_node("understand_question", self.sql_agent.understand_question)
        workflow.add_node("get_unique_nouns", self.sql_agent.get_unique_nouns)
        workflow.add_node("generate_sql", self.sql_agent.generate_sql)
        workflow.add_node("validate_and_fix_sql", self.sql_agent.validate_and_fix_sql)
        workflow.add_node("execute_sql", self.sql_agent.execute_sql)
        workflow.add_node("format_results", self.sql_agent.format_results)
        workflow.add_node("choose_visualization", self.sql_agent.choose_visualization)
        workflow.add_node("format_data_for_visualization", self.data_formatter.format_data_for_visualization)
        
        # Define edges
        workflow.add_edge("understand_question", "get_unique_nouns")
        workflow.add_edge("get_unique_nouns", "generate_sql")
        workflow.add_edge("generate_sql", "validate_and_fix_sql")
        workflow.add_edge("validate_and_fix_sql", "execute_sql")
        workflow.add_edge("execute_sql", "format_results")
        workflow.add_edge("execute_sql", "choose_visualization")
        workflow.add_edge("choose_visualization", "format_data_for_visualization")
        workflow.add_edge("format_data_for_visualization", END)
        workflow.add_edge("format_results", END)
        workflow.set_entry_point("understand_question")

        return workflow
    
    def execute_workflow(self, user_query: str, table_id: str) -> dict:
        """
        Executes the workflow with the given user query and table ID.
        """
        
        graph = self.initiate_workflow().compile();

        result = graph.invoke({
            "user_query": user_query,
            "table_id": table_id
        })

        return {
            "answer": result['answer'],
            "visualization": result['visualization'],
            "visualization_reason": result['visualization_reason'],
            "formatted_data_for_visualization": result['formatted_data_for_visualization']
        }
        
    def returnGraph(self):
        return self.initiate_workflow().compile()