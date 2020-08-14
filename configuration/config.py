"""
Stores configuration items of an application. 
The configuration have to be defined by the user. 

Implemented in Singleton-Pattern
"""

from .conf import CONFIG

def print_actions():
  print("\n")
  print("SHOW - ")
  print("SET - ")
  print("UNDO - ")
  print("EXIT - ")
  return

def autocomplete(action):
  # 
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


if __name__ == '__main__':
  print(f'Config module')