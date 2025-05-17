"""
DFA Visualizer Module
Handles the visualization of DFA states and token flow
"""

import tkinter as tk
from tkinter import ttk
import math
import time
from typing import List, Tuple, Optional
from lexer.core import Token, TokenType

class DFAVisualizer:
    """Visualizes DFA states and token flow with animation"""
    
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.states = {}  # state_id -> (x, y, radius)
        self.transitions = []  # (from_state, to_state, label)
        self.current_state = None
        self.animation_queue = []
        self.animation_speed = 0.3  # Faster animation speed
        self.node_radius = 35
        self.padding = 60
        
        # Token type mapping to state names
        self.token_type_to_state = {
            'INTEGER': 'NUMBER',
            'FLOAT': 'NUMBER',
            'NUMBER': 'NUMBER',
            'ID': 'IDENTIFIER',
            'IDENTIFIER': 'IDENTIFIER',
            'STRING': 'STRING',
            'OPERATOR': 'OPERATOR',
            'DELIMITER': 'DELIMITER',
            'COMMENT': 'COMMENT',
            'ERROR': 'ERROR'
        }
        
        self.colors = {
            'background': '#2D2D2D',
            'node': {
                'START': '#4CAF50',      # Green
                'IDENTIFIER': '#81C784',  # Light green
                'NUMBER': '#2196F3',      # Blue
                'STRING': '#FF9800',      # Orange
                'OPERATOR': '#9C27B0',    # Purple
                'DELIMITER': '#E91E63',   # Pink
                'COMMENT': '#9E9E9E',     # Gray
                'ERROR': '#F44336'        # Red
            },
            'node_active': '#FFD700',
            'edge': '#E0E0E0',
            'edge_active': '#FFD700',
            'text': '#FFFFFF',
            'text_active': '#2D2D2D'
        }
        
        # Reduce animation frames for better performance
        self.animation_frames = 10
        self.glow_radius = 45
        
        # Cache for gradients to avoid recalculation
        self._gradient_cache = {}
        
    def setup_canvas(self):
        """Initialize the canvas with a clean, subtle background (no grid)"""
        self.canvas.configure(bg=self.colors['background'])
        self.canvas.delete('grid')
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 300
        # Optionally, draw a very subtle grid (commented out for extra clean look)
        # grid_color = '#23272A'
        # for i in range(0, w, 40):
        #     self.canvas.create_line(i, 0, i, h, fill=grid_color, tags='grid')
        # for j in range(0, h, 40):
        #     self.canvas.create_line(0, j, w, j, fill=grid_color, tags='grid')
        # self.canvas.lower('grid')
        self.canvas.configure(width=w, height=h)
        
    def add_state(self, state_id: str, is_final: bool = False):
        """Add a state to the visualization"""
        # Calculate position based on number of existing states
        state_count = len(self.states)
        total_width = (state_count + 1) * (self.node_radius * 3)
        
        # Adjust canvas width if needed
        if total_width > self.canvas.winfo_width():
            new_width = max(800, total_width + self.padding * 2)
            self.canvas.configure(width=new_width)
        
        # Calculate x position with proper spacing
        x = self.padding + state_count * (self.node_radius * 3)
        y = self.canvas.winfo_height() // 2
        
        # Store state information
        self.states[state_id] = (x, y, self.node_radius, is_final)
        self._draw_state(state_id)
        
    def add_transition(self, from_state: str, to_state: str, label: str):
        """Add a transition between states"""
        self.transitions.append((from_state, to_state, label))
        self._draw_transition(from_state, to_state, label)
        
    def _create_gradient(self, color1, color2, steps):
        """Create a color gradient between two colors with caching"""
        cache_key = f"{color1}-{color2}-{steps}"
        if cache_key in self._gradient_cache:
            return self._gradient_cache[cache_key]
            
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        gradient = []
        for i in range(steps):
            factor = i / (steps - 1)
            r = int(r1 + (r2 - r1) * factor)
            g = int(g1 + (g2 - g1) * factor)
            b = int(b1 + (b2 - b1) * factor)
            gradient.append(f'#{r:02x}{g:02x}{b:02x}')
            
        self._gradient_cache[cache_key] = gradient
        return gradient
        
    def _draw_state(self, state_id: str):
        """Draw a state on the canvas with a clean, minimal look"""
        x, y, radius, is_final = self.states[state_id]
        base_color = self.colors['node'][state_id]
        # Flat node (no shadow, no gradient)
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=base_color,
            outline=self.colors['edge'], width=2, tags='node')
        # Subtle highlight for active/final
        if self.current_state == state_id or is_final:
            ring_color = '#FFD700' if self.current_state == state_id else '#4FC3F7'
            self.canvas.create_oval(
                x - radius - 4, y - radius - 4,
                x + radius + 4, y + radius + 4,
                outline=ring_color, width=2, tags='highlight')
        # State label
        self.canvas.create_text(
            x, y,
            text=state_id,
            fill=self.colors['text'],
            font=('Segoe UI', 13, 'bold'),
            tags='label')
        # Final state decoration (thin ring)
        if is_final:
            self.canvas.create_oval(
                x - radius + 6, y - radius + 6,
                x + radius - 6, y + radius - 6,
                outline=self.colors['edge'], width=1, tags='final')
        
    def _draw_transition(self, from_state: str, to_state: str, label: str):
        """Draw a clean, precise, and visually appealing transition between states"""
        x1, y1, r1, _ = self.states[from_state]
        x2, y2, r2, _ = self.states[to_state]
        edge_color = '#B0BEC5'  # Subtle, modern edge color
        arrow_color = '#1976D2'  # Vibrant arrowhead
        shadow_color = '#23272A'
        arrow_width = 2.5
        arrow_shape = (16, 22, 8)
        if from_state != to_state:
            # Calculate angle and start/end at node edge
            angle = math.atan2(y2 - y1, x2 - x1)
            start_x = x1 + r1 * math.cos(angle)
            start_y = y1 + r1 * math.sin(angle)
            end_x = x2 - r2 * math.cos(angle)
            end_y = y2 - r2 * math.sin(angle)
            # Bezier control point for smooth curve
            ctrl_dist = 36
            ctrl_x = (start_x + end_x) / 2 + ctrl_dist * math.sin(angle)
            ctrl_y = (start_y + end_y) / 2 - ctrl_dist * math.cos(angle)
            points = [start_x, start_y, ctrl_x, ctrl_y, end_x, end_y]
            # Draw shadow for depth
            self.canvas.create_line(
                *[p + 1 if i % 2 else p for i, p in enumerate(points)],
                fill=shadow_color, width=arrow_width + 2, smooth=True, arrow=tk.LAST,
                arrowshape=arrow_shape, tags='edge_shadow')
            # Draw main arrow
            self.canvas.create_line(
                *points,
                fill=edge_color,
                width=arrow_width,
                smooth=True,
                arrow=tk.LAST,
                arrowshape=arrow_shape,
                tags='edge')
            # Draw arrowhead overlay for vibrancy
            self.canvas.create_line(
                *points,
                fill=arrow_color,
                width=1.2,
                smooth=True,
                arrow=tk.LAST,
                arrowshape=(18, 26, 10),
                tags='arrowhead')
            # Label
            mid_x = (start_x + end_x) / 2 + 18 * math.sin(angle)
            mid_y = (start_y + end_y) / 2 - 18 * math.cos(angle) - 10
        else:
            # Self-loop
            angle = math.pi / 4
            start_x = x1 + r1 * math.cos(angle)
            start_y = y1 - r1 * math.sin(angle)
            end_x = x1 + r1 * math.cos(angle * 3)
            end_y = y1 - r1 * math.sin(angle * 3)
            ctrl_x = x1 + r1 * 1.7 * math.cos(angle)
            ctrl_y = y1 - r1 * 2.2
            self.canvas.create_line(
                start_x + 1, start_y + 1, ctrl_x + 1, ctrl_y + 1, end_x + 1, end_y + 1,
                fill=shadow_color, width=arrow_width + 2, smooth=True, arrow=tk.LAST,
                arrowshape=arrow_shape, tags='edge_shadow')
            self.canvas.create_line(
                start_x, start_y, ctrl_x, ctrl_y, end_x, end_y,
                fill=edge_color, width=arrow_width, smooth=True, arrow=tk.LAST,
                arrowshape=arrow_shape, tags='edge')
            self.canvas.create_line(
                start_x, start_y, ctrl_x, ctrl_y, end_x, end_y,
                fill=arrow_color, width=1.2, smooth=True, arrow=tk.LAST,
                arrowshape=(18, 26, 10), tags='arrowhead')
            mid_x = ctrl_x
            mid_y = ctrl_y - 10
        # Label background (very subtle)
        text = self.canvas.create_text(
            mid_x, mid_y,
            text=label,
            fill='#23272A',
            font=('Segoe UI', 9, 'bold'),
            tags='edge_label')
        bbox = self.canvas.bbox(text)
        if bbox:
            self.canvas.create_rectangle(
                bbox[0] - 3, bbox[1] - 1,
                bbox[2] + 3, bbox[3] + 1,
                fill='#F3F3F3', outline='', tags='edge_label_bg')
            self.canvas.tag_raise(text)
            
    def redraw(self):
        """Redraw the entire visualization"""
        # Clear the canvas
        self.canvas.delete("all")
        
        # Redraw all states
        for state_id in self.states:
            self._draw_state(state_id)
            
        # Redraw all transitions
        for from_state, to_state, label in self.transitions:
            self._draw_transition(from_state, to_state, label)
            
        # Highlight current state if any
        if self.current_state:
            self._highlight_state(self.current_state)
            
    def animate_token_flow(self, tokens: List[Token]):
        """Animate the flow of tokens through the DFA"""
        # Clear any existing animation
        self.animation_queue.clear()
        self.current_state = None
        
        # Reset states to their normal appearance
        self.redraw()
        
        # Start new animation
        self.animation_queue = tokens.copy()  # Make a copy to preserve original
        self._process_next_token()
        
    def _process_next_token(self):
        """Process the next token in the animation queue"""
        if not self.animation_queue:
            # Animation complete - reset to normal state
            self.current_state = None
            self.redraw()
            return
            
        token = self.animation_queue.pop(0)
        state_id = self.token_type_to_state.get(token.type.value, 'ERROR')
        self._highlight_state(state_id)
        self.canvas.after(int(self.animation_speed * 1000), self._process_next_token)
        
    def _highlight_state(self, state_id: str):
        """Highlight a state with optimized animation effects"""
        if self.current_state:
            self._draw_state(self.current_state)
            
        self.current_state = state_id
        x, y, radius, is_final = self.states[state_id]
        
        # Draw highlighted state
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=self.colors['node_active'],
            outline=self.colors['edge_active'],
            width=2
        )
        
        # Draw state label
        self.canvas.create_text(
            x, y,
            text=state_id,
            fill=self.colors['text_active'],
            font=('Segoe UI', 11, 'bold')
        )
        
        # Draw final state decoration if needed
        if is_final:
            self.canvas.create_oval(
                x - radius + 5, y - radius + 5,
                x + radius - 5, y + radius - 5,
                outline=self.colors['edge_active'],
                width=2
            )
        
    def reset(self):
        """Reset the visualization to its initial state"""
        # Clear the canvas and all data structures
        self.clear()
        
        # Reset canvas configuration
        self.setup_canvas()
        
        # Calculate initial layout
        self.layout_width = 0
        self.layout_height = 0
        
    def clear(self):
        """Clear the visualization"""
        self.canvas.delete("all")
        self.states.clear()
        self.transitions.clear()
        self.current_state = None
        self.animation_queue.clear()
        self._gradient_cache.clear()

    def animate_dfa_construction(self, states, transitions, on_complete=None, delay=350):
        """Animate DFA construction: add states and transitions step by step, then call on_complete."""
        self.clear()
        self._construction_states = list(states)
        self._construction_transitions = list(transitions)
        self._construction_on_complete = on_complete
        self._construction_delay = delay
        self._animate_next_state()

    def _animate_next_state(self):
        if self._construction_states:
            state = self._construction_states.pop(0)
            if isinstance(state, tuple):
                self.add_state(*state)
            else:
                self.add_state(state)
            self.canvas.after(self._construction_delay, self._animate_next_state)
        else:
            self._animate_next_transition()

    def _animate_next_transition(self):
        if self._construction_transitions:
            tr = self._construction_transitions.pop(0)
            self.add_transition(*tr)
            self.canvas.after(self._construction_delay, self._animate_next_transition)
        else:
            if self._construction_on_complete:
                self._construction_on_complete() 