from reasoning import Reason
from automate import Automate
from utils import collect_automation_mode, collect_user_task , get_os
import sys

def main():
  """Collect a user task, generate an action plan, and execute it."""
  
  try:
    # Prompt the user for either a typed task or a spoken task.
    used_voice,userInput = collect_user_task()
    automation_mode = collect_automation_mode()

    # Just to verify if the voice feature captured what it said it will
    '''if used_voice:
      print('The task you asked for if you used voice -->',userInput)'''

    print(f"Selected mode: {automation_mode}")
    print('Do not touch the machine!')
    print('Automation in progress...')

    # Generate step-by-step actions from the current desktop screenshot.
    response = Reason(userInput,get_os())
    execute = Automate()

    # Run the proposed action sequence.
    result = response.generate_plan()

    if not result:
      raise Exception("Failed to generate plan. Exiting...")

    execute.run(result,response, mode=automation_mode)
    
  except Exception as e:
    print('SOMETHING WENT WRONG! -->',e,file=sys.stderr)

# I just did this cause it is a tradition I do know the meaning!
if __name__ == "__main__":
  main()
