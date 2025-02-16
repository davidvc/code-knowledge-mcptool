"""LLM-based evaluator for code chat responses."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import os
import httpx

@dataclass
class EvaluationResult:
    """Result of response evaluation."""
    score: float  # 0.0 to 1.0
    reasoning: str
    is_acceptable: bool

class ResponseEvaluator(ABC):
    """Abstract base class for response evaluators."""
    
    @abstractmethod
    def evaluate_response(
        self,
        query: str,
        response: str,
        context: Optional[str] = None
    ) -> EvaluationResult:
        """Evaluate a response for accuracy and relevance."""
        pass

class OpenRouterEvaluator(ResponseEvaluator):
    """Evaluates responses using OpenRouter's API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "google/palm-2-chat-bison"):
        """Initialize the evaluator.
        
        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY environment variable)
            model: Model to use for evaluation (defaults to PaLM 2)
        """
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key must be provided either as argument or OPENROUTER_API_KEY environment variable")
        self.model = model
        
    def evaluate_response(
        self,
        query: str,
        response: str,
        context: Optional[str] = None
    ) -> EvaluationResult:
        """Evaluate a response for accuracy and relevance.
        
        Args:
            query: Original question asked
            response: Response from the code chat tool
            context: Optional additional context (e.g., relevant docs)
            
        Returns:
            EvaluationResult with score and reasoning
        """
        prompt = f"""You are evaluating the quality of a response to a code-related query.

Question: {query}

Response: {response}

{f'Additional Context: {context}' if context else ''}

Evaluate the response on:
1. Accuracy - Is the information correct?
2. Relevance - Does it answer the question?
3. Completeness - Is the answer thorough?
4. Clarity - Is it well-explained?

Provide:
1. A score from 0.0 to 1.0
2. Your reasoning
3. Whether the response is acceptable (score >= 0.7)

Format your response as:
SCORE: [number]
REASONING: [your analysis]
ACCEPTABLE: [true/false]
"""
        
        try:
            response = httpx.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://github.com/rooveterinaryinc/code_mcp_tool",
                    "X-Title": "Code Chat Tool Tests",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a code expert evaluating responses."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3
                },
                timeout=30.0
            )
            response.raise_for_status()
            
            # Parse evaluation response
            eval_text = response.json()["choices"][0]["message"]["content"]
            
            # Extract score, reasoning, and acceptability
            lines = eval_text.strip().split("\n")
            score = float(lines[0].split(": ")[1])
            reasoning = lines[1].split(": ")[1]
            acceptable = lines[2].split(": ")[1].lower() == "true"
            
            return EvaluationResult(
                score=score,
                reasoning=reasoning,
                is_acceptable=acceptable
            )
            
        except Exception as e:
            raise Exception(f"Evaluation failed: {str(e)}")
