"""Simple file-based cache for the latest task and model output.

This helper persists:
- raw model response JSON text in `task.json`
- the corresponding user instruction in `instructions.txt`
"""


def cached(json_data=None,task=None,mode=None):
    """Write/read cached task artifacts used by verification flow.

    Args:
        json_data: Raw model output to write when mode='write'.
        task: Original task text to write when mode='write'.
        mode: 'write' to persist data, anything else to read cached data.

    Returns:
        list[str, str] | None: [model_output, task] when reading succeeds.
    """
    try:
        if mode == 'write':
            # Store most recent model output for verification retries.
            with open('task.json', 'w') as f:
                f.write(json_data)
            # NOTE: Keeping filename as-is to avoid changing runtime behavior.
            with open('instrucutions.txt','w') as f:
                f.write(task)
        else:
            # Retrieve cached output + original task.
            with open('task.json') as f:
                data = f.read()
            with open('instructions.txt') as f:
                task = f.read()
            return [data,task]
    except FileNotFoundError:
        print('task.json not found')
        return None
    except Exception as e:
        print(f'Error in caching: {e}')
        return None