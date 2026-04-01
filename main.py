from reasoning import Reason
from automate import Automate
import platform
import sys

#get platform info
def get_os():
  """Gets the operating system the user currently uses to run the programme"""

  system = platform.system()

  if system == "Darwin":
    return "mac"
  
  elif system == "Windows":
    return "windows"
  
  return "linux"

def main():
  """Collect a user task, generate an action plan, and execute it."""
  
  try:
    # Prompt user for a natural-language task.
    userInput = input('What task do you want me to perform: ')

    print('Do not touch the machine!')
    print('Automation in progress...')

    # Generate step-by-step actions from the current desktop screenshot.
    response = Reason(userInput,get_os())
    execute = Automate()

    # Run the proposed action sequence.
    result = response.generate_plan()

    if not result:
      raise Exception("Failed to generate plan. Exiting...")

    execute.automate(result,response)
    
  except Exception as e:
    print('SOMETHING WENT WRONG! -->',e,file=sys.stderr)

# I just did this cause it is a tradition I do know the meaning!
if __name__ == "__main__":
  main()