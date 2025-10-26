# Text Analyzer

A clean text-insight toolkit built by Muhammad GAZEL (GHAZALTECH.COM) for both terminal purists and desktop users. The core analyzer powers word and character stats, top-word frequency, and VADER sentiment scoring, while the GUI wraps everything in a polished Tkinter experience ready for portfolio demos or client handoffs.

## Features
- Dual experience: interactive console flow (`text_analyzer.py`) and modern Tkinter window (`text_analyzer_gui.py`).
- Smart input handling: analyze plain text pasted into the app or load UTF-8 files with path validation.
- Detailed metrics: word count, characters with/without spaces, and the top five repeated words.
- Sentiment intelligence: NLTK VADER integration with labeled tone plus raw positive/neutral/negative/compound scores.
- Ready-to-package GUI: includes icon, PyInstaller spec, and tested EXE build artifacts (`text_analyzer GT.exe`).

## Requirements
- Python 3.10+ with `pip` available in your PATH.
- `nltk` (install via `pip install nltk`).
- Tkinter ships with the standard Python installer on Windows/macOS; on Linux, install your distro's `python3-tk` package.

> Both the console and GUI scripts download the VADER lexicon automatically when it is missing. If you prefer to preload it manually, run a Python shell and execute:
>
> ```python
> import nltk
> nltk.download("vader_lexicon")
> ```

## Project Structure
| Path | Purpose |
| ---- | ------- |
| `text_analyzer.py` | Console app with guided prompts and panel-styled terminal output. |
| `text_analyzer_gui.py` | Tkinter UI that reuses the console analyzer for identical results. |
| `text_analyzer_gui.spec` | PyInstaller configuration for the GUI build. |
| `logo.ico` | Icon used when packaging the Windows executable. |
| `dist/`, `build/`, `text_analyzer GT.exe` | Existing PyInstaller output (safe to regenerate). |

## Getting Started
1. (Optional) Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install nltk
   ```
3. (Optional) Download the VADER lexicon ahead of time as shown above.

## Running the Console Analyzer
```bash
python text_analyzer.py
```
Follow the on-screen prompt:
- Choose option 1 to analyze a saved `.txt` file. Paths with spaces and `~` (home) are supported.
- Choose option 2 to paste or type text directly. Type `END` on its own line when you finish.
The app prints a banner followed by overview, top-word, and sentiment panels.

## Running the GUI Analyzer
```bash
python text_analyzer_gui.py
```
- Click **Load Text File** to populate the input box, or paste text directly.
- Press **Analyze Text** to view the same metrics and sentiment scores inside the window.
- Results are read-only so you can copy them without accidental edits.

### Using the Packaged EXE
A ready-made build lives at `text_analyzer GT.exe`. Double-click it to launch the GUI without opening a console. If SmartScreen warns you, choose **More info** -> **Run anyway** (expected for unsigned personal builds).

## Building Your Own Windows Executable
1. Ensure PyInstaller is installed (`pip install pyinstaller`).
2. Run one of the following commands from the project root:
   ```bash
   pyinstaller text_analyzer_gui.spec
   # or
   pyinstaller --noconsole --onefile --icon logo.ico text_analyzer_gui.py
   ```
3. Find the fresh executable inside `dist/`. Copy `logo.ico` alongside it if you want the icon in Windows Explorer.

## Notes
- The GUI imports the console analyzer to keep all calculations, formatting, and thresholds perfectly aligned.
- Both applications store no data; everything stays in memory until you close the session.
- If you modify the logic in `text_analyzer.py`, the GUI automatically inherits those changes because it reuses the same functions.

Enjoy showcasing the Text Analyzer in your portfolio or sharing it with clients!
