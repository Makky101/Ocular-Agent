import pyautogui as auto
from reasoning import reason
import time

#Automate Task
def automate(steps):
  auto.PAUSE = 3.0
  auto.FAILSAFE = True

  try:
    for step in range(len(steps)):

      actions = steps[step]['action']

      for action in range(len(actions)):

        plan = actions[action]
        keyword = plan['keyword']

        if keyword == 'moveto':
          co_ord = plan['co-ord']
          #auto.moveTo(co_ord['x'], co_ord['y'], duration=0.3) 
          print('it had co-ordinates at moveto')
        
        elif keyword == 'click':
          if 'co-ord' in plan:
            #auto.click(plan['co-ord']['x'],plan['co-ord']['y'])
            print('it had co-ordinates for click')
          else:
            #auto.click()
            print('it clicked')
        
        elif keyword == 'doubleclick':
          if 'co-ord' in plan:
            #auto.doubleClick(plan['co-ord']['x'],plan['co-ord']['y'])
            print('it had co-ordinates for doubleclick')
          else:
            #auto.doubleClick()
            print('it doubleclicked')
        
        elif keyword == 'rightclick':
          if 'co-ord' in plan:
            #auto.rightClick(plan['co-ord']['x'],plan['co-ord']['y'])
            print('it had co-ordinates for rightclick')
          else:
            #auto.rightClick()
            print('it rightClicked')
        
        elif keyword == 'type':
          #auto.write(plan['text'],interval=0.05)
          print('it typed')
        
        elif keyword == 'press':
          #auto.press(plan['key'])
          print('it pressed smth 🤷')
        
        elif keyword == 'wait':
          time.sleep(plan['duration']) # I still want to pause based on the AI feedback just for clarity
          print('it waited')

        elif keyword == 'dragto':
          co_ords = plan['co-ord']
          #auto.dragTo(co_ords['x'],co_ords['y'],duration=0.5) 
          print('it draggedTo')
  except Exception as e:
    print('error at automate ->',e)

def main():
  try:
    # get user input and operating system
    userInput = input('What task do you want me to perform: ')
    #operatingSystem = input('What OS do you use be specific: ')
    response = reason(userInput,OS=None)

    automate(response)
  except Exception as e:
    print('error at main --> ',e)

# I just did this cause it is a tradition 😂 I do know the meaning!
if __name__ == "__main__":
  main()