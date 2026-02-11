import pyautogui as auto
from reasoning import reason
import time

#Automate Task
def automate(steps):
  auto.PAUSE = 3.0
  auto.FAILSAFE = True
  
  for step in range(len(steps)):

    actions = steps[step]['action']

    for action in range(len(actions)):

      plan = actions[action]
      keyword = plan['keyword']

      if keyword == 'moveto':
        co_ord = plan['co-ord']
        auto.moveTo(co_ord['x'], co_ord['y'], duration=0.3) 
      
      elif keyword == 'click':
        if 'co-ord' in plan:
          auto.click(plan['co-ord']['x'],plan['co-ord']['y'])
        else:
          auto.click()
      
      elif keyword == 'doubleclick':
        if 'co-ord' in plan:
          auto.doubleClick(plan['co-ord']['x'],plan['co-ord']['y'])
        else:
          auto.doubleClick()
      
      elif keyword == 'rightclick':
        if 'co-ord' in plan:
          auto.rightClick(plan['co-ord']['x'],plan['co-ord']['y'])
        else:
          auto.rightClick()
      
      elif keyword == 'type':
        auto.write(plan['text'],interval=0.05)
      
      elif keyword == 'press':
        auto.press(plan['key'])
      
      elif keyword == 'wait':
        time.sleep(plan['duration']) # I still want to pause based on the AI feedback just for clarity

      elif keyword == 'dragto':
        co_ords = plan['co-ord']
        auto.dragTo(co_ords['x'],co_ords['y'],duration=0.5) 


def main():
  # get user input and operating system
  userInput = input('What task do you want me to perform: ')
  #operatingSystem = input('What OS do you use be specific: ')
  response = reason(userInput,OS=None)

  automate(response)

# I just did this cause it is a tradition 😂
if __name__ == "__main__":
  main()