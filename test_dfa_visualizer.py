"""
Test module for DFA Visualizer
"""

import unittest
import tkinter as tk
from visualizer.dfa_visualizer import DFAVisualizer
from lexer.core import Token, TokenType

class TestDFAVisualizer(unittest.TestCase):
    """Test cases for DFA Visualizer"""
    
    def setUp(self):
        """Set up test environment"""
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root)
        self.visualizer = DFAVisualizer(self.canvas)
        
    def tearDown(self):
        """Clean up test environment"""
        self.root.destroy()
        
    def test_add_state(self):
        """Test adding states to the visualization"""
        self.visualizer.add_state("START")
        self.visualizer.add_state("IDENTIFIER", True)
        
        self.assertIn("START", self.visualizer.states)
        self.assertIn("IDENTIFIER", self.visualizer.states)
        self.assertTrue(self.visualizer.states["IDENTIFIER"][3])  # is_final
        
    def test_add_transition(self):
        """Test adding transitions between states"""
        self.visualizer.add_state("START")
        self.visualizer.add_state("IDENTIFIER")
        self.visualizer.add_transition("START", "IDENTIFIER", "letter")
        
        self.assertEqual(len(self.visualizer.transitions), 1)
        self.assertEqual(self.visualizer.transitions[0], 
                        ("START", "IDENTIFIER", "letter"))
        
    def test_animate_token_flow(self):
        """Test token flow animation"""
        self.visualizer.add_state("START")
        self.visualizer.add_state("IDENTIFIER", True)
        self.visualizer.add_transition("START", "IDENTIFIER", "letter")
        
        token = Token(TokenType.IDENTIFIER, "test", 1, 1)
        self.visualizer.animate_token_flow([token])
        
        # Animation should be queued
        self.assertEqual(len(self.visualizer.animation_queue), 1)
        
    def test_clear(self):
        """Test clearing the visualization"""
        self.visualizer.add_state("START")
        self.visualizer.add_state("IDENTIFIER")
        self.visualizer.add_transition("START", "IDENTIFIER", "letter")
        
        self.visualizer.clear()
        
        self.assertEqual(len(self.visualizer.states), 0)
        self.assertEqual(len(self.visualizer.transitions), 0)
        self.assertIsNone(self.visualizer.current_state)
        self.assertEqual(len(self.visualizer.animation_queue), 0)

if __name__ == '__main__':
    unittest.main() 