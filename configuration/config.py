"""
Stores configuration items of an application. 
The configuration have to be defined by the user. 

Implemented in Singleton-Pattern
"""

# TODO: Wenn man das Commando ausführen will aber dann einen Wert 
#       in dem commando hat der ausgeschrieben wurde, dann wird 
#       das Commando nicht ausgeführt. Anscheinend bricht er dann 
#       den Autocomplete ab wenn er den Qualified Commando bildet.

from .conf import CONFIG
import re

def print_actions():
  """
  Prints the basic function available while working with the
  config-menue.
  """
  print("\n")
  print("No valid action, valid actions are:")
  print("SHOW - ")
  print("SET - ")
  print("UNDO - ")
  print("EXIT - ")
  return


def checkOnValidAction(str):
  """
  Checks if 'str' is a valid action that is included in the validActions-list. 
  If it is a valid action, then the action is returned as string. Else the 
  function returnes false.

  @param str [IN]: String that defines an action that will be checked
  """
  validActions = ['SHOW', 'SET', 'EXIT', 'UNDO']
  count_actions = 0
  action = ""
  for validAction in validActions:
    if( validAction.find(str.upper()) == 0 ):
      count_actions = count_actions + 1
      action = validAction
  if( count_actions == 1):
    return action
  print_actions()
  return False
  
# Main autocomplete function that searches the input if possible 
# or prints some helping texts.
def autocomplete(action):
  # No input was done...
  if( len(action.split()) == 0 ): 
    print_actions()
    return False # No input done, do nothing...
  
  # There is only word inputted. Check if is, or can be expanded
  # to a valid action
  if( len(action.split()) == 1 ):
    op = action.split()[0]
    res = checkOnValidAction(op)
    
    if isinstance(res, str):
      
      #print (op + " ... " + res)
      if not op.upper() == res.upper():
        if not action[-1] == ' ':
          return res + ' '
    else:
      print_actions()
      return action

    #if( checkOnValidAction(op) == False):
    #  return False

  # At this part we have a valid function or we never made it up to
  # this point.
  subconf = CONFIG  
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

      to_complete_action = action.split()[-1]

      if item.upper().find(to_complete_action.upper()) == 0:
        automatches_found = automatches_found + 1
        completion_string = item
        print('---'+ completion_string)

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
    for item in subconf: 
      if item[0] != '_':
        print(f'{item}') 
  else:
    print('<cr> \t' + subconf['_desc'])

  return False

# interpret()
# Used as entry point so devide what should happen with the user input. 
# If called the module will try to interpet the string and the execute the 
# order
def interpret(input):
  parts = input.split()
  if(len(parts) > 0): # Only enable interpreting when the user actually inputted something
    if("SET".find(parts[0].upper()) == 0):
      # Change a leave in the Config parts ...
      return changeValue(parts[1:])
      #print("SET MUST BE DONE")
    if("SHOW".find(parts[0].upper()) == 0):
      return showValue(parts[1:])
  return None

def showValue(path):
  # Searching for the value to be shown
  sub_config = CONFIG
  validated_input = "SHOW " # This string will be validated first
                            # If someone uses the shorted version 
                            # this string will contain the string
                            # that will be really used....
  
  # Now try to find the element, we need to do it twice, because if 
  # you want the short form of identification, the app first needs 
  # to build a validated string, that will search for the short version.
  # IMPLEMENTATION OF THE INPUT OF SHORTENED STRINGS ... 
  for x in path:
    try:
      sub_config = sub_config[x] 
      validated_input = validated_input + x + " "
    except KeyError:
      # Normally on this part there would be the autocomplete 
      # mechanismen, -> sh   a   ver     ma
      #              -> SHOW APP VERSION MAYOR
      ret = autocomplete(validated_input + x)
      if ret != False:
        validated_input = ret
      else:
        print('\n No valid element')
        return False
  # When possible we have a validated String that identifies a leave
  # Now slicing the config into subparts until we have the designated element
  sub_config = CONFIG # Now loading the elements.
  for vs in validated_input.split()[1:]:
    sub_config = sub_config[vs]
  
  # Have the element founded by slicing have a value property that can be displayed?
  if "_value" in sub_config:
    print("\nValue: " + str(sub_config["_value"]))
  else:
    print("\nNo valid element!")
    return False
  return True
  

# setValue()
# Used to change a value in the Config-File.
# The last element needs to describe the new value and have to match
# the value defined by the "_regex"-property.
def changeValue(path):
  # Searching for the value to be changed
  sub_config = CONFIG
  validated_input = "SET " 

  # The last element should the  
  for x in path[:-1]:
    try:
      sub_config = sub_config[x] 
      validated_input = validated_input + x + " "
    except KeyError:
      # Normally on this part there would be the autocomplete 
      # mechanismen, -> sh   a   ver     ma
      #              -> SHOW APP VERSION MAYOR
      ret = autocomplete(validated_input + x)
      if ret != False:
        validated_input = ret
      else:
        print('\n No valid element')
        return False
  

  sub_config = CONFIG # Now loading the elements.
  for vs in validated_input.split()[1:]:
    sub_config = sub_config[vs]
  
  if "_value" in sub_config:

    if "_regex" in sub_config:
      # We found a _value-Prop that can be changed
      pattern = re.compile(sub_config['_regex'])  # Compile Regex
      if pattern.match(path[-1]):
        # As defined per regex, the value is valid
        print("Old value: " + str(sub_config["_value"]))
        print("New value: " + str(path[-1]))
        sub_config["_value"] = path[-1] # Set new value
    else:
      # No regex defined, set value to whatever was provided
      print("Old value: " + str(sub_config["_value"]))
      print("New value wo/: " + str(path[-1]))
      sub_config["_value"] = path[-1] # Set new value
  else:
    print("\nNo valid element!")
    return False
  return True

if __name__ == '__main__':
  print(f'Config module')