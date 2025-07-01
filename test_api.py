import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json
import os

# Set test environment variables
os.environ["GOOGLE_API_KEY"] = "test_key"

from api.main import app
from chat_schema import ChatResponse


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/api/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data


class TestChatEndpoint:
    """Test chat endpoint"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
    
    @patch('simple_workflow.get_gemma_client')
    def test_chat_success(self, mock_get_client):
        """Test successful chat interaction"""
        # Mock the Gemma client
        mock_client = MagicMock()
        mock_client.chat_sync.return_value = {
            "success": True,
            "response": '{"answer": "SMA is Spinal Muscular Atrophy, a genetic disorder.", "confidence": 0.9}',
            "error": None
        }
        mock_get_client.return_value = mock_client
        
        # Make request
        request_data = {"message": "What is SMA?"}
        response = self.client.post("/api/chat", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert "confidence" in data
        assert "timestamp" in data
        assert "SMA" in data["answer"]
        assert 0.0 <= data["confidence"] <= 1.0
    
    @patch('simple_workflow.get_gemma_client')
    def test_chat_llm_failure(self, mock_get_client):
        """Test chat with LLM failure"""
        # Mock failed LLM call
        mock_client = MagicMock()
        mock_client.chat_sync.return_value = {
            "success": False,
            "response": None,
            "error": "LLM service unavailable"
        }
        mock_get_client.return_value = mock_client
        
        # Make request
        request_data = {"message": "What is SMA?"}
        response = self.client.post("/api/chat", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return fallback response
        assert "answer" in data
        assert data["confidence"] == 0.0
        assert "trouble processing" in data["answer"]
    
    def test_chat_invalid_request(self):
        """Test chat with invalid request"""
        # Empty message
        request_data = {"message": ""}
        response = self.client.post("/api/chat", json=request_data)
        assert response.status_code == 422
        
        # Missing message
        request_data = {}
        response = self.client.post("/api/chat", json=request_data)
        assert response.status_code == 422
    
    def test_chat_message_too_long(self):
        """Test chat with message too long"""
        request_data = {"message": "x" * 2001}
        response = self.client.post("/api/chat", json=request_data)
        assert response.status_code == 422


class TestCORSAndGeneral:
    """Test CORS and general functionality"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_cors_headers(self):
        """Test CORS headers"""
        response = self.client.options("/api/chat")
        assert response.status_code == 200
    
    def test_404_endpoint(self):
        """Test 404 endpoint"""
        response = self.client.get("/nonexistent")
        assert response.status_code == 404


class TestEndToEnd:
    """End-to-end integration tests"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
    
    @patch('simple_workflow.get_gemma_client')
    def test_full_chat_flow(self, mock_get_client):
        """Test complete chat flow from request to response"""
        # Mock successful LLM response
        mock_client = MagicMock()
        mock_client.chat_sync.return_value = {
            "success": True,
            "response": '''
            SMA stands for Spinal Muscular Atrophy. Here's the information:
            
            ```json
            {
                "answer": "Spinal Muscular Atrophy (SMA) is a genetic neuromuscular disorder that affects motor neurons in the spinal cord, leading to muscle weakness and atrophy. It is caused by mutations in the SMN1 gene.",
                "confidence": 0.95
            }
            ```
            ''',
            "error": None
        }
        mock_get_client.return_value = mock_client
        
        # Test the complete flow
        request_data = {"message": "What is SMA and what causes it?"}
        response = self.client.post("/api/chat", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "answer" in data
        assert "confidence" in data
        assert "timestamp" in data
        
        # Verify content quality
        answer = data["answer"].lower()
        assert "spinal muscular atrophy" in answer
        assert "genetic" in answer
        assert data["confidence"] == 0.95
        
        # Verify timestamp format
        from datetime import datetime
        timestamp_str = data["timestamp"]
        datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))  # Should not raise exception
