#!/usr/bin/env python3
"""
Enhanced CLI interface for Alison - Emotionally Intelligent Co-pilot
Demonstrates the system with example interactions and provides an interactive mode
"""

import sys
import os
from alison import Alison


def demonstrate_alison():
    """Demonstrate Alison's capabilities with sample interactions"""
    print("🌟 Alison - Emotionally Intelligent Co-pilot Demonstration")
    print("=" * 60)
    print()
    
    # Create Alison instance
    alison = Alison("demo_memory.json")
    
    # Sample interactions demonstrating different emotional states and intents
    test_cases = [
        {
            "scenario": "Frustrated User",
            "input": "Alison, I'm really stuck on this project and it's driving me crazy!",
            "explanation": "Detects frustration and provides calm, supportive response"
        },
        {
            "scenario": "Excited Collaborator", 
            "input": "This is amazing! I have this brilliant idea for a new feature!",
            "explanation": "Matches enthusiasm and offers collaborative engagement"
        },
        {
            "scenario": "Confused Learner",
            "input": "I don't understand this concept. What does machine learning actually mean?",
            "explanation": "Recognizes confusion and adapts to provide patient clarification"
        },
        {
            "scenario": "Stressed Decision Maker",
            "input": "I have a deadline tomorrow and need to choose between three different approaches quickly!",
            "explanation": "Detects time pressure and offers structured decision support"
        },
        {
            "scenario": "Creative Brainstormer",
            "input": "Let's design something innovative! I want to create a unique user experience.",
            "explanation": "Identifies creative intent and becomes an inspiring partner"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🎭 Scenario {i}: {test_case['scenario']}")
        print(f"User: {test_case['input']}")
        
        response = alison.generate_response(test_case['input'])
        print(f"Alison: {response}")
        print(f"💡 Analysis: {test_case['explanation']}")
        print("-" * 60)
        print()
    
    # Show conversation insights
    print("📊 Conversation Analysis:")
    insights = alison.get_conversation_insights()
    
    print(f"• Total interactions: {insights['total_interactions']}")
    print(f"• Most common emotion detected: {insights['common_emotions']}")
    print(f"• Most common intent: {insights['common_intents']}")
    print(f"• Communication style adaptation:")
    
    for style, score in insights['communication_style'].items():
        print(f"  - {style.capitalize()}: {score:.2f}")
    
    print(f"• Conversation patterns:")
    for pattern, count in insights['conversation_patterns'].items():
        emotion, intent = pattern.split('_', 1)
        print(f"  - {emotion.replace('_', ' ').title()} + {intent.replace('_', ' ').title()}: {count}")
    
    print("\n" + "=" * 60)
    return alison


def interactive_mode(alison):
    """Run interactive conversation mode"""
    print("\n🗣️  Interactive Mode - Talk with Alison")
    print("Type your messages and see how Alison adapts to your emotional state")
    print("Commands: 'insights' to see analysis, 'demo' for examples, 'exit' to quit")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nAlison: It's been wonderful talking with you. Take care! 💫")
                print("Your conversation patterns have been saved for next time.")
                break
            
            if user_input.lower() == 'insights':
                print("\n📊 Current Conversation Insights:")
                insights = alison.get_conversation_insights()
                print(f"Total interactions: {insights['total_interactions']}")
                if insights['total_interactions'] > 0:
                    print(f"Your communication style: {insights['communication_style']}")
                    print(f"Conversation patterns: {insights['conversation_patterns']}")
                continue
            
            if user_input.lower() == 'demo':
                demonstrate_alison()
                continue
            
            if not user_input:
                continue
            
            response = alison.generate_response(user_input)
            
            # Show emotional analysis for educational purposes
            emotion, _ = alison.detect_emotional_state(user_input)
            intent, _ = alison.detect_intent(user_input)
            
            print(f"\nAlison: {response}")
            print(f"[Detected: {emotion.value} emotion, {intent.value} intent]")
            
        except KeyboardInterrupt:
            print("\n\nAlison: Until next time! 👋")
            break
        except Exception as e:
            print(f"\nAlison: I apologize, I encountered an error: {str(e)}")
            print("Let me try to help you in another way.")


def main():
    """Main application entry point"""
    print("🤖 Welcome to Alison - Your Emotionally Intelligent Co-pilot")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--demo-only':
        demonstrate_alison()
    elif len(sys.argv) > 1 and sys.argv[1] == '--interactive-only':
        alison = Alison()
        interactive_mode(alison)
    else:
        # Run demonstration first, then interactive mode
        alison = demonstrate_alison()
        
        # Ask if user wants to try interactive mode
        try:
            choice = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
            if choice in ['y', 'yes', '']:
                interactive_mode(alison)
        except KeyboardInterrupt:
            print("\nThanks for trying Alison! 👋")


if __name__ == "__main__":
    main()