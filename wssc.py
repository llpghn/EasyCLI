# A small websocket-client that can be used to query a wss service 
# that is operating on the JSON-RPC 2.0 protocol.

# Needed 'getch'
import getch
import sys

from configuration import config

APP_RUN = True

if __name__ == "__main__":
  # Welcome texts ...
  print(f'tab for help... at any place :)')  
  
  while(APP_RUN):
    stdin_string = ""

    while (True):

      print(f'\r                                                 ' , end='', flush = True)
      print(f'\r', end='', flush= True)
      print(f'> {stdin_string}', end='', flush = True)
      
      # READ THE CHAR
      char = getch.getch()
      
      if (char == '\n'):
        # ENTER PRESSED
        print("EXEC NOW...")
      
      elif (char =='\t'):
        # TABULATOR PRESSED
        
        #result = autocomplete(stdin_string)
        result = config.autocomplete(stdin_string)
        if not result == None: 
          stdin_string = result
        continue

      elif (hex(ord(char)) == '0x7f'):
        # BACKSPACE PRESSED
        stdin_string = stdin_string[:-1]
        continue

      else:
        # APPEND THE STRING
        stdin_string = stdin_string + char
      
    #if(str(stdin_string.rstrip()) == 'exit'):
    #  APP_RUN = False

  # EXIT MAIN LOOP
  print(f'Goodbye my friend :(')

