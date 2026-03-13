import difflib
import re
import shlex

from colorama import Fore, Style


def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = shlex.split(user_input)
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.strip().lower(), args


def get_special_response(user_input: str) -> str | None:
    input_lower = user_input.lower()

    if "слава україні" in input_lower or input_lower == "слава":
        return Fore.YELLOW + Style.BRIGHT + "Героям Слава! 🇺🇦"

    if "слава нації" in input_lower:
        return Fore.RED + Style.BRIGHT + "Смерть ворогам! 💀"

    if "україна" in input_lower and "понад усе" not in input_lower:
        return Fore.BLUE + Style.BRIGHT + "Понад усе! 💙" + Fore.YELLOW + Style.BRIGHT + "💛"

    if "путін" in input_lower:
        return Fore.RED + Style.BRIGHT + "Хуйло! ❌"

    return None


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def get_suggestion(command: str, commands: list[str]) -> str | None:
    matches = difflib.get_close_matches(command, commands, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_intent_suggestion(
    user_input: str,
    commands: list[str],
    intent_phrases: dict[str, list[str]],
) -> str | None:
    normalized = normalize_text(user_input)
    if not normalized:
        return None

    best_command = None
    best_score = 0.0

    for command, phrases in intent_phrases.items():
        for phrase in phrases:
            ratio = difflib.SequenceMatcher(None, normalized, phrase).ratio()
            if phrase in normalized:
                ratio = max(ratio, 0.95)
            if ratio > best_score:
                best_score = ratio
                best_command = command

    command_guess = difflib.get_close_matches(normalized, commands, n=1, cutoff=0.55)
    if command_guess and best_score < 0.72:
        return command_guess[0]

    return best_command if best_score >= 0.5 else None