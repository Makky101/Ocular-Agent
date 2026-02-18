"""Simple cache helpers for task generation + verification state.

Task cache files are separate from verification cache files so one flow
does not overwrite the other.
"""

TASK_OUTPUT_FILE = 'task_output.json'
TASK_INSTRUCTION_FILE = 'task_instruction.txt'


def task_cache_write(task, output):
    """Store latest task instruction and model action-plan output."""
    try:
        with open(TASK_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(output)
        with open(TASK_INSTRUCTION_FILE, 'w', encoding='utf-8') as f:
            f.write(task)
    except Exception as e:
        print(f'Error writing task cache: {e}')


def task_cache_read():
    """Read latest task instruction and model action-plan output.

    Returns:
        tuple[str, str] | None: (task, output) when available.
    """
    try:
        with open(TASK_INSTRUCTION_FILE, encoding='utf-8') as f:
            task = f.read()
        with open(TASK_OUTPUT_FILE, encoding='utf-8') as f:
            output = f.read()
        return task, output
    except FileNotFoundError:
        print('task cache not found')
        return None
    except Exception as e:
        print(f'Error reading task cache: {e}')
        return None