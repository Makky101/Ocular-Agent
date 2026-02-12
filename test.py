import subprocess
import time
import random

#test commands
basic_it_operations = [
    "open calude and discord",
    "open_chrome",
    "open_notepad",
    "open_vscode",
    "open_calculator",
    "open_file_explorer",
    "close_active_window",
    "minimize_active_window",
    "maximize_active_window",
    "switch_to_next_window",
    "switch_to_previous_window",
    "open_new_browser_tab",
    "close_current_browser_tab",
    "refresh_browser_tab",
    "scroll_up_page",
    "scroll_down_page",
    "press_enter_key",
    "press_escape_key",
    "press_space_key",
    "press_tab_key",
    "take_screenshot",
    "open_task_manager",
    "close_task_manager",
    "mute_system_volume",
    "increase_system_volume",
    "decrease_system_volume",
    "open_settings_app",
    "open_control_panel"
]

#just run test I cant be typing all day long
def test():
    process = subprocess.Popen(
        ['python','.\\main.py'],
        stdin=subprocess.PIPE, #Allow sending input
        stdout=subprocess.PIPE, # Capture output
        stderr=subprocess.PIPE, # Capture errors
        text=True #Ensures its in strings and not bytes
    )

    process.stdin.write(f'{random.choice(basic_it_operations)}\n') #simulates pressing Enter
    process.stdin.flush() #Ensures data is sent immediately

#run test
test()