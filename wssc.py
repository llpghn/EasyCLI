import getch
import sys
import re

from configuration import config

class CLI_Handler:
  
  # TODO: Two states, config and operate
  # TODO: Quit-Command alway possible
  # TODO: Implement Command-History
  # TODO: If theres no input and you press backsplash, error comes up

  CONSOLE_UNDERLINE = '\033[4m'
  CONSOLE_CLEAR_FORMAT = '\033[0m'
  VALID_CHAR_REGEX = re.compile(r"^[a-z\d\-_\s]+$")

  # Key-Codes for input validation
  ENTER_HEX_KEYCODE = '0xa'
  TABULATOR_HEX_KEYCODE = '0x9'
  ARROWUP_HEX_KEYCODE = '0x41'
  ARROWLEFT_HEX_KEYCODE = '0x44'
  ARROWRIGHT_HEX_KEYCODE = '0x43'
  BACKSPACE_HEX_KEYCODE = '0x7f'



  run = True        # True = Runs main loop, False = Ends main loop
  cursor_position = 0
  str_input = ""

  def __init__(self):
    print("Init Class Handler")

  
  def printConsoleOutput(self) -> None:
    """
    Prints the Input from the console back to the console.
    """
    print(f'\r                                                 ' , end='', flush = True)
    print(f'\r', end='', flush= True)
    if (self.cursor_position != len(self.str_input)):
      # Cursor is somewhat in the middle of the text
      print('> ' + self.str_input[:self.cursor_position], end = '')
      print(self.CONSOLE_UNDERLINE + self.str_input[self.cursor_position] + self.CONSOLE_CLEAR_FORMAT, end = '')
      print(self.str_input[self.cursor_position+1:], end = '', flush=True)
    else:
      print(f'> {self.str_input}', end='', flush = True)
    return 

  def handleEnter(self) -> None:
    if config.interpret(self.str_input) == True:
     self.str_input = '' # Execution ok, clearing the string
     self.cursor_position = 0

  def handleTabulator(self) -> None:
    result = config.autocomplete(self.str_input)
    if not result == False: 
      self.str_input = result
      self.cursor_position = len(self.str_input)
    return

  def handleBackspace(self) -> None:
    self.history_counter = 0
    #str_input = str_input[:-1]
    self.str_input = self.str_input[:self.cursor_position-1] + self.str_input[self.cursor_position:]
    self.cursor_position = self.cursor_position -1
    return

  def appendCharToInput(self, char) -> None:
    if (self.VALID_CHAR_REGEX.match(str(char))):
      if (self.cursor_position != len(self.str_input)):
        # Cursor is somewhat in the middle of the text
        input_first_part = self.str_input[:self.cursor_position]
        input_second_part = self.str_input[self.cursor_position:]
        self.str_input = input_first_part + char + input_second_part
      else:
        self.str_input = self.str_input + char
      self.cursor_position = self.cursor_position + 1
    return

  def handleArrowLeft(self) -> None:
    if (self.cursor_position > 1):
      self.cursor_position = self.cursor_position - 1
  
  def handleArrowRight(self) -> None:
    if (self.cursor_position < len(self.str_input)):
      self.cursor_position = self.cursor_position + 1
  
  def run(self):
    while(self.run):

      self.printConsoleOutput()
      char = getch.getch()
      #print(hex(ord(char)))

      if (hex(ord(char)) == self.ENTER_HEX_KEYCODE): 
        self.handleEnter()

      elif (hex(ord(char)) == self.TABULATOR_HEX_KEYCODE): 
        self.handleTabulator()

      #elif (hex(ord(char)) == self.ARROWUP_HEX_KEYCODE): 
        # str_input = getCommandFromHistory()

      elif (hex(ord(char)) == self.ARROWLEFT_HEX_KEYCODE): 
        self.handleArrowLeft()

      elif (hex(ord(char)) == self.ARROWRIGHT_HEX_KEYCODE):
        self.handleArrowRight()

      elif (hex(ord(char)) == self.BACKSPACE_HEX_KEYCODE):
        self.handleBackspace()

      else:
        self.appendCharToInput(char)


if __name__ == "__main__":
  
  cli = CLI_Handler()
  cli.run()

  print(f'Goodbye my friend :(')

