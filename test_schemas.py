import pytest
import json
from datetime import datetime
from pydantic import ValidationError
from chat_schema import ChatRequest, ChatResponse, HealthResponse


class TestChatRequest:
    """Test ChatRequest model"""
    
    def test_valid_request(self):
        """Test valid chat request creation"""
        request = ChatRequest(message="What is SMA?")
        assert request.message == "What is SMA?"
    
    def test_empty_message(self):
        """Test empty message validation"""
        with pytest.raises(ValidationError):
            ChatRequest(message="")
    
    def test_whitespace_only_message(self):
        """Test whitespace-only message validation"""
        with pytest.raises(ValidationError):
            ChatRequest(message="   ")
    
    def test_message_too_long(self):
        """Test message length validation"""
        long_message = "x" * 2001
        with pytest.raises(ValidationError):
            ChatRequest(message=long_message)
    
    def test_message_stripping(self):
        """Test message whitespace stripping"""
        request = ChatRequest(message="  What is SMA?  ")
        assert request.message == "What is SMA?"


class TestChatResponse:
    """Test ChatResponse model"""
    
    def test_valid_response(self):
        """Test valid chat response creation"""
        response = ChatResponse(
            answer="SMA is Spinal Muscular Atrophy",
            confidence=0.9
        )
        assert response.answer == "SMA is Spinal Muscular Atrophy"
        assert response.confidence == 0.9
        assert isinstance(response.timestamp, datetime)
    
    def test_empty_answer(self):
        """Test empty answer validation"""
        with pytest.raises(ValidationError):
            ChatResponse(answer="", confidence=0.9)
    
    def test_confidence_bounds(self):
        """Test confidence bounds validation"""
        # Test valid bounds
        ChatResponse(answer="Valid answer", confidence=0.0)
        ChatResponse(answer="Valid answer", confidence=1.0)
        ChatResponse(answer="Valid answer", confidence=0.5)
        
        # Test invalid bounds
        with pytest.raises(ValidationError):
            ChatResponse(answer="Invalid answer", confidence=-0.1)
        
        with pytest.raises(ValidationError):
            ChatResponse(answer="Invalid answer", confidence=1.1)
    
    def test_answer_stripping(self):
        """Test answer whitespace stripping"""
        response = ChatResponse(
            answer="  SMA is a genetic disorder  ",
            confidence=0.8
        )
        assert response.answer == "SMA is a genetic disorder"


class TestHealthResponse:
    """Test HealthResponse model"""
    
    def test_valid_health_response(self):
        """Test valid health response creation"""
        response = HealthResponse()
        assert response.status == "ok"
        assert isinstance(response.timestamp, datetime)
    
    def test_custom_status(self):
        """Test custom status"""
        response = HealthResponse(status="healthy")
        assert response.status == "healthy"
