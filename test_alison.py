#!/usr/bin/env python3
"""
Test suite for Alison emotionally intelligent co-pilot
"""

import unittest
import tempfile
import os
from alison import Alison, EmotionalState, UserIntent


class TestAlison(unittest.TestCase):
    """Test cases for Alison AI system"""
    
    def setUp(self):
        """Set up test environment"""
        # Use temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.alison = Alison(memory_file=self.temp_file.name)
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_emotion_detection_frustrated(self):
        """Test detection of frustrated emotional state"""
        text = "This is so frustrating! It won't work and I'm stuck."
        emotion, confidence = self.alison.detect_emotional_state(text)
        self.assertEqual(emotion, EmotionalState.FRUSTRATED)
        self.assertGreater(confidence, 0.5)
    
    def test_emotion_detection_excited(self):
        """Test detection of excited emotional state"""
        text = "This is amazing! I love this approach, it's perfect!"
        emotion, confidence = self.alison.detect_emotional_state(text)
        self.assertEqual(emotion, EmotionalState.EXCITED)
        self.assertGreater(confidence, 0.5)
    
    def test_emotion_detection_confused(self):
        """Test detection of confused emotional state"""
        text = "I don't understand this. What does this mean? It's unclear."
        emotion, confidence = self.alison.detect_emotional_state(text)
        self.assertEqual(emotion, EmotionalState.CONFUSED)
        self.assertGreater(confidence, 0.5)
    
    def test_intent_detection_help_request(self):
        """Test detection of help request intent"""
        text = "Alison, can you help me solve this problem?"
        intent, confidence = self.alison.detect_intent(text)
        self.assertEqual(intent, UserIntent.HELP_REQUEST)
        self.assertGreater(confidence, 0.5)
    
    def test_intent_detection_question(self):
        """Test detection of question intent"""
        text = "How do I approach this challenge? What would you recommend?"
        intent, confidence = self.alison.detect_intent(text)
        self.assertEqual(intent, UserIntent.QUESTION)
        self.assertGreater(confidence, 0.5)
    
    def test_intent_detection_creative(self):
        """Test detection of creative collaboration intent"""
        text = "Let's brainstorm some creative ideas for this design project."
        intent, confidence = self.alison.detect_intent(text)
        self.assertEqual(intent, UserIntent.CREATIVE_COLLABORATION)
        self.assertGreater(confidence, 0.5)
    
    def test_response_generation(self):
        """Test response generation with emotional intelligence"""
        user_input = "I'm really frustrated with this code. It's not working!"
        response = self.alison.generate_response(user_input)
        
        # Check that response acknowledges frustration
        self.assertIn("frustrating", response.lower())
        # Check that response offers help
        self.assertTrue(any(word in response.lower() for word in ["help", "support", "work through"]))
        # Ensure response is not empty
        self.assertGreater(len(response), 10)
    
    def test_tone_adaptation_frustrated(self):
        """Test tone adaptation for frustrated users"""
        tone = self.alison.adapt_response_tone(EmotionalState.FRUSTRATED, UserIntent.HELP_REQUEST)
        self.assertEqual(tone, "calm_supportive")
    
    def test_tone_adaptation_excited(self):
        """Test tone adaptation for excited users"""
        tone = self.alison.adapt_response_tone(EmotionalState.EXCITED, UserIntent.CREATIVE_COLLABORATION)
        self.assertEqual(tone, "enthusiastic_collaborative")
    
    def test_conversation_memory(self):
        """Test that conversation history is maintained"""
        initial_count = len(self.alison.conversation_history)
        
        self.alison.generate_response("Hello Alison!")
        self.assertEqual(len(self.alison.conversation_history), initial_count + 1)
        
        self.alison.generate_response("Can you help me with something?")
        self.assertEqual(len(self.alison.conversation_history), initial_count + 2)
    
    def test_user_profile_updates(self):
        """Test that user profile is updated based on interactions"""
        # Initial communication style
        initial_formal = self.alison.user_profile.communication_style["formal"]
        
        # Send a long, formal message
        long_formal_message = "Good afternoon, Alison. I would very much appreciate your assistance with a rather complex technical challenge that I have been encountering in my current project development efforts."
        self.alison.generate_response(long_formal_message)
        
        # Check that formal communication style increased
        updated_formal = self.alison.user_profile.communication_style["formal"]
        self.assertGreater(updated_formal, initial_formal)
    
    def test_conversation_insights(self):
        """Test conversation insights functionality"""
        # Generate some conversation history
        self.alison.generate_response("I'm excited about this project!")
        self.alison.generate_response("Can you help me brainstorm ideas?")
        
        insights = self.alison.get_conversation_insights()
        
        # Check insights structure
        self.assertIn("total_interactions", insights)
        self.assertIn("common_emotions", insights)
        self.assertIn("common_intents", insights)
        self.assertEqual(insights["total_interactions"], 2)
    
    def test_memory_persistence(self):
        """Test that memory is saved and can be loaded"""
        # Generate response to create memory
        self.alison.generate_response("Hello Alison!")
        
        # Create new instance with same memory file
        new_alison = Alison(memory_file=self.temp_file.name)
        
        # Check that user profile was loaded
        self.assertIsNotNone(new_alison.user_profile)
        self.assertIn("formal", new_alison.user_profile.communication_style)


class TestEmotionalIntelligence(unittest.TestCase):
    """Specific tests for emotional intelligence features"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.alison = Alison(memory_file=self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_empathetic_response_to_stress(self):
        """Test empathetic response to stressed user"""
        stressed_input = "I have a deadline tomorrow and I'm overwhelmed with work!"
        response = self.alison.generate_response(stressed_input)
        
        # Should acknowledge the pressure
        self.assertTrue(any(word in response.lower() for word in ["pressure", "understand", "stress"]))
        # Should offer structured help
        self.assertTrue(any(word in response.lower() for word in ["step", "help", "support"]))
    
    def test_adaptive_communication_style(self):
        """Test that Alison adapts to user's communication style over time"""
        # Send multiple casual messages
        casual_messages = [
            "hey alison, what's up?",
            "can u help me real quick?",
            "this is cool stuff!"
        ]
        
        for msg in casual_messages:
            self.alison.generate_response(msg)
        
        # Check that casual style has increased
        casual_score = self.alison.user_profile.communication_style["casual"]
        formal_score = self.alison.user_profile.communication_style["formal"]
        self.assertGreater(casual_score, formal_score)
    
    def test_contextual_understanding(self):
        """Test that Alison understands context and maintains conversation flow"""
        # First interaction
        response1 = self.alison.generate_response("I'm working on a creative project")
        
        # Second interaction should understand context
        response2 = self.alison.generate_response("What do you think about adding colors?")
        
        # Both responses should be contextually appropriate
        self.assertGreater(len(response1), 10)
        self.assertGreater(len(response2), 10)
        
        # Check conversation history
        self.assertEqual(len(self.alison.conversation_history), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)