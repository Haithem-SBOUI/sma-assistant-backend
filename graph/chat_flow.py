import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from chat_schema import ChatRequest, ChatResponse
from gemma_client import get_gemma_client
from utils.llm import process_llm_response, create_fallback_response

logger = logging.getLogger(__name__)


class ChatState(TypedDict):
    """State object for the chat workflow"""
    request: ChatRequest
    raw_response: str
    response: ChatResponse
    error: str
    messages: Annotated[list, add_messages]


class ChatWorkflow:
    """LangGraph workflow for processing SMA chat requests"""
    
    def __init__(self):
        self.gemma_client = get_gemma_client()
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the state graph
        workflow = StateGraph(ChatState)
        
        # Add nodes
        workflow.add_node("start", self.start_node)
        workflow.add_node("chat", self.chat_node)
        workflow.add_node("validation", self.validation_node)
        workflow.add_node("end", self.end_node)
        
        # Add edges
        workflow.set_entry_point("start")
        workflow.add_edge("start", "chat")
        workflow.add_edge("chat", "validation")
        workflow.add_edge("validation", "end")
        workflow.add_edge("end", END)
        
        return workflow.compile()
    
    def start_node(self, state: ChatState) -> ChatState:
        """
        Initial node - process the chat request
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state
        """
        logger.info(f"Starting chat workflow for message: {state['request'].message[:50]}...")
        
        return {
            **state,
            "raw_response": "",
            "error": "",
            "messages": []
        }
    
    def chat_node(self, state: ChatState) -> ChatState:
        """
        Chat node - call Gemma LLM
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with LLM response
        """
        try:
            logger.info("Calling Gemma LLM...")
            
            # Call Gemma synchronously (async handling done in client)
            result = self.gemma_client.chat_sync(state["request"].message)
            
            if result["success"]:
                return {
                    **state,
                    "raw_response": result["response"],
                    "error": ""
                }
            else:
                return {
                    **state,
                    "raw_response": "",
                    "error": result["error"]
                }
        
        except Exception as e:
            error_msg = f"Error in chat node: {str(e)}"
            logger.error(error_msg)
            return {
                **state,
                "raw_response": "",
                "error": error_msg
            }
    
    def validation_node(self, state: ChatState) -> ChatState:
        """
        Validation node - parse and validate LLM response
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with validated response
        """
        try:
            if state.get("error") or not state.get("raw_response"):
                # Create fallback response for errors
                response = create_fallback_response()
            else:
                # Process the raw response
                response = process_llm_response(
                    state["raw_response"], 
                    state["request"].message
                )
            
            return {
                **state,
                "response": response
            }
        
        except Exception as e:
            error_msg = f"Error in validation node: {str(e)}"
            logger.error(error_msg)
            return {
                **state,
                "response": create_fallback_response(),
                "error": error_msg
            }
    
    def end_node(self, state: ChatState) -> ChatState:
        """
        End node - finalize the response
        
        Args:
            state: Current workflow state
            
        Returns:
            Final state
        """
        logger.info("Chat workflow completed successfully")
        return state
    
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat request through the workflow
        
        Args:
            request: The chat request to process
            
        Returns:
            ChatResponse object
        """
        try:
            # Initial state
            initial_state = ChatState(
                request=request,
                raw_response="",
                response=None,
                error="",
                messages=[]
            )
            
            # Run the workflow
            final_state = await self.workflow.ainvoke(initial_state)
            
            return final_state["response"]
        
        except Exception as e:
            logger.error(f"Error processing chat workflow: {e}")
            return create_fallback_response()


# Global workflow instance
_workflow_instance = None


def get_chat_workflow() -> ChatWorkflow:
    """Get or create the global chat workflow instance"""
    global _workflow_instance
    if _workflow_instance is None:
        _workflow_instance = ChatWorkflow()
    return _workflow_instance
