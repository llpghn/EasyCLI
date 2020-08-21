import getch
import sys
import re

from configuration import config

class CLI_Handler:
  
  # TODO: Two states, config and operate
  # TODO: Quit-Command alway possible
  # TODO: Implement Command-History
  # TODO: If theres no input and you press backsplash, error comes up
  
  run = True        # True = Runs main loop, False = Ends main loop
  command_history = []  # Stores commands as history
  history_counter = 0
  cursor_position = 0
  reprint_input = True  # If it is set to true, then the string will be
                      # reprinted to the console.

  CONSOLE_UNDERLINE = r'\033[4m'
  CONSOLE_CLEAR_FORMAT = r'\033[0m'
  VALID_CHAR_REGEX = re.compile(r"^[a-z\d\-_\s]+$")



  def __init__(self):
    print("Init Class Handler")

  def run(self):
    while(self.run):
      str_input = ""

      while (True):

        print(f'\r                                                 ' , end='', flush = True)
        print(f'\r', end='', flush= True)
      
        if (self.cursor_position != len(str_input)):
          # Cursor is somewhat in the middle of the text
          print('> ' + str_input[:self.cursor_position], end = '')
          print('\033[4m' + str_input[self.cursor_position] +'\033[0m', end = '')
          print(str_input[self.cursor_position+1:], end = '', flush=True)
        else:
          print(f'> {str_input}', end='', flush = True)



        # READ THE CHAR
        char = getch.getch()


        if (char == '\n'):  # enter
          print(str_input + '|')
          if config.interpret(str_input) == True:
            # addCommandToHistory(str_input)
            str_input = '' # Execution ok, clearing the string
            self.cursor_position = 0
          
          continue

        elif (char =='\t'):  # tabulator
          result = config.autocomplete(str_input)
          if not result == False: 
            str_input = result
            self.cursor_position = len(str_input)
            # addCommandToHistory(str_input)
          
          continue

        elif (hex(ord(char)) == '0x41'):  # Arrow up
          # str_input = getCommandFromHistory()
          
          continue

        elif (hex(ord(char)) == '0x44'):  # Arrow left
          #print("Arrow left")
          if (self.cursor_position > 1):
            self.cursor_position = self.cursor_position - 1
          continue

        elif (hex(ord(char)) == '0x43'):  # Arrow right
          if (self.cursor_position < len(str_input)):
            self.cursor_position = self.cursor_position + 1
          continue

        elif (hex(ord(char)) == '0x7f'):  # backspace 
          self.history_counter = 0
          #str_input = str_input[:-1]
          str_input = str_input[:self.cursor_position-1] + str_input[self.cursor_position:]
          self.cursor_position = self.cursor_position -1
          continue

        else:
          # append the char to the string 
          if (self.VALID_CHAR_REGEX.match(str(char))):
            if (self.cursor_position != len(str_input)):
              # Cursor is somewhat in the middle of the text
              input_first_part = str_input[:self.cursor_position]
              input_second_part = str_input[self.cursor_position:]
              str_input = input_first_part + char + input_second_part
            else:
              str_input = str_input + char
            self.cursor_position = self.cursor_position + 1
          continue


if __name__ == "__main__":
  
  cli = CLI_Handler()
  cli.run()

  print(f'Goodbye my friend :(')

