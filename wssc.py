import getch
import sys

from configuration import config

APP_RUN = True

# TODO: implement command history

if __name__ == "__main__":

  while(APP_RUN):
    stdin_string = ""

    while (True):

      print(f'\r                                                 ' , end='', flush = True)
      print(f'\r', end='', flush= True)
      print(f'> {stdin_string}', end='', flush = True)
      
      # READ THE CHAR
      char = getch.getch()
      if (char == '\n'):  # enter
        if config.interpret(stdin_string) == True:
          stdin_string = '' # Execution ok, clearing the string
      elif (char =='\t'):  # tabulator
        result = config.autocomplete(stdin_string)
        if not result == False: 
          stdin_string = result
        continue
      elif (hex(ord(char)) == '0x7f'):  # backspace 
        # TODO: Only deletion on the end are valid, there is 
        #       no possibility to change a value in the middle
        #       of the input
        stdin_string = stdin_string[:-1]
        continue
      else:
        # append the char to the string 
        stdin_string = stdin_string + char
  # EXIT MAIN LOOP
  print(f'Goodbye my friend :(')

