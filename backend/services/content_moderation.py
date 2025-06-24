from langchain.llms import Ollama
from langchain.schema import BaseOutputParser
from typing import Dict, Any
import re
import logging
from config import settings

logger = logging.getLogger(__name__)

class ContentModerationResult:
    def __init__(self, is_clean: bool, message: str, score: float = 0.0):
        self.is_clean = is_clean
        self.message = message
        self.score = score

class ContentModerationParser(BaseOutputParser):
    """Custom parser for content moderation results"""
    
    def parse(self, text: str) -> ContentModerationResult:
        # Look for JSON-like response
        try:
            import json
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return ContentModerationResult(
                    is_clean=data.get('is_clean', True),
                    message=data.get('message', 'Content analysis complete'),
                    score=data.get('score', 0.0)
                )
        except:
            pass
        
        # Fallback to text analysis
        text_lower = text.lower()
        is_clean = not any(word in text_lower for word in [
            'inappropriate', 'offensive', 'profanity', 'vulgar', 'hate', 'toxic'
        ])
        
        return ContentModerationResult(
            is_clean=is_clean,
            message="Content reviewed" if is_clean else "Content may contain inappropriate material",
            score=0.1 if not is_clean else 0.9
        )

class LLMContentModerator:
    """LLM-based content moderation service using Ollama"""
    
    def __init__(self):
        self.llm = None
        self.parser = ContentModerationParser()
    
    async def initialize(self):
        """Initialize the LLM connection"""
        try:
            self.llm = Ollama(
                base_url=settings.ollama_host,
                model=settings.ollama_model,
                temperature=0.1  # Low temperature for consistent moderation
            )
            logger.info(f"LLM Content Moderator initialized with {settings.ollama_model}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            self.llm = None
    
    async def moderate_content(self, text: str) -> ContentModerationResult:
        """Moderate content using LLM"""
        if not self.llm:
            logger.warning("LLM not available, using fallback moderation")
            return self._fallback_moderation(text)
        
        prompt = f"""
You are a content moderator. Analyze the following text for:
1. Profanity and vulgar language
2. Hate speech or discriminatory content
3. Spam or inappropriate promotional content
4. Overall tone and professionalism

Text to analyze: "{text}"

Respond with a JSON object containing:
- "is_clean": boolean (true if content is appropriate)
- "message": string (explanation of the decision)
- "score": float (0-1, where 1 is completely clean)

JSON Response:
"""
        
        try:
            response = await self.llm.ainvoke(prompt)
            result = self.parser.parse(response)
            logger.info(f"Content moderation result: {result.is_clean} - {result.message}")
            return result
        except Exception as e:
            logger.error(f"LLM moderation failed: {e}")
            return self._fallback_moderation(text)
    
    def _fallback_moderation(self, text: str) -> ContentModerationResult:
        """Fallback moderation using basic word filtering"""
        prohibited_words = [
            'damn', 'hell', 'shit', 'fuck', 'bitch', 'asshole', 'bastard',
            'crap', 'piss', 'whore', 'slut', 'faggot', 'nigger', 'retard',
            'stupid', 'idiot', 'moron', 'dumb', 'hate', 'kill', 'die'
        ]
        
        text_lower = text.lower()
        found_words = [word for word in prohibited_words if word in text_lower]
        
        if found_words:
            return ContentModerationResult(
                is_clean=False,
                message=f"Content contains prohibited words: {', '.join(found_words)}",
                score=0.2
            )
        
        # Check for excessive caps (potential spam)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.7 and len(text) > 10:
            return ContentModerationResult(
                is_clean=False,
                message="Content contains excessive capitalization",
                score=0.4
            )
        
        return ContentModerationResult(
            is_clean=True,
            message="Content appears appropriate",
            score=0.9
        )

# Global moderator instance
content_moderator = LLMContentModerator()
