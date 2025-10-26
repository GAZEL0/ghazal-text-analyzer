# Text Analyzer by Muhammad GAZEL, GHAZALTECH.COM
# I keep the imports explicit so the script reads clearly at a glance.
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple
import textwrap

try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
except ImportError:
    print("nltk is required for this project. Install it with 'pip install nltk' and run again.")
    sys.exit(1)


# I make sure the sentiment lexicon is ready before running the analyzer.
def ensure_vader_lexicon() -> None:
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        print("\nSetting up the NLTK VADER lexicon (this only runs once)...")
        nltk.download("vader_lexicon")


# I draw a lightweight banner to welcome anyone who runs this tool.
def display_banner() -> None:
    width = 74
    tagline = "Text insights ready in seconds"
    print("=" * width)
    print("TEXT ANALYZER".center(width))
    print(tagline.center(width))
    print("=" * width)
    print()


# I keep every panel consistent so the terminal output stays tidy.
def print_panel(title: str, lines: List[str]) -> None:
    inner_width = max(len(title) + 4, max((len(line) for line in lines), default=0))
    inner_width = max(inner_width, 48)
    border = "+" + "-" * (inner_width + 2) + "+"
    print(border)
    print(f"| {title.center(inner_width)} |")
    print("| " + "-" * inner_width + " |")
    for line in lines:
        wrapped = textwrap.wrap(line, inner_width) or [""]
        for segment in wrapped:
            print(f"| {segment.ljust(inner_width)} |")
    print(border)
    print()


# I collect the user's preferred input method so the flow feels guided.
def prompt_input_method() -> str:
    print_panel(
        "Input Options",
        [
            "1) Analyze a text file",
            "2) Paste or type text directly",
            "I accept file paths with spaces and I expand ~ for home directories.",
        ],
    )
    while True:
        choice = input("Choose an option (1 or 2): ").strip()
        if choice in {"1", "2"}:
            return choice
        print("Please type 1 or 2 so I know which route to take.\n")


# I read text from disk and validate the path so users get quick feedback.
def read_text_from_file() -> str:
    while True:
        raw_path = input("\nEnter the path to your text file: ").strip().strip('"')
        if not raw_path:
            print("Please provide a file path so I can keep going.")
            continue
        candidate = Path(os.path.expanduser(raw_path)).resolve()
        if not candidate.is_file():
            print("I could not find that file. Double-check the path and try again.")
            continue
        try:
            text = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = candidate.read_text(encoding="utf-8", errors="replace")
        if text.strip():
            return text
        print("That file looks empty. Pick another file or use manual input.")


# I capture manual text input and finish when the user types END on its own line.
def read_text_from_input() -> str:
    print("\nPaste or type your text below. Type END on a new line when you are finished.\n")
    lines: List[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() == "END":
            break
        lines.append(line)
    text = "\n".join(lines).strip()
    if text:
        return text
    print("I did not capture any text. Let's try that again.\n")
    return read_text_from_input()


# I gather the final text payload based on the user's selection.
def collect_text() -> str:
    while True:
        method = prompt_input_method()
        if method == "1":
            return read_text_from_file()
        return read_text_from_input()


# I keep the sentiment labels in one place so they stay consistent.
def label_sentiment(score: float) -> str:
    if score >= 0.05:
        return "Positive"
    if score <= -0.05:
        return "Negative"
    return "Neutral"


# I run all calculations in one pass so the analysis stays fast.
def analyze_text(text: str, analyzer: SentimentIntensityAnalyzer) -> Dict[str, object]:
    cleaned = text.strip()
    words = re.findall(r"\b[\w']+\b", cleaned.lower())
    word_count = len(words)
    characters_with_spaces = len(cleaned)
    characters_without_spaces = sum(1 for char in cleaned if not char.isspace())
    word_frequencies = Counter(words).most_common(5)
    sentiment_scores = analyzer.polarity_scores(cleaned) if cleaned else {"compound": 0.0, "pos": 0.0, "neu": 0.0, "neg": 0.0}
    sentiment_label = label_sentiment(sentiment_scores["compound"])
    return {
        "words": word_count,
        "chars_with_spaces": characters_with_spaces,
        "chars_without_spaces": characters_without_spaces,
        "top_words": word_frequencies,
        "sentiment_label": sentiment_label,
        "sentiment_scores": sentiment_scores,
        "preview": (cleaned[:200] + "...") if len(cleaned) > 200 else cleaned,
    }


# I format the frequency table so it reads like a quick leaderboard.
def format_top_words(top_words: List[Tuple[str, int]]) -> List[str]:
    if not top_words:
        return ["No words detected. Add more text to see frequency insights."]
    lines = []
    for index, (word, count) in enumerate(top_words, start=1):
        lines.append(f"{index}. {word} - {count} time(s)")
    return lines


# I centralize the display logic so the results come out polished every time.
def show_results(summary: dict) -> None:
    overview_lines = [
        f"Word count: {summary['words']}",
        f"Characters (with spaces): {summary['chars_with_spaces']}",
        f"Characters (without spaces): {summary['chars_without_spaces']}",
        f"Sample preview: {summary['preview'] or 'N/A'}",
    ]
    print_panel("Overview", overview_lines)

    freq_lines = format_top_words(summary["top_words"])
    print_panel("Most Frequent Words", freq_lines)

    scores = summary["sentiment_scores"]
    sentiment_lines = [
        f"Overall tone: {summary['sentiment_label']}",
        f"Compound score: {scores['compound']:.3f}",
        f"Positive: {scores['pos']:.3f} | Neutral: {scores['neu']:.3f} | Negative: {scores['neg']:.3f}",
    ]
    print_panel("Sentiment", sentiment_lines)
    print("Thanks for exploring your text with this analyzer.\n")


# I orchestrate the flow so running the script feels effortless.
def main() -> None:
    display_banner()
    ensure_vader_lexicon()
    analyzer = SentimentIntensityAnalyzer()
    text = collect_text()
    results = analyze_text(text, analyzer)
    show_results(results)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSession canceled. See you next time!")
