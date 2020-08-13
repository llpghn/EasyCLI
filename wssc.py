# A small websocket-client that can be used to query a wss service 
# that is operating on the JSON-RPC 2.0 protocol.

# Needed 'getch'
import getch
import sys

CONFIG = {
  "APP" : {
    "_desc": "Config. Top-Layer of Configuration item.",
    "VERSION": {
      "_desc": "Version of this client.",
      "MAYOR" : {
        "_value": 0,
        "_desc": "0..100  Major version of client",
      },
      "MINOR" : {
        "_value": 10,
        "_desc": "0..100 Version Minor number", 
      }
    }
    
  },
}

APP_RUN = True

def print_actions():
  print("\n")
  print("SHOW - ")
  print("SET - ")
  print("UNDO - ")
  print("EXIT - ")
  return

def autocomplete(action):
  #####################################
  # Check if the first element is a valid action, else do nothing
  #####################################
  if(len(action.split())==0):
    print_actions()
    return None
  else:
    op = action.split()[0]
    if("SHOW".find(op.upper()) == 0) and (len(op) < 4):
      return "SHOW "
    if("SET".find(op.upper()) == 0) and (len(op) < 3):
      return "SET "
    if("UNDO".find(op.upper()) == 0) and (len(op) < 4):
      return "UNDO "
    if("EXIT".find(op.upper()) == 0) and (len(op) < 4):
      return "EXIT "
    
    found = False
    if (op.upper() == 'SET'):
      found = True
    if (op.upper() == 'SHOW'):
      found = True
    if (op.upper() == 'UNDO'):
      found = True
    
    if not found:
      print_actions()
      return None

  #################################################
  # Reduce the config to the last complete subnode.
  #################################################
  subconf = CONFIG  # Temporar config 
                    # Holds the reference to the last node that can be found
  for layer in action.split()[1:]:
    if layer.upper() in subconf:
      subconf = subconf[layer.upper()] # Saving the smaller subconfig...
  
  #################################################
  # Check if we have reached a leave in the config structure
  #################################################
  contain_subnodes = False
  for item in subconf:
    if item[0] != "_":
      contain_subnodes = True

  ##############################################
  # Check if we can autocomplete the input
  ##############################################

  if contain_subnodes == True:
    automatches_found = 0
    completion_string = ""

    for item in subconf:
      #print('--- ' + item)
      # Check if the item starts with what was inputted
      to_complete_action = action.split()[-1]
      #print(to_complete_action)
      if item.upper().find(to_complete_action.upper()) == 0:
        automatches_found = automatches_found + 1
        completion_string = item
        print('---'+ completion_string)
    # Have we found a Entry to that we can autocomplete
    if automatches_found == 1:
      new_action = ""
      for sub_action in action.split()[:-1]:
        new_action = new_action + sub_action + " "
      new_action = new_action + completion_string + " "
      return new_action

  ###################################################
  # Print all subnodes in tree
  ###################################################
  print("\n")
  if contain_subnodes:
    # Print available subnodes
    for item in subconf: 
      # Schreibe alle Nodes die kein Blatt darstellen
      if item[0] != '_':
        print(f'{item}') 
  else:
    print('<cr> \t' + subconf['_desc'])

  return None



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
        #helper(stdin_string)
        result = autocomplete(stdin_string)
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

