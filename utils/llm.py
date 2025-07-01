import json
import re
import logging
from typing import Dict, Any, Optional
from chat_schema import ChatResponse

logger = logging.getLogger(__name__)


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from text that may contain fenced code blocks or plain JSON
    
    Args:
        text: Raw text that may contain JSON
        
    Returns:
        Parsed JSON dict or None if extraction fails
    """
    if not text or not text.strip():
        logger.warning("Empty text provided for JSON extraction")
        return None
    
    # Clean the text
    text = text.strip()
    
    # Try to extract JSON from fenced code blocks first
    json_patterns = [
        r'```json\s*\n(.*?)\n```',  # ```json ... ```
        r'```\s*\n(.*?)\n```',     # ``` ... ```
        r'`([^`]*)`',              # `...`
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue
    
    # Try to parse the entire text as JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON-like structure in the text
    json_start = text.find('{')
    json_end = text.rfind('}')
    
    if json_start != -1 and json_end != -1 and json_end > json_start:
        potential_json = text[json_start:json_end + 1]
        try:
            return json.loads(potential_json)
        except json.JSONDecodeError:
            pass
    
    logger.warning(f"Could not extract valid JSON from text: {text[:200]}...")
    return None


def validate_chat_response(data: Dict[str, Any]) -> ChatResponse:
    """
    Validate and convert dict to ChatResponse model
    
    Args:
        data: Dictionary containing response data
        
    Returns:
        Validated ChatResponse object
        
    Raises:
        ValueError: If validation fails
    """
    try:
        # Ensure required fields exist
        if 'answer' not in data:
            raise ValueError("Missing 'answer' field in response")
        if 'confidence' not in data:
            raise ValueError("Missing 'confidence' field in response")
        
        # Validate and create ChatResponse
        return ChatResponse(**data)
    
    except Exception as e:
        logger.error(f"ChatResponse validation failed: {e}")
        raise ValueError(f"Invalid ChatResponse format: {e}")


def create_fallback_response(error_message: str = "I apologize, but I'm having trouble processing your request right now.") -> ChatResponse:
    """
    Create a fallback response when LLM fails
    
    Args:
        error_message: Custom error message
        
    Returns:
        ChatResponse with fallback content
    """
    return ChatResponse(
        answer=f"{error_message} Please try rephrasing your question about Spinal Muscular Atrophy (SMA), or contact a healthcare professional for immediate assistance.",
        confidence=0.0
    )


def process_llm_response(raw_response: str, user_message: str) -> ChatResponse:
    """
    Process raw LLM response into validated ChatResponse
    
    Args:
        raw_response: Raw text from LLM
        user_message: Original user message for context
        
    Returns:
        Validated ChatResponse object
    """
    try:
        # Extract JSON from response
        json_data = extract_json_from_text(raw_response)
        
        if json_data is None:
            logger.warning("Could not extract JSON from LLM response")
            return create_fallback_response("I received an invalid response format.")
        
        # Validate the response
        chat_response = validate_chat_response(json_data)
        
        # Additional validation - ensure it's SMA-related
        if not _is_sma_related_response(chat_response.answer):
            logger.warning("Response doesn't appear to be SMA-related")
            return ChatResponse(
                answer="I can only provide information about Spinal Muscular Atrophy (SMA). Please ask a question related to SMA, its symptoms, treatments, or management.",
                confidence=0.9
            )
        
        return chat_response
        
    except Exception as e:
        logger.error(f"Error processing LLM response: {e}")
        return create_fallback_response()


def _is_sma_related_response(answer: str) -> bool:
    """
    Check if response appears to be SMA-related
    
    Args:
        answer: The answer text to check
        
    Returns:
        True if appears SMA-related, False otherwise
    """
    sma_keywords = [
        'sma', 'spinal muscular atrophy', 'motor neuron', 'smn1', 'smn2',
        'muscle weakness', 'muscle atrophy', 'spinraza', 'zolgensma',
        'risdiplam', 'evrysdi', 'motor unit', 'anterior horn'
    ]
    
    answer_lower = answer.lower()
    return any(keyword in answer_lower for keyword in sma_keywords)
