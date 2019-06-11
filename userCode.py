
import userCommLib

# You may only import userCommLib

# You may create your own functions that you can call on console
# userCommand is string-function dictionary where
#   key is name of your command and value being the function

# Make sure that your function has two parameters.
# If your function use less than two parameters,
#   please set default values for them

# Here is an example command:
def sayHelloTo(name, arg2=''):
    userCommLib.display('Hello, ' + str(name))

# +++++++ CODE HERE +++++++



# +++++++++++++++++++++++++

userCommand = {'hi': sayHelloTo}

# This function is required so that game library can
#       read userCommand

def getUserCommand():
    return userCommand
