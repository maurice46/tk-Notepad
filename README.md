# Tk Notepad

A simple notepad application built with Python and Tkinter.

## Features

- Create, open, and save plain text files
- Warns you about unsaved changes before New, Open, or Exit
- Undo support (Ctrl+Z)
- Keyboard shortcuts:

| Action | Shortcut |
|--------|----------|
| New    | Ctrl+N   |
| Open   | Ctrl+O   |
| Save   | Ctrl+S   |
| Exit   | Ctrl+Q   |

## Requirements

- Python 3.8 or newer
- Tkinter (included with the Python installers from [python.org](https://www.python.org/downloads/) on Windows and macOS)

On Linux, you may need to install Tkinter separately:

```
sudo apt install python3-tk
```

## Running

```
git clone https://github.com/maurice46/tk-notepad.git
cd tk-notepad
python notepad.py
```

On some systems the command is `python3` instead of `python`.

## Building a standalone app (optional)

You can bundle the app so it runs without Python installed, using [PyInstaller](https://pyinstaller.org):

```
pip install pyinstaller
pyinstaller --windowed --name Notepad notepad.py
```

The result appears in the `dist/` folder. You need to build on each operating system you want to support.

Unsigned apps may trigger security warnings:

- **Windows:** SmartScreen shows "Windows protected your PC". Click **More info**, then **Run anyway**.
- **macOS:** Right-click the app, choose **Open**, and confirm.

## License

Released under the [MIT License](LICENSE).
