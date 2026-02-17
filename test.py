import random
import subprocess
import sys
from dataclasses import dataclass

# Small structure to keep each test case readable.
@dataclass
class TestCase:
    name: str
    command: str




# Extra command pool for optional fuzz/random run.
# This helps discover odd behaviors outside deterministic tests.
cmd = [
    "open claude and discord",
    "open chrome",
    "open notepad",
    "open vscode",
    "open calculator",
    "open file explorer",
    "close active window",
    "minimize active window",
    "maximize active window",
    "switch to next window",
    "switch to previous window",
    "open new browser tab",
    "close current browser tab",
    "refresh browser tab",
    "scroll up page",
    "scroll down page",
    "press enter key",
    "press escape key",
    "press space key",
    "press tab key",
    "take screenshot",
    "open task manager",
    "close task manager",
    "mute system volume",
    "increase system volume",
    "decrease system volume",
    "open settings app",
    "open control panel",
]


def run_case(test_case: TestCase, timeout_seconds: int = 30) -> bool:
    print(f"\n Running: {test_case.name}")
    print(f"Input Task: {test_case.command}")

    try:
        # sys.executable ensures we use the SAME Python interpreter
        # that launched this test script (safer than hardcoding 'python').
        result = subprocess.run(
            [sys.executable, ".\\main.py"],
            input=f"{test_case.command}\n",  # simulate Enter key
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        print(f"TIMEOUT after {timeout_seconds}s")

        # Show partial logs if any were produced before timeout.
        if error.stdout:
            print("--- partial stdout ---")
            print(error.stdout)
        if error.stderr:
            print("--- partial stderr ---")
            print(error.stderr)
        return False
    except Exception as error:
        print(f"CRASH while running case: {error}")
        return False

    print(f"Return code: {result.returncode}")

    # Print output to make debugging easy.
    if result.stdout:
        print("--- stdout ---")
        print(result.stdout.strip())
    if result.stderr:
        print("--- stderr ---")
        print(result.stderr.strip())

    passed = result.returncode == 0
    print("PASS" if passed else "FAIL")


def run_test_suite():
    test_case = TestCase(
        name="random cmd",
        command=random.choice(cmd),
    )
    
    run_case(test_case)


if __name__ == "__main__":
    # You can change this to False if you only want deterministic tests.
    run_test_suite()