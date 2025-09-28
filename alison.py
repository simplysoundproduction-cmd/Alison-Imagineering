#!/usr/bin/env python3
"""
Alison - Emotionally Intelligent Co-pilot
An AI system that blends logic with empathy, adapts to user state,
and acts as a conversational strategist and creative partner.
"""

import json
import re
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import os


class EmotionalState(Enum):
    """Detected emotional states from user input"""
    NEUTRAL = "neutral"
    EXCITED = "excited"
    FRUSTRATED = "frustrated"
    CONFUSED = "confused"
    HAPPY = "happy"
    STRESSED = "stressed"
    FOCUSED = "focused"
    CREATIVE = "creative"


class UserIntent(Enum):
    """Detected user intents"""
    HELP_REQUEST = "help_request"
    QUESTION = "question"
    CREATIVE_COLLABORATION = "creative_collaboration"
    DECISION_MAKING = "decision_making"
    EMOTIONAL_SUPPORT = "emotional_support"
    INFORMATION_SEARCH = "information_search"
    CASUAL_CONVERSATION = "casual_conversation"


@dataclass
class ConversationContext:
    """Context for a single conversation turn"""
    user_input: str
    timestamp: float
    detected_emotion: EmotionalState
    detected_intent: UserIntent
    confidence: float
    response_tone: str
    

@dataclass
class UserProfile:
    """User's learned preferences and patterns"""
    communication_style: Dict[str, float]
    values: List[str]
    conversation_patterns: Dict[str, int]
    preferred_response_style: str
    emotional_triggers: Dict[str, List[str]]


class Alison:
    """
    Main Alison AI Co-pilot class
    Emotionally intelligent, adaptive, and empathetic AI assistant
    """
    
    def __init__(self, memory_file: str = "alison_memory.json"):
        self.memory_file = memory_file
        self.conversation_history: List[ConversationContext] = []
        self.user_profile: UserProfile = self._load_or_create_profile()
        
        # Emotional intelligence patterns
        self.emotion_patterns = {
            EmotionalState.FRUSTRATED: {
                "keywords": ["stuck", "frustrated", "can't", "won't work", "annoying", "damn", "ugh"],
                "tone_indicators": ["!!", "....", "CAPS", "short sentences"]
            },
            EmotionalState.EXCITED: {
                "keywords": ["amazing", "awesome", "great", "excited", "yes!", "perfect", "love"],
                "tone_indicators": ["!", "multiple exclamations", "longer sentences"]
            },
            EmotionalState.CONFUSED: {
                "keywords": ["confused", "don't understand", "what", "how", "unclear", "?"],
                "tone_indicators": ["?", "short questions", "hesitation"]
            },
            EmotionalState.STRESSED: {
                "keywords": ["deadline", "urgent", "quickly", "stress", "overwhelmed", "too much"],
                "tone_indicators": ["short", "direct", "multiple requests"]
            }
        }
        
        # Intent detection patterns
        self.intent_patterns = {
            UserIntent.HELP_REQUEST: r"(help|assist|support|fix|solve|stuck)",
            UserIntent.QUESTION: r"(\?|what|how|why|when|where|which)",
            UserIntent.CREATIVE_COLLABORATION: r"(create|design|brainstorm|ideas|creative|imagine)",
            UserIntent.DECISION_MAKING: r"(decide|choose|should|option|alternative|recommend)",
        }
        
    def _load_or_create_profile(self) -> UserProfile:
        """Load existing user profile or create new one"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    return UserProfile(**data.get('user_profile', {}))
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Create default profile
        return UserProfile(
            communication_style={
                "formal": 0.5,
                "casual": 0.5,
                "direct": 0.5,
                "empathetic": 0.7
            },
            values=[],
            conversation_patterns={},
            preferred_response_style="balanced",
            emotional_triggers={}
        )
    
    def _save_memory(self):
        """Save conversation history and user profile"""
        memory_data = {
            "user_profile": asdict(self.user_profile),
            "conversation_count": len(self.conversation_history),
            "last_interaction": time.time()
        }
        
        with open(self.memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
    
    def detect_emotional_state(self, text: str) -> Tuple[EmotionalState, float]:
        """Detect user's emotional state from input text"""
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            # Check keywords
            for keyword in patterns["keywords"]:
                if keyword in text_lower:
                    score += 1
            
            # Check tone indicators
            if "!" in text and emotion == EmotionalState.EXCITED:
                score += 1
            if text.count("!") > 2 and emotion == EmotionalState.FRUSTRATED:
                score += 1
            if "?" in text and emotion == EmotionalState.CONFUSED:
                score += 1
            if len(text.split()) < 5 and emotion == EmotionalState.STRESSED:
                score += 0.5
                
            emotion_scores[emotion] = score
        
        # Default to neutral if no strong emotion detected
        if not emotion_scores or max(emotion_scores.values()) < 1:
            return EmotionalState.NEUTRAL, 0.8
        
        best_emotion = max(emotion_scores.keys(), key=lambda x: emotion_scores[x])
        confidence = min(emotion_scores[best_emotion] / 3.0, 1.0)
        
        return best_emotion, confidence
    
    def detect_intent(self, text: str) -> Tuple[UserIntent, float]:
        """Detect user's intent from input text"""
        text_lower = text.lower()
        
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, text_lower):
                confidence = 0.8
                return intent, confidence
        
        # Default intent based on context
        if "?" in text:
            return UserIntent.QUESTION, 0.6
        elif any(word in text_lower for word in ["alison", "help"]):
            return UserIntent.HELP_REQUEST, 0.7
        else:
            return UserIntent.CASUAL_CONVERSATION, 0.5
    
    def adapt_response_tone(self, emotion: EmotionalState, intent: UserIntent) -> str:
        """Adapt response tone based on detected emotion and intent"""
        if emotion == EmotionalState.FRUSTRATED:
            return "calm_supportive"
        elif emotion == EmotionalState.EXCITED:
            return "enthusiastic_collaborative"
        elif emotion == EmotionalState.CONFUSED:
            return "patient_clarifying"
        elif emotion == EmotionalState.STRESSED:
            return "efficient_reassuring"
        elif intent == UserIntent.CREATIVE_COLLABORATION:
            return "inspiring_creative"
        elif intent == UserIntent.DECISION_MAKING:
            return "analytical_supportive"
        else:
            return self.user_profile.preferred_response_style or "balanced"
    
    def generate_response(self, user_input: str) -> str:
        """Generate empathetic and contextually appropriate response"""
        # Detect emotion and intent
        emotion, emotion_confidence = self.detect_emotional_state(user_input)
        intent, intent_confidence = self.detect_intent(user_input)
        
        # Adapt tone
        response_tone = self.adapt_response_tone(emotion, intent)
        
        # Store context
        context = ConversationContext(
            user_input=user_input,
            timestamp=time.time(),
            detected_emotion=emotion,
            detected_intent=intent,
            confidence=min(emotion_confidence, intent_confidence),
            response_tone=response_tone
        )
        self.conversation_history.append(context)
        
        # Generate contextual response
        response = self._craft_response(user_input, emotion, intent, response_tone)
        
        # Update user profile based on interaction
        self._update_user_profile(user_input, emotion, intent)
        
        # Save memory
        self._save_memory()
        
        return response
    
    def _craft_response(self, user_input: str, emotion: EmotionalState, 
                       intent: UserIntent, tone: str) -> str:
        """Craft appropriate response based on context"""
        
        # Emotional acknowledgment
        if emotion == EmotionalState.FRUSTRATED:
            emotion_response = "I can sense this is frustrating for you. "
        elif emotion == EmotionalState.EXCITED:
            emotion_response = "I love your enthusiasm! "
        elif emotion == EmotionalState.CONFUSED:
            emotion_response = "I understand this might be unclear. "
        elif emotion == EmotionalState.STRESSED:
            emotion_response = "I can see you're working under pressure. "
        else:
            emotion_response = ""
        
        # Intent-based response
        if intent == UserIntent.HELP_REQUEST:
            intent_response = "Let me help you work through this step by step. "
        elif intent == UserIntent.CREATIVE_COLLABORATION:
            intent_response = "I'd love to explore ideas with you. "
        elif intent == UserIntent.DECISION_MAKING:
            intent_response = "Let's think through your options together. "
        elif intent == UserIntent.QUESTION:
            intent_response = "I'll do my best to clarify this for you. "
        else:
            intent_response = "I'm here to support you. "
        
        # Combine empathetic acknowledgment with helpful intent
        base_response = emotion_response + intent_response
        
        # Add specific guidance based on input
        if "alison" in user_input.lower():
            base_response += "What specifically would you like me to help you with?"
        elif any(word in user_input.lower() for word in ["stuck", "problem", "issue"]):
            base_response += "Can you tell me more about what you're working on and where you're getting stuck?"
        elif any(word in user_input.lower() for word in ["create", "design", "build"]):
            base_response += "What kind of solution are you envisioning? I can help brainstorm approaches."
        
        return base_response.strip()
    
    def _update_user_profile(self, user_input: str, emotion: EmotionalState, intent: UserIntent):
        """Update user profile based on interaction patterns"""
        # Track conversation patterns
        pattern_key = f"{emotion.value}_{intent.value}"
        self.user_profile.conversation_patterns[pattern_key] = \
            self.user_profile.conversation_patterns.get(pattern_key, 0) + 1
        
        # Adjust communication style based on user's input style
        adjustment = 0.05  # Smaller adjustment to avoid over-normalization
        if len(user_input.split()) > 20:
            self.user_profile.communication_style["formal"] += adjustment
            self.user_profile.communication_style["casual"] -= adjustment * 0.5
        else:
            self.user_profile.communication_style["casual"] += adjustment
            self.user_profile.communication_style["formal"] -= adjustment * 0.5
        
        # Ensure values stay within reasonable bounds
        for key in self.user_profile.communication_style:
            self.user_profile.communication_style[key] = max(0.1, min(0.9, 
                self.user_profile.communication_style[key]))
    
    def get_conversation_insights(self) -> Dict:
        """Provide insights about conversation patterns"""
        if not self.conversation_history:
            return {"message": "No conversation history yet"}
        
        emotions = [c.detected_emotion.value for c in self.conversation_history]
        intents = [c.detected_intent.value for c in self.conversation_history]
        
        return {
            "total_interactions": len(self.conversation_history),
            "common_emotions": max(set(emotions), key=emotions.count) if emotions else "none",
            "common_intents": max(set(intents), key=intents.count) if intents else "none",
            "communication_style": self.user_profile.communication_style,
            "conversation_patterns": self.user_profile.conversation_patterns
        }


def main():
    """Main CLI interface for Alison"""
    alison = Alison()
    
    print("🌟 Alison - Your Emotionally Intelligent Co-pilot")
    print("I'm here to listen, understand, and help. Type 'exit' to end our conversation.")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nAlison: It's been wonderful talking with you. Take care! 💫")
                break
            
            if not user_input:
                continue
            
            response = alison.generate_response(user_input)
            print(f"\nAlison: {response}")
            
        except KeyboardInterrupt:
            print("\n\nAlison: Until next time! 👋")
            break
        except Exception as e:
            print(f"\nAlison: I apologize, I encountered an error: {str(e)}")
            print("Let me try to help you in another way.")


if __name__ == "__main__":
    main()