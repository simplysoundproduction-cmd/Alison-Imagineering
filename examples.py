#!/usr/bin/env python3
"""
Examples of integrating Alison into different applications
"""

from alison import Alison, EmotionalState, UserIntent
import time


def example_1_simple_integration():
    """Example 1: Simple integration in any application"""
    print("=== Example 1: Simple Integration ===")
    
    alison = Alison("example1_memory.json")
    
    # Simulate user interactions in an app
    user_messages = [
        "This feature isn't working properly!",
        "Can you help me understand how this works?", 
        "I have an exciting idea for improvement!",
        "I need to decide between two options quickly."
    ]
    
    for message in user_messages:
        print(f"User: {message}")
        response = alison.generate_response(message)
        print(f"Alison: {response}")
        print()


def example_2_emotional_coaching():
    """Example 2: Emotional coaching and support"""
    print("=== Example 2: Emotional Coaching ===")
    
    alison = Alison("coaching_memory.json")
    
    # Simulate a stressed user working through challenges
    coaching_session = [
        "I'm feeling overwhelmed with all these deadlines",
        "I don't think I can handle all this work",
        "Maybe I should just give up on this project",
        "Actually, you're right. Let me break this down step by step"
    ]
    
    for message in coaching_session:
        print(f"User: {message}")
        response = alison.generate_response(message)
        print(f"Alison: {response}")
        
        # Show emotional analysis
        emotion, confidence = alison.detect_emotional_state(message)
        print(f"[Emotional State: {emotion.value} (confidence: {confidence:.2f})]")
        print()


def example_3_creative_collaboration():
    """Example 3: Creative brainstorming partner"""
    print("=== Example 3: Creative Collaboration ===")
    
    alison = Alison("creative_memory.json")
    
    # Simulate a creative brainstorming session
    creative_session = [
        "I want to design a mobile app that helps people",
        "What if we focused on mental wellness and mindfulness?",
        "I love that direction! How can we make it engaging?",
        "What features would make users want to use it daily?"
    ]
    
    for message in creative_session:
        print(f"User: {message}")
        response = alison.generate_response(message)
        print(f"Alison: {response}")
        
        # Show intent analysis
        intent, confidence = alison.detect_intent(message)
        print(f"[Intent: {intent.value} (confidence: {confidence:.2f})]")
        print()


def example_4_decision_support():
    """Example 4: Decision-making assistance"""
    print("=== Example 4: Decision Support ===")
    
    alison = Alison("decision_memory.json")
    
    # Simulate decision-making process
    decision_process = [
        "I need to choose between three job offers",
        "One offers higher pay, one has better culture, one has growth potential",
        "I value work-life balance but also career advancement",
        "Help me think through the pros and cons systematically"
    ]
    
    for message in decision_process:
        print(f"User: {message}")
        response = alison.generate_response(message)
        print(f"Alison: {response}")
        print()


def example_5_learning_adaptation():
    """Example 5: Show how Alison adapts over time"""
    print("=== Example 5: Learning and Adaptation ===")
    
    alison = Alison("learning_memory.json")
    
    print("Initial user profile:")
    print(f"Communication style: {alison.user_profile.communication_style}")
    print()
    
    # Simulate multiple interactions to show learning
    formal_messages = [
        "Good morning, Alison. I would appreciate your assistance with a technical matter.",
        "Could you please provide guidance on the most appropriate methodology?",
        "I require clarification regarding the implementation details, if you would be so kind."
    ]
    
    print("After formal interactions:")
    for msg in formal_messages:
        alison.generate_response(msg)
    
    print(f"Updated communication style: {alison.user_profile.communication_style}")
    print()
    
    # Now try casual messages
    casual_messages = [
        "hey alison, what's up?",
        "can u help me real quick?",
        "this is pretty cool stuff!"
    ]
    
    print("After casual interactions:")
    for msg in casual_messages:
        alison.generate_response(msg)
    
    print(f"Final communication style: {alison.user_profile.communication_style}")
    print()
    
    # Show conversation insights
    print("Conversation insights:")
    insights = alison.get_conversation_insights()
    for key, value in insights.items():
        print(f"  {key}: {value}")


def example_6_integration_template():
    """Example 6: Template for integrating into your own app"""
    print("=== Example 6: Integration Template ===")
    
    class MyApp:
        def __init__(self):
            self.alison = Alison("myapp_memory.json")
        
        def handle_user_message(self, message):
            """Handle user message with emotional intelligence"""
            # Get Alison's response
            response = self.alison.generate_response(message)
            
            # Get emotional context for app logic
            emotion, _ = self.alison.detect_emotional_state(message)
            intent, _ = self.alison.detect_intent(message)
            
            # Customize app behavior based on emotional state
            if emotion == EmotionalState.FRUSTRATED:
                # Maybe offer additional help options
                response += "\n\nWould you like me to connect you with additional resources?"
            elif emotion == EmotionalState.EXCITED:
                # Maybe suggest related features
                response += "\n\nSince you're excited about this, you might also enjoy exploring..."
            
            return response, emotion, intent
        
        def get_user_insights(self):
            """Get insights about user interaction patterns"""
            return self.alison.get_conversation_insights()
    
    # Demo the template
    app = MyApp()
    
    test_message = "I'm having trouble with this feature and it's really annoying!"
    response, emotion, intent = app.handle_user_message(test_message)
    
    print(f"User: {test_message}")
    print(f"App Response: {response}")
    print(f"Detected Emotion: {emotion.value}")
    print(f"Detected Intent: {intent.value}")


def main():
    """Run all examples"""
    examples = [
        example_1_simple_integration,
        example_2_emotional_coaching,
        example_3_creative_collaboration,
        example_4_decision_support,
        example_5_learning_adaptation,
        example_6_integration_template
    ]
    
    for i, example in enumerate(examples, 1):
        example()
        if i < len(examples):
            print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()