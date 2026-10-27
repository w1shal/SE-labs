# Lab 5 — Static Code Analysis: Event Manager

## Issue documentation table

Line numbers below refer to the supplied **original** `event_manager.py`; line numbers may change in the corrected file.

| # | Tool / code | Type / severity | Original line(s) | Description / impact | Fix approach |
|---:|---|---|---:|---|---|
| 1 | Bandit B605 | Security / High | 56 | `os.system()` builds a shell command by concatenating `eventName`; a crafted name could alter the command. | Replaced with `subprocess.run()` and an argument list, `shell=False`; sanitized the event name used in the badge filename. |
| 2 | Bandit B301 | Security / Medium | 51 | `pickle.load()` can execute code while deserializing a malicious pickle file. | Replaced pickle persistence with JSON and validated the loaded event structure. |
| 3 | Bandit B403 | Security / Low | 2 | Importing `pickle` is flagged because pickle-based deserialization is unsafe for untrusted data. | Removed `pickle` entirely and use JSON. |
| 4 | Bandit B311 | Security / Low | 72 | `random.choice()` is a non-cryptographic PRNG and may be unsuitable when a draw must be difficult to predict. | Used `secrets.choice()` for the lucky draw. |
| 5 | Pylint W0102 | Bug / correctness | 9 | `guests=[]` is a mutable default shared between calls, so events can accidentally share a guest list. | Changed the default to `None` and create a new list per event. |
| 6 | Pylint C0114 | Maintainability | 1 | The module has no module docstring. | Added a module docstring describing the program. |
| 7 | Pylint C0116 | Maintainability | 9, 15, 27, 32, 39, 44, 49, 54, 59 | Functions lack docstrings, making their intent and behavior less clear. | Added docstrings to every function. |
| 8 | Pylint C0103 | Style / maintainability | 9, 15, 27, 32, 39, 44, 49, 54 | Function and variable names such as `createEvent`, `eventName`, and `fileName` do not follow snake_case. | Renamed functions and parameters to snake_case. |
| 9 | Pylint W0613 | Maintainability / correctness | 39 | `sortOrder` is accepted by `guestReport()` but never used. | Implemented ascending and descending sorting and reject unsupported values. |
| 10 | Pylint R1705 | Readability | 33–36 | An `else` follows a branch that already returns. | Removed the unnecessary `else` and de-indented the second return. |
| 11 | Flake8 E231 | Style | 61 | Missing whitespace after a comma in `createEvent("Alumni Dinner", "Rooftop",2)`. | Added a space after the comma. |
| 12 | Flake8 E225 | Style | 66 | Missing whitespace around the assignment operator in `left=seatsLeft(...)`. | Changed to `left = seats_left(...)`. |
| 13 | Flake8 E261 | Style | 75 | Inline comment does not have the required two spaces before `#`. | Added the required spacing; the corrected version also keeps the comment concise. |
| 14 | Flake8 E305 | Style | 79 | Insufficient blank lines after the function definition before the module-level call. | Added the standard blank lines and guarded the entry point with `if __name__ == "__main__":`. |

## Reflection questions — suggested answers

> Note: The supplied three-page handout says to answer reflection questions but does not include the actual questions. These are suitable general responses; replace them if your instructor has provided a separate question sheet.

### 1. What is static code analysis, and why is it useful?
Static code analysis examines source code without executing it. It can reveal likely bugs, unsafe patterns, and style violations early, making software easier to maintain and review.

### 2. How do Pylint, Bandit, and Flake8 differ?
Pylint checks broader code quality, naming, documentation, and potential design problems. Bandit focuses on common Python security risks. Flake8 reports style and formatting violations, including many PEP 8 issues. Their scopes overlap in places, but they are complementary.

### 3. Which issue was most serious, and why?
The Bandit B605 finding was rated high severity because concatenating event-controlled text into a shell command can create command-injection risk. The pickle deserialization finding was also important because loading untrusted pickle data can execute attacker-controlled code.

### 4. What changes improved the program?
The fixes removed pickle, replaced shell command construction with a subprocess argument list, used `secrets.choice()` for the draw, eliminated the mutable default list, implemented the previously unused sorting argument, added docstrings, and corrected naming and formatting.

### 5. Can static analysis prove that a program is secure and correct?
No. Static analysis finds patterns that may indicate problems; it cannot prove the absence of all defects. Its findings need review, and the corrected program should also be run and tested with representative and edge-case inputs.

### 6. What did you learn from this lab?
Using multiple tools gives broader coverage than relying on one tool. Severity helps prioritize fixes, but low-severity maintainability and style issues also matter. Re-running the tools after each focused change provides evidence that the reported issues have been addressed.

## Report status

The supplied initial reports are preserved in `reports/before/`. The after reports must be generated locally after installing Pylint, Bandit, and Flake8, using the commands in the lab instructions. Do not label a report as an after report until it has actually been generated from the corrected program.
