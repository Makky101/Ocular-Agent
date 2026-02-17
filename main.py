import pyautogui as auto
from reasoning import reason,error_checking
import time

"""Main automation entry point.
This module converts an AI-generated action plan into concrete UI actions
using PyAutoGUI.
"""

# Automate Task
def automate(steps):
  """Execute a list of automation steps produced by the reasoning layer.
  Args:
    steps: List of step dictionaries. Each step must contain an `action` list
      with action dictionaries using keywords such as `moveto`, `click`, etc.
  """
  
  auto.PAUSE = 3.0
  auto.FAILSAFE = True

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
        
        # Explicit wait to handle UI transitions/loading states.
        elif keyword == 'wait':
          time.sleep(plan['duration']) # I still want to pause based on the AI feedback just for clarity

        # Click-and-drag from current position to destination coordinates.
        elif keyword == 'dragto':
          co_ords = plan['co-ord']
          auto.dragTo(co_ords['x'],co_ords['y'],duration=0.5) 
  except Exception as e:
    print('error at automate ->',e)

def main():
  """Collect a user task, generate an action plan, and execute it."""
  try:
    # Prompt user for a natural-language task.
    userInput = input('What task do you want me to perform: ')
    # Generate step-by-step actions from the current desktop screenshot.
    response = reason(userInput,default=True,OS=None)
    
    print('do not touch the machine!')

    # Run the proposed action sequence.
    automate(response)

    # If verification asks for edits, retry the same response.
    while True:
      status = error_checking()
      if status == 'edit':
        automate(response)
      else:
        break
  except Exception as e:
    print('error at main --> ', e)

# I just did this cause it is a tradition 😂 I do know the meaning!
if __name__ == "__main__":
  main()