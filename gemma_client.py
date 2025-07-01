import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GemmaClient:
    """Async client for Google Gemma via LangChain with robust error handling"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Initialize the LangChain Google GenAI client
        self.llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMMA_MODEL_NAME"),  # Using Gemini Pro as it's more accessible than Gemma
            google_api_key=self.api_key,
            temperature=0.1,  # Low temperature for medical accuracy
            max_tokens=1000,
            timeout=30.0,
            convert_system_message_to_human=True  # Fix for SystemMessage support
        )
        
        # Load system prompt
        self.system_prompt = self._load_system_prompt()
        
    def _load_system_prompt(self) -> str:
        """Load system prompt from file"""
        try:
            with open("system_prompt.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.warning("system_prompt.txt not found, using default prompt")
            return """You are a medical assistant for SMA. Respond only in JSON format: 
            {"answer": "your response", "confidence": 0.95}"""
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, Exception))
    )
    async def chat_async(self, user_message: str) -> Dict[str, Any]:
        """
        Send a message to Gemma and get response with retry logic
        
        Args:
            user_message: The user's question about SMA
            
        Returns:
            Dict containing the AI response
        """
        try:
            logger.info(f"Sending request to Gemini: {user_message[:100]}...")
            
            # Combine system prompt with user message for Google GenAI
            # Since convert_system_message_to_human=True, system message becomes human message
            combined_message = f"{self.system_prompt}\n\nUser Question: {user_message}"
            
            # Use single HumanMessage for compatibility
            messages = [HumanMessage(content=combined_message)]
            
            # Call the LLM asynchronously
            response = await self.llm.ainvoke(messages)
            
            # Extract content
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            logger.info(f"Received response from Gemini: {response_text[:100]}...")
            
            return {
                "response": response_text,
                "success": True,
                "error": None
            }
            
        except Exception as e:
            error_msg = f"Error calling Gemini: {str(e)}"
            logger.error(error_msg)
            
            return {
                "response": None,
                "success": False,
                "error": error_msg
            }
    
    async def chat_sync(self, user_message: str) -> Dict[str, Any]:
        """Synchronous wrapper for chat_async"""
        return await self.chat_async(user_message)


# Global client instance
_client_instance: Optional[GemmaClient] = None


def get_gemma_client() -> GemmaClient:
    """Get or create the global Gemma client instance"""
    global _client_instance
    if _client_instance is None:
        _client_instance = GemmaClient()
    return _client_instance
