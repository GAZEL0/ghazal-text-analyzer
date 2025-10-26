# Text Analyzer GUI by Muhammad GAZEL, GHAZALTECH.COM
# I keep this GUI aligned with the console analyzer so both stay consistent.

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from typing import List

from text_analyzer import (
    SentimentIntensityAnalyzer,
    analyze_text as console_analyze_text,
    ensure_vader_lexicon,
    format_top_words as console_format_top_words,
)

# I reuse the same analyzer instance to keep results identical in both apps.
ensure_vader_lexicon()
analyzer = SentimentIntensityAnalyzer()


def load_file() -> None:
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not path:
        return
    try:
        with open(path, "r", encoding="utf-8") as file_handle:
            content = file_handle.read()
    except Exception as exc:
        messagebox.showerror("File Error", f"Could not read the selected file.\n\nDetails: {exc}")
        return
    input_box.delete("1.0", tk.END)
    input_box.insert(tk.END, content)


def run_analysis() -> None:
    raw_text = input_box.get("1.0", tk.END).strip()
    if not raw_text:
        messagebox.showwarning("No Text", "Please enter or load some text first.")
        return

    results = console_analyze_text(raw_text, analyzer)
    freq_lines: List[str] = console_format_top_words(results["top_words"])
    scores = results["sentiment_scores"]

    output_lines: List[str] = [
        f"Word count: {results['words']}",
        f"Characters (with spaces): {results['chars_with_spaces']}",
        f"Characters (without spaces): {results['chars_without_spaces']}",
        "",
        "Top 5 Words:",
    ]
    output_lines.extend(freq_lines)
    output_lines.extend(
        [
            "",
            f"Sentiment: {results['sentiment_label']}",
            (
                "Scores -> "
                f"Pos: {scores['pos']:.3f}, "
                f"Neu: {scores['neu']:.3f}, "
                f"Neg: {scores['neg']:.3f}, "
                f"Compound: {scores['compound']:.3f}"
            ),
        ]
    )

    compiled_output = "\n".join(output_lines).strip()
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, compiled_output)
    output_box.config(state="disabled")


root = tk.Tk()
root.title("Text Analyzer - GHAZALTECH.COM")
root.geometry("780x740")
root.minsize(640, 560)
root.configure(bg="#0F172A")

header = tk.Label(
    root,
    text="Text Analyzer by GHAZAL TECH",
    font=("Poppins", 18, "bold"),
    bg="#0F172A",
    fg="#FBBF24",
    pady=16,
)
header.pack()

controls_frame = tk.Frame(root, bg="#0F172A")
controls_frame.pack(fill=tk.X, padx=12)

load_btn = tk.Button(
    controls_frame,
    text="Load Text File",
    command=load_file,
    font=("Poppins", 11),
    bg="#1E293B",
    fg="#F8FAFC",
    activebackground="#0E7490",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=16,
    pady=6,
)
load_btn.pack(side=tk.LEFT, pady=(0, 6))

analyze_btn = tk.Button(
    controls_frame,
    text="Analyze Text",
    command=run_analysis,
    bg="#0E7490",
    fg="white",
    font=("Poppins", 12, "bold"),
    padx=20,
    pady=8,
    relief="flat",
    cursor="hand2",
)
analyze_btn.pack(side=tk.RIGHT, pady=(0, 6))

input_label = tk.Label(
    root,
    text="Input Text",
    font=("Poppins", 13, "bold"),
    bg="#0F172A",
    fg="#FBBF24",
)
input_label.pack()

input_box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    height=12,
    font=("Consolas", 11),
    bg="#1E293B",
    fg="#E2E8F0",
    insertbackground="white",
    relief="flat",
    borderwidth=0,
)
input_box.pack(padx=12, pady=10, fill=tk.BOTH, expand=True)

output_label = tk.Label(
    root,
    text="Analysis Results",
    font=("Poppins", 13, "bold"),
    bg="#0F172A",
    fg="#FBBF24",
    pady=5,
)
output_label.pack()

output_box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    height=14,
    font=("Consolas", 10),
    bg="#1E293B",
    fg="#E2E8F0",
    insertbackground="white",
    relief="flat",
    borderwidth=0,
)
output_box.pack(padx=12, pady=6, fill=tk.BOTH, expand=True)
output_box.config(state="disabled")

root.mainloop()