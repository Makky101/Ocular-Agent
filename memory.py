import sys

class cache:
    """Simple cache helpers for task generation + verification state.
    Task cache files are separate from verification cache files so one flow
    does not overwrite the other.
    """
    def __init__(self):
        self.TASK_OUTPUT_FILE = 'task_output.json'
        self.TASK_INSTRUCTION_FILE = 'task_instruction.txt'

    def task_cache_write(self,task, json_data):
        """Store latest task instruction and model action-plan output."""
        try:
            with open(self.TASK_OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(json_data)
            with open(self.TASK_INSTRUCTION_FILE, 'w', encoding='utf-8') as f:
                f.write(task)
        except Exception as e:
            raise RuntimeError(f"Error writing task cache: {e}")


    def task_cache_read(self):
        """Read latest task instruction and model action-plan output.
        Returns:
            tuple[str, str] | None: (task, output) when available.
        """
        try:
            with open(self.TASK_INSTRUCTION_FILE, encoding='utf-8') as f:
                task = f.read()
            with open(self.TASK_OUTPUT_FILE, encoding='utf-8') as f:
                output = f.read()
            return task, output
        except FileNotFoundError:
            print('task cache not found',file=sys.stderr)
            return None
        except Exception as e:
            raise RuntimeError(f'Error reading task cache: {e}')