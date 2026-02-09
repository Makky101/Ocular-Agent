import pyautogui as auto
from reasoning import reason

def main():
    auto.FAILSAFE = True
    '''# get user input and operating system
    userInput = input('What task do you want me to perform: ')
    operatingSystem = input('What OS do you use: ')
    print(reason(userInput,operatingSystem))

    auto.moveTo(500,1000,duration=3)
    auto.click()
    auto.write("I just used the pyautogui respond back briefly", interval=0.1)'''
    #print(reason())
    auto.moveTo(202,915,duration=3) 

  #'You are a **Technical Operator** that can handle everyday task on a computer and **only** has access to user screen as' f'the laptop will be on already. Write **a software based method step by step approach checklist** that will enable you to accomplish the specific task given to you on this specific Operating System:{OS}.' f'The task:{task}'

if __name__ == "__main__":
    main()