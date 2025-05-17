"""
Main window GUI module for LexVi
Contains the main application window and UI components
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
from lexer.core import Lexer, Token, TokenType
from visualizer.dfa_visualizer import DFAVisualizer

class SyntaxHighlighter:
    """Custom syntax highlighter for the code editor"""
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.highlighting_rules = []
        
        # Define highlighting rules with different colors
        self.keyword_format = {"foreground": "#569CD6"}  # Blue
        self.string_format = {"foreground": "#CE9178"}   # Orange
        self.comment_format = {"foreground": "#6A9955"}  # Green
        self.number_format = {"foreground": "#B5CEA8"}   # Light Green
        self.identifier_format = {"foreground": "#9CDCFE"}  # Light Blue
        self.operator_format = {"foreground": "#D4D4D4"}   # White
        
        # Keywords
        keywords = ['if', 'else', 'while', 'for', 'return', 'break', 'continue',
                   'def', 'class', 'import', 'from', 'as', 'try', 'except',
                   'finally', 'raise', 'with', 'yield', 'async', 'await']
        
        for word in keywords:
            self.highlighting_rules.append((r'\b' + word + r'\b', self.keyword_format))
        
        # Other patterns
        self.highlighting_rules.append((r'"[^"]*"|\'[^\']*\'', self.string_format))
        self.highlighting_rules.append((r'#.*', self.comment_format))
        self.highlighting_rules.append((r'\b\d+\b', self.number_format))
        self.highlighting_rules.append((r'[a-zA-Z_][a-zA-Z0-9_]*', self.identifier_format))
        self.highlighting_rules.append((r'[+\-*/%=<>!&|^~]+', self.operator_format))

    def highlight(self):
        """Apply syntax highlighting to the text"""
        self.text_widget.tag_remove("highlight", "1.0", "end")
        
        for pattern, format in self.highlighting_rules:
            start = "1.0"
            while True:
                start = self.text_widget.search(pattern, start, "end", regexp=True)
                if not start:
                    break
                end = f"{start}+{len(self.text_widget.get(start, f'{start} lineend'))}c"
                self.text_widget.tag_add("highlight", start, end)
                for tag, value in format.items():
                    self.text_widget.tag_config("highlight", **{tag: value})
                start = end

class MainWindow:
    """Main application window"""
    
    def __init__(self, root):
        """Initialize the main window"""
        self.root = root
        self.lexer = Lexer()
        self.current_token_index = 0
        self.tokens = []
        self.status_var = tk.StringVar(value="Ready")
        self.theme_var = tk.BooleanVar(value=True)  # True for dark theme
        self.setup_styles()
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_line_numbers()

    def setup_styles(self):
        """Setup custom styles for widgets"""
        style = ttk.Style()
        
        # Modern dark theme
        style.configure('Dark.TFrame', background='#181A1B')
        style.configure('Dark.TLabel', background='#181A1B', foreground='#F3F3F3', font=('Segoe UI', 11))
        style.configure('Dark.TButton', 
                       background='#23272A',
                       foreground='#4FC3F7',  # Blue accent
                       borderwidth=0,
                       padding=(14, 8),
                       font=('Segoe UI Semibold', 11))
        style.map('Dark.TButton',
                 background=[('active', '#263238'), ('pressed', '#263238')],
                 foreground=[('active', '#80DEEA')])
        style.configure('Dark.TCheckbutton',
                       background='#181A1B',
                       foreground='#4FC3F7',
                       font=('Segoe UI', 11))
        style.configure('Dark.Treeview',
                       background='#23272A',
                       foreground='#F3F3F3',
                       fieldbackground='#23272A',
                       rowheight=28,
                       font=('Segoe UI', 10))
        style.configure('Dark.Treeview.Heading',
                       background='#263238',
                       foreground='#4FC3F7',
                       font=('Segoe UI Semibold', 11),
                       padding=7)
        style.configure('Dark.TLabelframe',
                       background='#181A1B',
                       foreground='#4FC3F7',
                       padding=14,
                       borderwidth=0)
        style.configure('Dark.TLabelframe.Label',
                       background='#181A1B',
                       foreground='#4FC3F7',
                       font=('Segoe UI Semibold', 12))
        style.configure('Dark.TNotebook',
                       background='#181A1B',
                       tabmargins=[2, 8, 2, 0],
                       borderwidth=0)
        style.configure('Dark.TNotebook.Tab',
                       background='#23272A',
                       foreground='#F3F3F3',
                       padding=[16, 8],
                       font=('Segoe UI', 11),
                       borderwidth=0)
        style.map('Dark.TNotebook.Tab',
                 background=[('selected', '#263238')],
                 foreground=[('selected', '#4FC3F7')])
        style.configure('Dark.TSeparator', background='#23272A')
        
        # Scale styles
        style.configure('Dark.Horizontal.TScale',
                       background='#23272A',
                       troughcolor='#1E1E1E',
                       sliderthickness=20,
                       sliderlength=20)
        style.configure('Light.Horizontal.TScale',
                       background='#FFFFFF',
                       troughcolor='#E3F2FD',
                       sliderthickness=20,
                       sliderlength=20)
        
        # Toolbar button style
        style.configure('Toolbar.TButton',
                       background='#23272A',
                       foreground='#F3F3F3',
                       borderwidth=0,
                       padding=(8, 4),
                       font=('Segoe UI', 10))
        style.map('Toolbar.TButton',
                 background=[('active', '#263238'), ('pressed', '#263238')],
                 foreground=[('active', '#4FC3F7')])
        
        # Menu styles
        style.configure('Dark.TMenubutton',
                       background='#23272A',
                       foreground='#F3F3F3',
                       borderwidth=0,
                       padding=(8, 4),
                       font=('Segoe UI', 10))
        style.map('Dark.TMenubutton',
                 background=[('active', '#263238')],
                 foreground=[('active', '#4FC3F7')])
        
        # Dialog styles
        style.configure('Dialog.TFrame',
                       background='#23272A',
                       padding=10)
        style.configure('Dialog.TLabel',
                       background='#23272A',
                       foreground='#F3F3F3',
                       font=('Segoe UI', 10))
        style.configure('Dialog.TButton',
                       background='#4FC3F7',
                       foreground='#FFFFFF',
                       borderwidth=0,
                       padding=(10, 5),
                       font=('Segoe UI', 10))
        style.map('Dialog.TButton',
                 background=[('active', '#45a049'), ('pressed', '#45a049')])
        
        # Modern light theme
        style.configure('Light.TFrame', background='#F7F9FA')
        style.configure('Light.TLabel', background='#F7F9FA', foreground='#23272A', font=('Segoe UI', 11))
        style.configure('Light.TButton',
                       background='#FFFFFF',
                       foreground='#1976D2',
                       borderwidth=0,
                       padding=(14, 8),
                       font=('Segoe UI Semibold', 11))
        style.map('Light.TButton',
                 background=[('active', '#E3F2FD'), ('pressed', '#E3F2FD')],
                 foreground=[('active', '#1565C0')])
        style.configure('Light.TCheckbutton',
                       background='#F7F9FA',
                       foreground='#1976D2',
                       font=('Segoe UI', 11))
        style.configure('Light.Treeview',
                       background='#FFFFFF',
                       foreground='#23272A',
                       fieldbackground='#FFFFFF',
                       rowheight=28,
                       font=('Segoe UI', 10))
        style.configure('Light.Treeview.Heading',
                       background='#E3F2FD',
                       foreground='#1976D2',
                       font=('Segoe UI Semibold', 11),
                       padding=7)
        style.configure('Light.TLabelframe',
                       background='#F7F9FA',
                       foreground='#1976D2',
                       padding=14,
                       borderwidth=0)
        style.configure('Light.TLabelframe.Label',
                       background='#F7F9FA',
                       foreground='#1976D2',
                       font=('Segoe UI Semibold', 12))
        style.configure('Light.TNotebook',
                       background='#F7F9FA',
                       tabmargins=[2, 8, 2, 0],
                       borderwidth=0)
        style.configure('Light.TNotebook.Tab',
                       background='#FFFFFF',
                       foreground='#23272A',
                       padding=[16, 8],
                       font=('Segoe UI', 11),
                       borderwidth=0)
        style.map('Light.TNotebook.Tab',
                 background=[('selected', '#E3F2FD')],
                 foreground=[('selected', '#1976D2')])
        style.configure('Light.TSeparator', background='#E3F2FD')

        # Add style for Accent.TFrame for a visible background (debug: use red)
        style.configure('Accent.TFrame', background='#8B0000', borderwidth=2, relief='solid')

    def setup_ui(self):
        """Setup the main window UI components"""
        # Set window minimum size
        self.root.minsize(1200, 800)
        self.root.title("LexVi - Interactive Lexical Analyzer")
        
        # --- Title/Logo Bar ---
        title_bar = ttk.Frame(self.root, style='Dark.TFrame')
        title_bar.pack(fill="x", padx=0, pady=(0, 8))
        # If you have a logo image, you can add it here with a Label
        title_label = ttk.Label(title_bar, text="🧩 LexVi", style='Dark.TLabel', font=('Segoe UI Semibold', 18))
        title_label.pack(side="left", padx=(18, 8), pady=8)
        subtitle_label = ttk.Label(title_bar, text="Interactive Lexical Analyzer", style='Dark.TLabel', font=('Segoe UI', 13))
        subtitle_label.pack(side="left", padx=0, pady=8)
        # Separator below title
        ttk.Separator(self.root, orient='horizontal', style='Dark.TSeparator').pack(fill='x', padx=0, pady=(0, 10))

        # Control Panel (must be packed before main_paned)
        control_frame = ttk.Frame(self.root, style='Accent.TFrame', height=70, borderwidth=2, relief='solid')
        control_frame.pack(side='top', fill='x', padx=20, pady=(0, 20))
        control_frame.pack_propagate(False)
        control_frame.configure(style='Accent.TFrame')
        
        # Run, Execute, and Export Buttons (Prominently displayed)
        run_button = ttk.Button(
            control_frame,
            text="Run",
            command=self.run_lexer,
            style='Accent.TButton',
            width=14
        )
        run_button.pack(side='left', padx=(0, 16), pady=12)
        
        execute_button = ttk.Button(
            control_frame,
            text="Execute",
            command=self.execute_code,
            style='Accent.TButton',
            width=14
        )
        execute_button.pack(side='left', padx=(0, 16), pady=12)
        
        export_button = ttk.Button(
            control_frame,
            text="Export",
            command=self.export_csv,
            style='Accent.TButton',
            width=14
        )
        export_button.pack(side='left', padx=(0, 16), pady=12)
        
        # Other Controls
        controls = ttk.Frame(control_frame)
        controls.pack(side='left', fill='x', expand=True)
        
        # Step Controls
        step_frame = ttk.Frame(controls)
        step_frame.pack(side='left', padx=(0, 20))
        
        ttk.Button(
            step_frame,
            text="Step",
            command=self.step_through,
            style='Accent.TButton',
            width=10
        ).pack(side='left', padx=(0, 8), pady=12)
        
        ttk.Button(
            step_frame,
            text="Reset",
            command=self.reset_visualization,
            style='Accent.TButton',
            width=10
        ).pack(side='left', pady=12)
        
        # Speed Control
        speed_frame = ttk.Frame(controls)
        speed_frame.pack(side='left')
        
        ttk.Label(
            speed_frame,
            text="Speed:",
            style='Card.TLabel'
        ).pack(side='left', padx=(0, 5), pady=12)
        
        self.speed_scale = ttk.Scale(
            speed_frame,
            from_=1,
            to=10,
            orient='horizontal',
            command=self.update_speed,
            style='Dark.Horizontal.TScale'
        )
        self.speed_scale.set(5)
        self.speed_scale.pack(side='left', fill='x', expand=True, pady=12)

        # Create main paned window (pack after control panel)
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL, style='Dark.TFrame')
        main_paned.pack(fill="both", expand=True, padx=15, pady=0)

        # Left pane - Code input and output
        left_frame = ttk.Frame(main_paned, style='Dark.TFrame')
        main_paned.add(left_frame, weight=1)

        # Create a paned window for the left side
        left_paned = ttk.PanedWindow(left_frame, orient=tk.VERTICAL, style='Dark.TFrame')
        left_paned.pack(fill="both", expand=True, padx=5, pady=5)

        # Code input area with label
        code_frame = ttk.LabelFrame(left_paned, text="Code Editor", style='Dark.TLabelframe')
        left_paned.add(code_frame, weight=2)
        
        self.code_editor = tk.Text(code_frame, bg='#1E1E1E', fg='#E0E0E0', 
                                 insertbackground='#4CAF50', font=('Consolas', 12),
                                 padx=15, pady=15, relief='flat', wrap=tk.WORD)
        self.code_editor.pack(fill="both", expand=True, padx=5, pady=5)
        self.highlighter = SyntaxHighlighter(self.code_editor)
        self.code_editor.bind("<KeyRelease>", self.on_code_change)

        # Code output area with label
        output_frame = ttk.LabelFrame(left_paned, text="Output", style='Dark.TLabelframe')
        left_paned.add(output_frame, weight=1)
        
        # Create a notebook for different output types
        self.output_notebook = ttk.Notebook(output_frame)
        self.output_notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Token analysis output tab
        token_output_frame = ttk.Frame(self.output_notebook, style='Dark.TFrame')
        self.output_notebook.add(token_output_frame, text="Token Analysis")
        
        self.token_output = tk.Text(token_output_frame, bg='#1E1E1E', fg='#E0E0E0',
                                  font=('Consolas', 12), padx=15, pady=15,
                                  relief='flat', state='disabled', wrap=tk.WORD)
        self.token_output.pack(fill="both", expand=True)
        
        # Code execution output tab
        exec_output_frame = ttk.Frame(self.output_notebook, style='Dark.TFrame')
        self.output_notebook.add(exec_output_frame, text="Code Execution")
        
        self.exec_output = tk.Text(exec_output_frame, bg='#1E1E1E', fg='#E0E0E0',
                                 font=('Consolas', 12), padx=15, pady=15,
                                 relief='flat', state='disabled', wrap=tk.WORD)
        self.exec_output.pack(fill="both", expand=True)

        # Right pane - Token table and DFA visualization
        right_frame = ttk.Frame(main_paned, style='Dark.TFrame')
        main_paned.add(right_frame, weight=1)

        # Create a paned window for the right side
        right_paned = ttk.PanedWindow(right_frame, orient=tk.VERTICAL, style='Dark.TFrame')
        right_paned.pack(fill="both", expand=True, padx=5, pady=5)

        # Token table
        token_frame = ttk.LabelFrame(right_paned, text="Tokens", style='Dark.TLabelframe')
        right_paned.add(token_frame, weight=1)

        # Create Treeview for tokens with custom style
        self.token_tree = ttk.Treeview(token_frame, columns=("Type", "Value", "Line", "Column"),
                                     show="headings", selectmode="browse", style='Dark.Treeview')
        
        # Configure column widths and headings
        self.token_tree.column("Type", width=100, anchor=tk.CENTER)
        self.token_tree.column("Value", width=150, anchor=tk.W)
        self.token_tree.column("Line", width=50, anchor=tk.CENTER)
        self.token_tree.column("Column", width=70, anchor=tk.CENTER)
        
        self.token_tree.heading("Type", text="Type")
        self.token_tree.heading("Value", text="Value")
        self.token_tree.heading("Line", text="Line")
        self.token_tree.heading("Column", text="Column")
        
        # Add scrollbar with custom style
        token_scroll = ttk.Scrollbar(token_frame, orient="vertical", 
                                   command=self.token_tree.yview)
        self.token_tree.configure(yscrollcommand=token_scroll.set)
        
        self.token_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        token_scroll.pack(side="right", fill="y", pady=5)

        # DFA Visualization
        dfa_frame = ttk.LabelFrame(right_paned, text="DFA Visualization", style='Dark.TLabelframe')
        right_paned.add(dfa_frame, weight=1)

        # Create canvas for DFA visualization
        self.dfa_canvas = tk.Canvas(dfa_frame, bg='#2D2D2D', highlightthickness=0)
        self.dfa_canvas.pack(fill="both", expand=True, padx=5, pady=5)

        # Initialize DFA visualizer with the canvas
        self.dfa_visualizer = DFAVisualizer(self.dfa_canvas)
        self.dfa_visualizer.setup_canvas()

        # Add status bar
        status_frame = ttk.Frame(self.root, style='Dark.TFrame')
        status_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            style='Dark.TLabel',
            font=('Segoe UI', 10)
        )
        status_label.pack(side='left')

    def setup_menu(self):
        """Setup the application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=lambda: self.code_editor.edit_undo(), accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=lambda: self.code_editor.edit_redo(), accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.code_editor.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=lambda: self.code_editor.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=lambda: self.code_editor.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.show_find_dialog, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace", command=self.show_replace_dialog, accelerator="Ctrl+H")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Dark Theme", variable=self.theme_var, command=self.toggle_theme)
        view_menu.add_checkbutton(label="Line Numbers", variable=tk.BooleanVar(value=True), command=self.toggle_line_numbers)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)

    def setup_toolbar(self):
        """Setup the toolbar with common actions"""
        toolbar = ttk.Frame(self.root, style='Dark.TFrame')
        toolbar.pack(fill='x', padx=0, pady=(0, 5))
        
        # Create buttons with icons (using emoji as placeholders)
        ttk.Button(toolbar, text="📄 New", command=self.new_file, style='Toolbar.TButton').pack(side='left', padx=2)
        ttk.Button(toolbar, text="📂 Open", command=self.open_file, style='Toolbar.TButton').pack(side='left', padx=2)
        ttk.Button(toolbar, text="💾 Save", command=self.save_file, style='Toolbar.TButton').pack(side='left', padx=2)
        ttk.Separator(toolbar, orient='vertical').pack(side='left', padx=5, fill='y')
        ttk.Button(toolbar, text="▶️ Run", command=self.run_lexer, style='Toolbar.TButton').pack(side='left', padx=2)
        ttk.Button(toolbar, text="⚡ Execute", command=self.execute_code, style='Toolbar.TButton').pack(side='left', padx=2)
        ttk.Button(toolbar, text="📤 Export", command=self.export_csv, style='Toolbar.TButton').pack(side='left', padx=2)
        ttk.Button(toolbar, text="⏯️ Step", command=self.step_through, style='Toolbar.TButton').pack(side='left', padx=2)
        ttk.Button(toolbar, text="🔄 Reset", command=self.reset_visualization, style='Toolbar.TButton').pack(side='left', padx=2)
        ttk.Separator(toolbar, orient='vertical').pack(side='left', padx=5, fill='y')
        ttk.Button(toolbar, text="🌙 Theme", command=self.toggle_theme, style='Toolbar.TButton').pack(side='left', padx=2)

    def setup_line_numbers(self):
        """Setup line numbers for the code editor"""
        self.line_numbers = tk.Text(self.code_editor.master, width=4, padx=3, takefocus=0,
                                  border=0, background='#1E1E1E', foreground='#858585',
                                  state='disabled', font=('Consolas', 12))
        self.line_numbers.pack(side='left', fill='y')
        
        def update_line_numbers(*args):
            self.line_numbers.config(state='normal')
            self.line_numbers.delete('1.0', 'end')
            i = self.code_editor.get('1.0', 'end-1c').count('\n') + 1
            line_numbers_string = '\n'.join(str(x) for x in range(1, i + 1))
            self.line_numbers.insert('1.0', line_numbers_string)
            self.line_numbers.config(state='disabled')
        
        self.code_editor.bind('<Key>', update_line_numbers)
        self.code_editor.bind('<MouseWheel>', update_line_numbers)
        update_line_numbers()

    def show_find_dialog(self):
        """Show the find dialog"""
        find_dialog = tk.Toplevel(self.root)
        find_dialog.title("Find")
        find_dialog.geometry("300x100")
        find_dialog.transient(self.root)
        
        ttk.Label(find_dialog, text="Find:").pack(pady=5)
        find_entry = ttk.Entry(find_dialog, width=30)
        find_entry.pack(pady=5)
        find_entry.focus_set()
        
        def find():
            text = find_entry.get()
            if text:
                self.code_editor.tag_remove('search', '1.0', 'end')
                start = '1.0'
                while True:
                    start = self.code_editor.search(text, start, 'end')
                    if not start:
                        break
                    end = f"{start}+{len(text)}c"
                    self.code_editor.tag_add('search', start, end)
                    start = end
                self.code_editor.tag_config('search', background='#4CAF50', foreground='white')
        
        ttk.Button(find_dialog, text="Find", command=find).pack(pady=5)

    def show_replace_dialog(self):
        """Show the replace dialog"""
        replace_dialog = tk.Toplevel(self.root)
        replace_dialog.title("Replace")
        replace_dialog.geometry("300x150")
        replace_dialog.transient(self.root)
        
        ttk.Label(replace_dialog, text="Find:").pack(pady=5)
        find_entry = ttk.Entry(replace_dialog, width=30)
        find_entry.pack(pady=5)
        
        ttk.Label(replace_dialog, text="Replace with:").pack(pady=5)
        replace_entry = ttk.Entry(replace_dialog, width=30)
        replace_entry.pack(pady=5)
        
        def replace():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            if find_text:
                content = self.code_editor.get('1.0', 'end-1c')
                new_content = content.replace(find_text, replace_text)
                self.code_editor.delete('1.0', 'end')
                self.code_editor.insert('1.0', new_content)
        
        ttk.Button(replace_dialog, text="Replace", command=replace).pack(pady=5)

    def show_about(self):
        """Show the about dialog"""
        messagebox.showinfo("About LexVi",
                          "LexVi - Interactive Lexical Analyzer\n\n"
                          "Version 1.0\n"
                          "A modern tool for lexical analysis and visualization.")

    def show_documentation(self):
        """Show the documentation"""
        # Open documentation in a new window
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Documentation")
        doc_window.geometry("800x600")
        
        text = tk.Text(doc_window, wrap=tk.WORD, padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True)
        
        # Add documentation content
        doc_content = """
        LexVi Documentation
        
        1. Getting Started
        - Open or create a new file
        - Write your code in the editor
        - Click Run to analyze the code
        
        2. Features
        - Syntax highlighting
        - Token analysis
        - DFA visualization
        - Code execution
        - Dark/Light theme
        
        3. Controls
        - Run: Execute the code
        - Step: Step through tokens
        - Reset: Reset visualization
        - Speed: Adjust animation speed
        
        4. Keyboard Shortcuts
        - Ctrl+N: New file
        - Ctrl+O: Open file
        - Ctrl+S: Save file
        - Ctrl+F: Find
        - Ctrl+H: Replace
        """
        text.insert('1.0', doc_content)
        text.config(state='disabled')

    def new_file(self):
        """Create a new file"""
        self.code_editor.delete('1.0', 'end')
        self.root.title("LexVi - New File")

    def open_file(self):
        """Open a file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.code_editor.delete('1.0', 'end')
                    self.code_editor.insert('1.0', file.read())
                self.root.title(f"LexVi - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")

    def save_file(self):
        """Save the current file"""
        if not hasattr(self, 'current_file') or not self.current_file:
            return self.save_file_as()
            
        try:
            with open(self.current_file, 'w') as file:
                file.write(self.code_editor.get('1.0', 'end-1c'))
            self.status_var.set(f"File saved: {self.current_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")

    def save_file_as(self):
        """Save the current file with a new name"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.code_editor.get('1.0', 'end-1c'))
                self.current_file = file_path
                self.root.title(f"LexVi - {file_path}")
                self.status_var.set(f"File saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")

    def toggle_line_numbers(self):
        """Toggle line numbers visibility"""
        if self.line_numbers.winfo_viewable():
            self.line_numbers.pack_forget()
        else:
            self.line_numbers.pack(side='left', fill='y')

    def run_lexer(self):
        """Run the lexer on the current code"""
        self.status_var.set("Running lexical analysis...")
        self.root.update()
        # Reset DFA visualization
        self.dfa_visualizer.reset()
        # Get current code and run lexer
        code = self.code_editor.get("1.0", "end-1c")
        self.tokens = self.lexer.tokenize(code)
        self.current_token_index = 0
        # Setup and display DFA visualization (animation will handle tokens)
        self._setup_dfa_visualization()
        # Update output text (not animated)
        # self.update_output()  # Commented out to avoid showing all tokens at once
        self.status_var.set("Analysis complete!")

    def _setup_dfa_visualization(self):
        """Setup the DFA visualization with states and transitions, animated step by step"""
        # Define states and transitions
        states = [
            ("START", False),
            ("IDENTIFIER", True),
            ("NUMBER", True),
            ("STRING", True),
            ("OPERATOR", True),
            ("DELIMITER", True),
            ("COMMENT", True),
            ("ERROR", False)
        ]
        transitions = [
            ("START", "IDENTIFIER", "letter"),
            ("IDENTIFIER", "IDENTIFIER", "letter/digit"),
            ("START", "NUMBER", "digit"),
            ("NUMBER", "NUMBER", "digit"),
            ("START", "STRING", '"'),
            ("STRING", "STRING", "any"),
            ("STRING", "STRING", '"'),
            ("START", "OPERATOR", "operator"),
            ("START", "DELIMITER", "delimiter"),
            ("START", "COMMENT", "#"),
            ("COMMENT", "COMMENT", "any"),
            ("START", "ERROR", "invalid"),
            ("ERROR", "ERROR", "any")
        ]
        # Animate DFA construction, then animate tokens one by one
        def after_dfa():
            self.update_token_table()
            self.display_errors()
            if self.tokens:
                self.animate_tokens_one_by_one()
        self.dfa_visualizer.animate_dfa_construction(states, transitions, on_complete=after_dfa)

    def step_through(self):
        """Step through the lexer one token at a time"""
        if not hasattr(self, 'tokens') or not self.tokens:
            self.run_lexer()
            return
            
        if self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            self.highlight_token(token)
            self.dfa_visualizer.animate_token_flow([token])
            self.current_token_index += 1
            self.status_var.set(f"Processing token: {token.value}")
        else:
            self.status_var.set("End of tokens reached")

    def reset_visualization(self):
        """Reset the DFA visualization and token analysis"""
        self.dfa_visualizer.reset()
        self.token_tree.delete(*self.token_tree.get_children())
        self.tokens = []
        self.current_token_index = 0
        self.status_var.set("Visualization reset")
        
        # Clear outputs
        self.token_output.configure(state='normal')
        self.token_output.delete('1.0', 'end')
        self.token_output.configure(state='disabled')
        
        self.exec_output.configure(state='normal')
        self.exec_output.delete('1.0', 'end')
        self.exec_output.configure(state='disabled')

    def update_speed(self, value):
        """Update the animation speed"""
        try:
            speed = float(value)
            if hasattr(self, 'dfa_visualizer') and self.dfa_visualizer:
                self.dfa_visualizer.animation_speed = speed
                self.status_var.set(f"Animation speed: {speed}")
        except ValueError:
            pass

    def highlight_token(self, token):
        """Highlight the current token in the code editor"""
        self.code_editor.tag_remove("current_token", "1.0", "end")
        start = f"{token.line}.{token.column}"
        end = f"{token.line}.{token.column + len(token.value)}"
        self.code_editor.tag_add("current_token", start, end)
        self.code_editor.tag_config("current_token", background="yellow")
        self.code_editor.see(start)

    def update_token_table(self):
        """Update the token table with current tokens"""
        self.token_tree.delete(*self.token_tree.get_children())
        for token in self.tokens:
            self.token_tree.insert("", "end", values=(
                token.type.value,
                token.value,
                token.line,
                token.column
            ))

    def display_errors(self):
        """Display any lexing errors"""
        errors = self.lexer.get_errors()
        if errors:
            error_text = "\n".join(f"Line {line}, Column {column}: {error}"
                                 for error, line, column in errors)
            messagebox.showerror("Lexing Errors", error_text)

    def export_csv(self):
        """Export tokens to CSV file"""
        file_name = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")])
        
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write("Type,Value,Line,Column\n")
                    for token in self.lexer.tokens:
                        f.write(f"{token.type},{token.value},{token.line},{token.column}\n")
                messagebox.showinfo("Success", "Tokens exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def update_output(self):
        """Update the token analysis output text"""
        self.token_output.configure(state='normal')
        self.token_output.delete("1.0", "end")
        
        # Add header
        self.token_output.insert("end", "Token Analysis Output:\n\n")
        
        # Add token information
        for token in self.tokens:
            self.token_output.insert("end", f"Token: {token.type.value}\n")
            self.token_output.insert("end", f"Value: {token.value}\n")
            self.token_output.insert("end", f"Position: Line {token.line}, Column {token.column}\n")
            self.token_output.insert("end", "-" * 40 + "\n")
            
        # Add error information if any
        errors = self.lexer.get_errors()
        if errors:
            self.token_output.insert("end", "\nErrors Found:\n")
            for error, line, column in errors:
                self.token_output.insert("end", f"Line {line}, Column {column}: {error}\n")
        
        self.token_output.configure(state='disabled')
        # Switch to the token analysis tab
        self.output_notebook.select(0)  # Index 0 is the Token Analysis tab

    def execute_code(self):
        """Execute the code and show the output"""
        code = self.code_editor.get("1.0", "end-1c")
        if not code.strip():
            return
            
        # Clear previous output
        self.exec_output.configure(state='normal')
        self.exec_output.delete("1.0", "end")
        
        try:
            # Create a new namespace for execution
            namespace = {}
            
            # Redirect stdout to capture print statements
            import sys
            from io import StringIO
            old_stdout = sys.stdout
            redirected_output = StringIO()
            sys.stdout = redirected_output
            
            # Execute the code
            exec(code, namespace)
            
            # Restore stdout
            sys.stdout = old_stdout
            
            # Get the output
            output = redirected_output.getvalue()
            
            # Display the output
            if output:
                self.exec_output.insert("end", "Output:\n")
                self.exec_output.insert("end", output)
            else:
                self.exec_output.insert("end", "Code executed successfully. No output.")
                
        except Exception as e:
            self.exec_output.insert("end", f"Error:\n{str(e)}")
            
        finally:
            self.exec_output.configure(state='disabled')
            # Switch to the execution output tab
            self.output_notebook.select(1)  # Index 1 is the Code Execution tab

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.theme_var.get():
            # Dark theme
            self.root.configure(bg='#1E1E1E')
            self.code_editor.configure(bg='#1E1E1E', fg='#E0E0E0', insertbackground='#4CAF50')
            self.token_output.configure(bg='#1E1E1E', fg='#E0E0E0')
            self.exec_output.configure(bg='#1E1E1E', fg='#E0E0E0')
            self.speed_scale.configure(style='Dark.Horizontal.TScale')
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Frame):
                    widget.configure(style='Dark.TFrame')
                elif isinstance(widget, ttk.Label):
                    widget.configure(style='Dark.TLabel')
                elif isinstance(widget, ttk.Button):
                    widget.configure(style='Dark.TButton')
                elif isinstance(widget, ttk.Checkbutton):
                    widget.configure(style='Dark.TCheckbutton')
                elif isinstance(widget, ttk.Treeview):
                    widget.configure(style='Dark.Treeview')
                elif isinstance(widget, ttk.LabelFrame):
                    widget.configure(style='Dark.TLabelframe')
                elif isinstance(widget, ttk.Notebook):
                    widget.configure(style='Dark.TNotebook')
        else:
            # Light theme
            self.root.configure(bg='#F5F5F5')
            self.code_editor.configure(bg='#FFFFFF', fg='#333333', insertbackground='#2196F3')
            self.token_output.configure(bg='#FFFFFF', fg='#333333')
            self.exec_output.configure(bg='#FFFFFF', fg='#333333')
            self.speed_scale.configure(style='Light.Horizontal.TScale')
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Frame):
                    widget.configure(style='Light.TFrame')
                elif isinstance(widget, ttk.Label):
                    widget.configure(style='Light.TLabel')
                elif isinstance(widget, ttk.Button):
                    widget.configure(style='Light.TButton')
                elif isinstance(widget, ttk.Checkbutton):
                    widget.configure(style='Light.TCheckbutton')
                elif isinstance(widget, ttk.Treeview):
                    widget.configure(style='Light.Treeview')
                elif isinstance(widget, ttk.LabelFrame):
                    widget.configure(style='Light.TLabelframe')
                elif isinstance(widget, ttk.Notebook):
                    widget.configure(style='Light.TNotebook')

    def on_code_change(self, event):
        """Handle code changes in the editor"""
        # Apply syntax highlighting
        self.highlighter.highlight()
        
        # Get current code
        code = self.code_editor.get("1.0", "end-1c")
        
        # If code is empty or only whitespace, reset the visualization
        if not code.strip():
            self.dfa_visualizer.reset()
            self.token_tree.delete(*self.token_tree.get_children())
            self.tokens = []
            self.current_token_index = 0
            self.status_var.set("Ready")

    def run_code(self):
        """Run the code and update all visualizations"""
        # Run the lexer
        self.run_lexer()
        
        # Execute the code
        self.execute_code()
        
        # Update status
        self.status_var.set("Code execution complete!")

    def animate_tokens_one_by_one(self):
        """Animate tokens one by one, showing each being tokenized in the output, and highlighting in the editor, table, and output."""
        self.current_token_index = 0
        self.output_notebook.select(0)
        self.token_output.configure(state='normal')
        self.token_output.delete('1.0', 'end')
        self.token_output.tag_remove('current_token', '1.0', 'end')
        def animate_next():
            if self.current_token_index < len(self.tokens):
                token = self.tokens[self.current_token_index]
                self.highlight_token(token)
                # Highlight in token table
                self.token_tree.selection_set(self.token_tree.get_children()[self.current_token_index])
                self.token_tree.see(self.token_tree.get_children()[self.current_token_index])
                # Append to token_output and highlight
                details = f"Token: {token.type.value}\nValue: {token.value}\nPosition: Line {token.line}, Column {token.column}\n" + ("-" * 40 + "\n")
                self.token_output.insert('end', details)
                self.token_output.tag_remove('current_token', '1.0', 'end')
                # Highlight just the newly added token
                start_idx = f'end-{len(details)}c'
                end_idx = 'end'
                self.token_output.tag_add('current_token', start_idx, end_idx)
                self.token_output.tag_config('current_token', background='#FFD700', foreground='#23272A')
                self.token_output.see('end')
                # Animate DFA state
                state_id = self.dfa_visualizer.token_type_to_state.get(token.type.value, 'ERROR')
                self.dfa_visualizer._highlight_state(state_id)
                self.current_token_index += 1
                delay = int(self.speed_scale.get() * 80)
                self.root.after(delay, animate_next)
            else:
                self.token_output.tag_remove('current_token', '1.0', 'end')
                self.token_output.configure(state='disabled')
                self.status_var.set("Token animation complete!")
        animate_next() 