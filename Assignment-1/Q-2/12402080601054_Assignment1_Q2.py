# Campus Password Audit
# Assignment 1 - Question 2
# Python 3.10+

from collections import deque


class AhoCorasick:
    """
    Aho-Corasick automaton for efficiently finding
    banned words inside passwords.
    """

    def __init__(self):
        # Each node contains:
        # 'next' -> dictionary of child nodes
        # 'fail' -> failure link
        # 'output' -> True if a banned word ends here
        self.nodes = [
            {
                "next": {},
                "fail": 0,
                "output": False
            }
        ]

    def add_word(self, word):
        """Add a banned word to the trie."""
        current = 0

        for ch in word.lower():
            if ch not in self.nodes[current]["next"]:
                self.nodes[current]["next"][ch] = len(self.nodes)

                self.nodes.append({
                    "next": {},
                    "fail": 0,
                    "output": False
                })

            current = self.nodes[current]["next"][ch]

        self.nodes[current]["output"] = True

    def build_failure_links(self):
        """Build failure links using BFS."""
        queue = deque()

        # Initialize failure links of root's children.
        for child in self.nodes[0]["next"].values():
            self.nodes[child]["fail"] = 0
            queue.append(child)

        while queue:
            current = queue.popleft()

            for ch, child in self.nodes[current]["next"].items():
                queue.append(child)

                failure = self.nodes[current]["fail"]

                # Follow failure links until a matching transition
                # is found or the root is reached.
                while (
                    failure != 0
                    and ch not in self.nodes[failure]["next"]
                ):
                    failure = self.nodes[failure]["fail"]

                if ch in self.nodes[failure]["next"]:
                    self.nodes[child]["fail"] = (
                        self.nodes[failure]["next"][ch]
                    )
                else:
                    self.nodes[child]["fail"] = 0

                # If a banned word ends at the failure node,
                # it also means a banned word exists here.
                if self.nodes[self.nodes[child]["fail"]]["output"]:
                    self.nodes[child]["output"] = True

    def contains_banned_word(self, text):
        """
        Return True if text contains any banned word.
        Search is case-insensitive.
        """
        current = 0

        for ch in text.lower():

            while (
                current != 0
                and ch not in self.nodes[current]["next"]
            ):
                current = self.nodes[current]["fail"]

            if ch in self.nodes[current]["next"]:
                current = self.nodes[current]["next"][ch]
            else:
                current = 0

            if self.nodes[current]["output"]:
                return True

        return False


def check_pattern(password):
    """
    Check whether the password satisfies all required
    character-pattern conditions.
    """

    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    previous = ""
    consecutive_count = 0

    for ch in password:

        # Check lowercase
        if ch.islower():
            has_lower = True

        # Check uppercase
        if ch.isupper():
            has_upper = True

        # Check digit
        if ch.isdigit():
            has_digit = True

        # Check allowed special symbols
        if ch in "$#@":
            has_special = True

        # Check consecutive repeated characters
        if ch == previous:
            consecutive_count += 1
        else:
            previous = ch
            consecutive_count = 1

        if consecutive_count > 3:
            return False

    return (
        has_lower
        and has_upper
        and has_digit
        and has_special
    )


def classify_password(password, automaton):
    """
    Classify a password according to the assignment rules.
    """

    # Length condition
    if not (6 <= len(password) <= 12):
        return "WEAK_LENGTH"

    # Pattern condition
    if not check_pattern(password):
        return "WEAK_PATTERN"

    # Banned-word condition
    if automaton.contains_banned_word(password):
        return "COMPROMISED"

    return "STRONG"


def main():
    try:
        # Read number of banned words
        b = int(input().strip())

        if not (1 <= b <= 10000):
            raise ValueError("Invalid number of banned words.")

        automaton = AhoCorasick()

        # Read banned words
        for _ in range(b):
            banned_word = input().strip()

            if not banned_word:
                raise ValueError("Banned word cannot be empty.")

            automaton.add_word(banned_word)

        # Build Aho-Corasick failure links
        automaton.build_failure_links()

        # Read number of passwords
        n = int(input().strip())

        if not (1 <= n <= 100000):
            raise ValueError("Invalid number of passwords.")

        # Process passwords
        for index in range(1, n + 1):
            password = input().rstrip("\n")

            # Constraint: password length <= 100
            if len(password) > 100:
                raise ValueError(
                    "Password length cannot exceed 100 characters."
                )

            classification = classify_password(
                password,
                automaton
            )

            print(f"{index}: {classification}")

    except ValueError as error:
        print(f"Input Error: {error}")


if __name__ == "__main__":
    main()