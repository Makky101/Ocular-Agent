import pyautogui as auto
from reasoning import reason
from screenCapture import screenCapture
import time

def main():
  auto.FAILSAFE = True
  # get user input and operating system
  userInput = input('What task do you want me to perform: ')
  operatingSystem = input('What OS do you use: ')
  print(reason(userInput,operatingSystem))


if __name__ == "__main__":
    main()