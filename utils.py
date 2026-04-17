import platform

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

# Keep the automation choices in one place so the wording is easy to tweak later.
# options
AUTOMATION_OPTIONS = [
  {
    "key": "simple",
    "aliases": {"", "1", "simple", "s"},
    "title": "Simple automation",
    "description": (
      "Generates one plan and runs it once. It is faster, uses fewer model calls, "
      "and is better for a limited free tier, but it does not verify each step."
    ),
  },
  {
    "key": "advanced",
    "aliases": {"2", "advanced", "a"},
    "title": "Advanced automation",
    "description": (
      "Verifies each step and can rebuild the plan after an error. It is slower and "
      "uses more model calls, but it is better at recovering when something changes "
      "on screen."
    ),
  },
]

def collect_automation_mode():
  """Ask the user which automation style to use for the current task."""

  print("\nChoose how the automation should run:")

  # display the options
  for option in AUTOMATION_OPTIONS:
    option_number = "1" if option["key"] == "simple" else "2"
    print(f"{option_number}. {option['title']} ({option['key']})")
    print(f"   {option['description']}")

  # let user pick option
  while True:
    choice = input(
      "\nSelect 1 for simple or 2 for advanced [default: simple]: "
    ).strip().lower()

    for option in AUTOMATION_OPTIONS:
      if choice in option["aliases"]:
        return option["key"]

    print("Please choose 1/2, simple/advanced, or press Enter for simple.")