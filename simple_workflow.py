import logging
from typing import Dict, Any
from chat_schema import ChatRequest, ChatResponse
from gemma_client import get_gemma_client
from utils.llm import process_llm_response, create_fallback_response

logger = logging.getLogger(__name__)


class SimpleChatWorkflow:
    """Simple workflow for processing SMA chat requests without LangGraph complexity"""
    
    def __init__(self):
        self.gemma_client = get_gemma_client()
    
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat request through a simple workflow
        
        Args:
            request: The chat request to process
            
        Returns:
            ChatResponse object
        """
        try:
            logger.info(f"Processing chat request: {request.message[:50]}...")
            
            # Step 1: Call Gemma LLM
            result = await self.gemma_client.chat_sync(request.message)
            
            # Step 2: Process the response
            if result["success"] and result["response"]:
                response = process_llm_response(result["response"], request.message)
            else:
                error_msg = result.get("error", "Unknown error occurred")
                logger.error(f"LLM call failed: {error_msg}")
                response = create_fallback_response()
            
            logger.info(f"Generated response with confidence: {response.confidence}")
            return response
        
        except Exception as e:
            logger.error(f"Error processing chat workflow: {e}")
            return create_fallback_response()


# Global workflow instance
_workflow_instance = None


def get_chat_workflow() -> SimpleChatWorkflow:
    """Get or create the global chat workflow instance"""
    global _workflow_instance
    if _workflow_instance is None:
        _workflow_instance = SimpleChatWorkflow()
    return _workflow_instance
