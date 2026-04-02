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

def collect_user_task():
  """Let the user either type a task or speak it through the microphone."""

  # Keep the original typed flow as the default so existing usage still works.
  mode = input("Press Enter to type your task or type 'voice' to speak it: ").strip().lower()
  voice_mode = False
  if mode != "voice":
    return voice_mode,input('What task do you want me to perform: ')

  duration_text = input("How many seconds should I listen? (default 6): ").strip()

  # Use a short default recording window so the feature stays quick to use.
  if not duration_text:
    duration = 6
  else:
    try:
      duration = int(duration_text)
    except ValueError as e:
      raise ValueError("Recording duration must be a whole number of seconds.") from e

  # Import voice support only when the user asks for it, so typed usage stays unaffected.
  from voice_input import capture_voice_task

  user_input = capture_voice_task(duration=duration, playback=True)
  print(f"Captured task: {user_input}")
  voice_mode = True
  return voice_mode,user_input

def main():
  """Collect a user task, generate an action plan, and execute it."""
  
  try:
    # Prompt the user for either a typed task or a spoken task.
    used_voice,userInput = collect_user_task()

    if used_voice:
      print('The task you asked for if you used voice -->',userInput)

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
