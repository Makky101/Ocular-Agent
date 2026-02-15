def cached(json_data,mode=None):
    try:
        if mode == 'write':
            with open('task.json', 'w') as f:
                f.write(json_data)
        else:
            with open('task.json') as f:
                data = f.read()
                return data
    except FileNotFoundError:
        print('task.json not found')
        return None
    except Exception as e:
        print(f'Error in caching: {e}')
        return None