"""
Automata visualization module for LexVi
Contains classes for visualizing DFA and token transitions
"""

import graphviz
from typing import Dict, Set, Tuple

class AutomataVisualizer:
    """Class for visualizing finite automata"""
    
    def __init__(self):
        self.dot = graphviz.Digraph(comment='Lexical Analyzer Automata')
        self.dot.attr(rankdir='LR')
        self.dot.attr('node', shape='circle')
        
    def add_state(self, state: str, is_final: bool = False):
        """Add a state to the automata visualization"""
        if is_final:
            self.dot.node(state, shape='doublecircle')
        else:
            self.dot.node(state)
            
    def add_transition(self, from_state: str, to_state: str, label: str):
        """Add a transition between states"""
        self.dot.edge(from_state, to_state, label=label)
        
    def render(self, filename: str = 'automata', view: bool = True):
        """Render the automata visualization"""
        self.dot.render(filename, view=view)
        
    def clear(self):
        """Clear the current visualization"""
        self.dot.clear()
        
class TokenStreamVisualizer:
    """Class for visualizing token stream and transitions"""
    
    def __init__(self):
        self.dot = graphviz.Digraph(comment='Token Stream')
        self.dot.attr(rankdir='LR')
        self.dot.attr('node', shape='box')
        
    def add_token(self, token_type: str, token_value: str, position: int):
        """Add a token to the visualization"""
        node_id = f'token_{position}'
        label = f'{token_type}\n{token_value}'
        self.dot.node(node_id, label)
        
        if position > 0:
            self.dot.edge(f'token_{position-1}', node_id)
            
    def render(self, filename: str = 'token_stream', view: bool = True):
        """Render the token stream visualization"""
        self.dot.render(filename, view=view)
        
    def clear(self):
        """Clear the current visualization"""
        self.dot.clear() 