import getch
import sys
import re

from configuration import config

APP_RUN = True        # True = Runs main loop, False = Ends main loop
command_history = []  # Stores commands as history
history_counter = 0
cursor_position = 0
reprint_input = True  # If it is set to true, then the string will be
                      # reprinted to the console.



# TODO: implement command history

# def addCommandToHistory(command):
#   """
#   Adds the command (completted or executed) to the COMMAND_HISTORY. 
#   """
#   command_history.append(command)
#   history_counter = 0
# def getCommandFromHistory():
#   """
#   Returns the command selected by the user.
#   """
#   if(len(command_history) == history_counter):
#     return command_history[0]
#   else:
#     return command_history[history_counter]


if __name__ == "__main__":
  
  regex_checker = re.compile(r"^[a-z\d\-_\s]+$")


  while(APP_RUN):
    stdin_string = ""

    while (True):

      print(f'\r                                                 ' , end='', flush = True)
      print(f'\r', end='', flush= True)
      #print(f'> {stdin_string}', end='', flush = True)

      if (cursor_position != len(stdin_string)):
        # Cursor is somewhat in the middle of the text
        print('> ' + stdin_string[:cursor_position], end = '')
        print('\033[4m' + stdin_string[cursor_position] +'\033[0m', end = '')
        print(stdin_string[cursor_position+1:], end = '', flush=True)
      else:
        print(f'> {stdin_string}', end='', flush = True)



      # READ THE CHAR
      char = getch.getch()


      if (char == '\n'):  # enter
        print(stdin_string + '|')
        if config.interpret(stdin_string) == True:
          # addCommandToHistory(stdin_string)
          stdin_string = '' # Execution ok, clearing the string
          cursor_position = 0
        reprint_input = True
        continue

      elif (char =='\t'):  # tabulator
        result = config.autocomplete(stdin_string)
        if not result == False: 
          stdin_string = result
          cursor_position = len(stdin_string)
          # addCommandToHistory(stdin_string)
        reprint_input = True
        continue

      elif (hex(ord(char)) == '0x41'):  # Arrow up
        # stdin_string = getCommandFromHistory()
        reprint_input = True
        continue

      elif (hex(ord(char)) == '0x44'):  # Arrow left
        #print("Arrow left")
        if (cursor_position > 1):
          cursor_position = cursor_position - 1
        continue

      elif (hex(ord(char)) == '0x43'):  # Arrow right
        if (cursor_position < len(stdin_string)):
          cursor_position = cursor_position + 1
        continue

      elif (hex(ord(char)) == '0x7f'):  # backspace 
        history_counter = 0
        #stdin_string = stdin_string[:-1]
        stdin_string = stdin_string[:cursor_position-1] + stdin_string[cursor_position:]
        cursor_position = cursor_position -1
        reprint_input = True
        continue

      else:
        # append the char to the string 
        if (regex_checker.match(str(char))):
          if (cursor_position != len(stdin_string)):
            # Cursor is somewhat in the middle of the text
            input_first_part = stdin_string[:cursor_position]
            input_second_part = stdin_string[cursor_position:]
            stdin_string = input_first_part + char + input_second_part
          else:
            stdin_string = stdin_string + char
          cursor_position = cursor_position + 1
          reprint_input = True
        continue

  # EXIT MAIN LOOP
  print(f'Goodbye my friend :(')

