import pyautogui as auto
import time
import sys

class Automate:
    """Main automation entry point.
    This module converts an AI-generated action plan into concrete UI actions
    using PyAutoGUI.
    """
    MAX_RETRIES = 3

    def __init__(self):
        self.json_plan = None

    def run(self, json_plan=None, reason=None, mode="advanced"):
        """Execute a plan using either the simple or advanced automation path."""

        if mode == "simple":
            return self.run_simple(json_plan)

        if mode == "advanced":
            return self.run_advanced(json_plan, reason)

        raise ValueError("Unknown automation mode. Use 'simple' or 'advanced'.")

    # Backward-compatible entry point for the advanced mode.
    def automate(self, json_plan=None, reason=None, retries=0):
        return self.run_advanced(json_plan, reason, retries=retries)

    def run_simple(self, json_plan=None):
        """Execute the full plan once without step verification."""

        self.validate_plan(json_plan)
        self.json_plan = json_plan

        self._configure_runtime()

        try:
            for step in self.json_plan:
                self._execute_step(step)
        except Exception as e:
            raise RuntimeError(f"error at run_simple -> {e}")

    def run_advanced(self, json_plan=None, reason=None, retries=0):
        """Execute a list of automation steps produced by the reasoning layer.

        Args:
            steps: List of step dictionaries. Each step must contain an `action` list
            with action dictionaries using keywords such as `moveto`, `click`, etc.
        """
        self.validate_plan(json_plan)
        if reason is None:
            raise ValueError("Advanced automation requires a reasoning instance")

        self.json_plan = json_plan

        if retries > self.MAX_RETRIES:
            raise RuntimeError("MAX TRIES EXCEEDED!!")
        

        if self.json_plan is None:
            raise ValueError("No plan to automate")
        
        self._configure_runtime()
        try:
            for step in self.json_plan:
                self._execute_step(step)
                
                # 2. verify step
                raw = reason._call_model(
                    reason.step_verification_prompt(step)
                )

                result = reason.clean_data(raw)

                status = result.get("status","ok")

                if status == "fail":
                    feedback = f"""
                    Step failed: {step['step']}
                    Reason: {result.get('reason', '')}
                    """
                    print(f"Step failed: {feedback}",file=sys.stderr)

                    # 3. regenerate plan with feedback
                    new_plan = reason.generate_plan(feedback)

                    if not new_plan:
                        raise RuntimeError("Regeneration failed")
                    
                    # restart with new plan
                    return self.run_advanced(new_plan, reason, retries + 1)
                
        except Exception as e:
            raise RuntimeError(f"error at run_advanced -> {e}")

    @staticmethod
    def _configure_runtime():
        auto.PAUSE = 3.0
        auto.FAILSAFE = True

    def _execute_step(self, step):
        for action in step['action']:
            self._execute_action(action)

    # helper function to execute task
    # used directly for the simple function
    def _execute_action(self, plan):
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
        
    @staticmethod
    def validate_plan(plan):
        if not isinstance(plan, list):
            raise ValueError("Plan must be a list")

        for i, step in enumerate(plan):
            if "action" not in step:
                raise ValueError(f"Step {i} missing 'action'")

            if not isinstance(step["action"], list):
                raise ValueError(f"Step {i} action must be a list")

            for action in step["action"]:
                if "keyword" not in action:
                    raise ValueError(f"Step {i} action missing 'keyword'")
