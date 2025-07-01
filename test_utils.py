import pytest
import json
from unittest.mock import patch, MagicMock
from utils.llm import (
    extract_json_from_text,
    validate_chat_response,
    create_fallback_response,
    process_llm_response,
    _is_sma_related_response
)
from chat_schema import ChatResponse


class TestJSONExtraction:
    """Test JSON extraction utilities"""
    
    def test_extract_json_from_fenced_block(self):
        """Test extracting JSON from fenced code block"""
        text = '```json\n{"answer": "SMA info", "confidence": 0.9}\n```'
        result = extract_json_from_text(text)
        expected = {"answer": "SMA info", "confidence": 0.9}
        assert result == expected
    
    def test_extract_json_from_plain_text(self):
        """Test extracting JSON from plain text"""
        text = '{"answer": "SMA info", "confidence": 0.9}'
        result = extract_json_from_text(text)
        expected = {"answer": "SMA info", "confidence": 0.9}
        assert result == expected
    
    def test_extract_json_with_surrounding_text(self):
        """Test extracting JSON with surrounding text"""
        text = 'Here is the response: {"answer": "SMA info", "confidence": 0.9} Hope this helps!'
        result = extract_json_from_text(text)
        expected = {"answer": "SMA info", "confidence": 0.9}
        assert result == expected
    
    def test_extract_json_invalid_text(self):
        """Test extracting JSON from invalid text"""
        text = "This is not JSON at all"
        result = extract_json_from_text(text)
        assert result is None
    
    def test_extract_json_empty_text(self):
        """Test extracting JSON from empty text"""
        result = extract_json_from_text("")
        assert result is None


class TestChatResponseValidation:
    """Test ChatResponse validation"""
    
    def test_validate_valid_response(self):
        """Test validating valid response data"""
        data = {"answer": "SMA is a genetic disorder", "confidence": 0.9}
        response = validate_chat_response(data)
        assert isinstance(response, ChatResponse)
        assert response.answer == "SMA is a genetic disorder"
        assert response.confidence == 0.9
    
    def test_validate_missing_answer(self):
        """Test validation with missing answer"""
        data = {"confidence": 0.9}
        with pytest.raises(ValueError, match="Missing 'answer' field"):
            validate_chat_response(data)
    
    def test_validate_missing_confidence(self):
        """Test validation with missing confidence"""
        data = {"answer": "SMA info"}
        with pytest.raises(ValueError, match="Missing 'confidence' field"):
            validate_chat_response(data)


class TestFallbackResponse:
    """Test fallback response creation"""
    
    def test_create_default_fallback(self):
        """Test creating default fallback response"""
        response = create_fallback_response()
        assert isinstance(response, ChatResponse)
        assert response.confidence == 0.0
        assert "trouble processing" in response.answer
        assert "SMA" in response.answer
    
    def test_create_custom_fallback(self):
        """Test creating custom fallback response"""
        custom_message = "Custom error occurred"
        response = create_fallback_response(custom_message)
        assert custom_message in response.answer
        assert response.confidence == 0.0


class TestSMARelatedCheck:
    """Test SMA-related response checking"""
    
    def test_sma_related_true(self):
        """Test detecting SMA-related content"""
        sma_texts = [
            "Spinal Muscular Atrophy is a genetic disorder",
            "SMA affects motor neurons",
            "Spinraza is a treatment for SMA",
            "SMN1 gene mutation causes SMA"
        ]
        
        for text in sma_texts:
            assert _is_sma_related_response(text) is True
    
    def test_sma_related_false(self):
        """Test detecting non-SMA content"""
        non_sma_texts = [
            "The weather is nice today",
            "I like pizza",
            "Python is a programming language"
        ]
        
        for text in non_sma_texts:
            assert _is_sma_related_response(text) is False


class TestProcessLLMResponse:
    """Test LLM response processing"""
    
    def test_process_valid_response(self):
        """Test processing valid LLM response"""
        raw_response = '{"answer": "SMA is a genetic disorder affecting motor neurons", "confidence": 0.9}'
        user_message = "What is SMA?"
        
        response = process_llm_response(raw_response, user_message)
        
        assert isinstance(response, ChatResponse)
        assert "SMA" in response.answer
        assert response.confidence == 0.9
    
    def test_process_invalid_json(self):
        """Test processing invalid JSON response"""
        raw_response = "This is not valid JSON"
        user_message = "What is SMA?"
        
        response = process_llm_response(raw_response, user_message)
        
        assert isinstance(response, ChatResponse)
        assert response.confidence == 0.0
        assert "invalid response format" in response.answer
    
    def test_process_non_sma_response(self):
        """Test processing non-SMA related response"""
        raw_response = '{"answer": "I like talking about weather", "confidence": 0.9}'
        user_message = "Tell me about weather"
        
        response = process_llm_response(raw_response, user_message)
        
        assert isinstance(response, ChatResponse)
        assert "SMA" in response.answer
        assert "only provide information about" in response.answer
