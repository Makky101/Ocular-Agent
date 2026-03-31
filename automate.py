import pyautogui as auto
import time

class Automate:

    """Main automation entry point.
    This module converts an AI-generated action plan into concrete UI actions
    using PyAutoGUI.
    """
    def __init__(self):
        self.json_plan = None
    # Automate Task
    def automate(self,json_plan=None):
        """Execute a list of automation steps produced by the reasoning layer.

        Args:
            steps: List of step dictionaries. Each step must contain an `action` list
            with action dictionaries using keywords such as `moveto`, `click`, etc.
        """
        self.json_plan  = json_plan

        if self.json_plan is None:
            raise ValueError("No plan to automate")
        
        auto.PAUSE = 3.0
        auto.FAILSAFE = True
        steps = self.json_plan
        try:
            for step in range(len(steps)):

                actions = steps[step]['action']

                for action in range(len(actions)):
                    plan = actions[action]
                    keyword = plan['keyword']

                    # Move cursor to target coordinates before interaction.
                    if keyword == 'moveto':
                        co_ord = plan['co-ord']
                        auto.moveTo(co_ord['x'], co_ord['y'], duration=0.3) 
                
                    # Click at provided coordinates or current cursor location.
                    elif keyword == 'click':
                        if 'co-ord' in plan:
                            auto.click(plan['co-ord']['x'],plan['co-ord']['y'])
                        else:
                            auto.click()
                        
                    # Double-click where requested.
                    elif keyword == 'doubleclick':
                        if 'co-ord' in plan:
                            auto.doubleClick(plan['co-ord']['x'],plan['co-ord']['y'])
                        else:
                            auto.doubleClick()
                    
                    # Right-click for context menus or secondary actions.
                    elif keyword == 'rightclick':
                        if 'co-ord' in plan:
                            auto.rightClick(plan['co-ord']['x'],plan['co-ord']['y'])
                        else:
                            auto.rightClick()
                    
                    # Type text into the currently focused input field.
                    elif keyword == 'type':
                        auto.write(plan['text'],interval=0.05)
                    
                    # Press keyboard key (enter/tab/esc/etc.).
                    elif keyword == 'press':
                        auto.press(plan['key'])

                    # Press key combination (e.g. win+r, ctrl+l).
                    elif keyword == 'hotkey':
                        auto.hotkey(*plan['keys'])
                    
                    # Explicit wait to handle UI transitions/loading states.
                    elif keyword == 'wait':
                        time.sleep(plan['duration']) # I still want to pause based on the AI feedback just for clarity

                    # Click-and-drag from current position to destination coordinates.
                    elif keyword == 'dragto':
                        co_ords = plan['co-ord']
                        auto.dragTo(co_ords['x'],co_ords['y'],duration=0.5) 
        except Exception as e:
            raise RuntimeError(f"error at automate: {e}")

    #retry steps
    def retry(self,reason):
        try:
            max_retries = 3
            attempt = 0
            feedback = None
            while attempt < max_retries:
                print(f"\nAttempt {attempt + 1}/{max_retries}")
                verification = reason.verify_execution()
                status = verification["status"]
                feedback = verification["reason"]
                if status == 'exit':
                    print("Task completed successfully")
                    return
                elif status == 'edit':
                    plan = reason.generate_plan(feedback)
                    if not plan:
                        raise RuntimeError("Plan regeneration failed during retry")
                    self.automate(plan)
                    attempt += 1
                else:
                    print(f"Verification failed. {feedback}")
                    attempt += 1

            print("Max retries reached.Task failed.")

        except Exception as e:
            raise RuntimeError(f"error during automation: {e}")
