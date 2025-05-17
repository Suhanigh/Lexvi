#!/usr/bin/env python3
"""
LexVi: An Interactive Lexical Analyzer Tool
Main application entry point
"""

import sys
import tkinter as tk
from tkinter import ttk
from gui.main_window import MainWindow

def main():
    """Main function to start the LexVi application"""
    # Create root window
    root = tk.Tk()
    root.title("LexVi - Interactive Lexical Analyzer")
    root.geometry("1200x800")
    
    # Set initial dark theme
    root.configure(bg='#1E1E1E')
    
    # Create and start the application
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 