# LexVi: An Interactive Lexical Analyzer Tool

LexVi is a Python-based desktop application that provides an interactive environment for lexical analysis of code. It features a modern GUI interface, real-time syntax highlighting, and visualization capabilities for understanding the tokenization process.

## Features

- Modern GUI interface built with PyQt5
- Real-time syntax highlighting
- Interactive tokenization with step-by-step execution
- Visualization of token stream and automata
- Export capabilities (CSV and PDF)
- Error detection and reporting
- Drag-and-drop file support

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/lexvi.git
cd lexvi
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python main.py
```

2. Enter or paste code into the input area
3. Use the control buttons to:
   - Run: Perform complete tokenization
   - Step-by-Step: Execute tokenization one step at a time
   - Pause: Pause the current execution
   - Export CSV: Save tokens to a CSV file
   - Export PDF: Save tokens to a PDF file

## Project Structure

```
lexvi/
├── lexer/
│   └── core.py          # Core lexer functionality
├── gui/
│   └── main_window.py   # GUI implementation
├── visualizer/
│   └── automata.py      # Visualization components
├── tests/
│   └── test_lexer.py    # Unit tests
├── main.py              # Application entry point
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## Testing

Run the test suite using pytest:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
