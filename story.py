
import gameLib

currentStory = 'prologue'
obj = ''
submission = False

def checkSubmission(arg):
    return False

def getStory():
    return currentStory

def getObj():
    return obj

def setSubmission(sub):
    check = ''
    if currentStory == 'tutorial1':
        check = 'a'
    elif currentStory == 'tutorial2':
        check = 'c'
    else:
        print('Error: setSubmission Error')
        return
    
    global submission
    submission = (sub == check)
    
def chat(chatter, message):
    print(chatter, end=': ')
    print(message)

def prologue():
    currentStory = 'prologue'
    gameLib.sleep(1)
    print('[WHITE has logged into the chat]\n')
    gameLib.sleep(2)
    chat('GREEN', 'Here you here')
    gameLib.sleep(2)
    chat('GREEN', 'What took you so long?\n')
    
    choices = [
        '...Huh?',
        'Sorry. Was fixing my internet',
        'I had to read stupid txt file'
    ]
    choice = gameLib.askUser(choices)
    
    chat('WHITE', choices[choice-1])
    gameLib.sleep(4)
    
    choices = [
        'Didn\'t I tell you, that you always must be 10 min early?',
        'THAT is unexcusable',
        'WHAT are you talking about?'
    ]
    chat('GREEN', choices[choice-1])
    gameLib.sleep(4)
    chat('GREEN', 'Do you think your intern job is a joke?')
    gameLib.sleep(4)
    chat('GREEN', 'This is why we need more professional person. Why did we even hire YOU?')
    gameLib.sleep(4)
    chat('GREEN', 'Anyways, we are busy. I need you to get into the FLAMEL machine')
    gameLib.sleep(2)
    chat('GREEN', 'Do you have the access to it?')
    
    choices = [
        'What is FLAMEL?',
        'Yes',
        'No'
    ]
    choice = gameLib.askUser(choices)
    
    chat('WHITE', choices[choice-1])
    gameLib.sleep(4)
    choices = [
        'You don\'t even know what we are doing here?',
        'Alright',
        'I\'m granting you the access right now'
    ]
    chat('GREEN', choices[choice-1])
    gameLib.sleep(4)
    chat('GREEN', 'FLAMEL is remote machine that controls a chemistry lab')
    gameLib.sleep(4)
    chat('GREEN', 'Remote machine can prevent dangerous situation caused by reactions')
    gameLib.sleep(4)
    chat('GREEN', 'Remember, the access code is to the machine is \"won\"')
    gameLib.sleep(2)
    chat('GREEN', 'I\'ll show you how to use FLAMEL once you get in')
    gameLib.sleep(4)
    chat('GREEN', 'Enter code \"obj\" to the console when you\'re in')
    gameLib.sleep(4)
    print('[GREEN has left the chat]')
    gameLib.sleep(4)
    print('[Connecting to FLAMEL]')
    gameLib.sleep(6)
    return tutorial1

def tutorial1():
    gameLib.clearScreen()
    global currentStory
    currentStory = 'tutorial1'
    global checkSubmission
    def checkSubmission(arg):
        return arg == 'a'
    
    global obj
    obj = 'This is FLAMEL console.\n'
    obj = obj + 'You will be keep using command \"obj\" to check your objective.\n'
    obj = obj + 'Now, let\'s try to access substance \"a\".\n'
    obj = obj + 'Substance a is in supply stock. You can access it by \"a\".\n'
    obj = obj + 'Let\'s try to move substance a to container 1. Do following command:\n'
    obj = obj + 'mov a 1\n\n'
    obj = obj + 'This command above means: move substance a to supply 1\n'
    obj = obj + 'Now, we have substance a in supply 1. Actually, I \"do\" need some substance a.\n'
    obj = obj + 'Hand that over to me by command:\n'
    obj = obj + 'sub 1\n\n'
    obj = obj + 'Which means: submit content inside container 1'
    obj = obj + 'Please hand me this asap.\n-Green'
    
    global submission
    submission = False
    
    while not submission:
        quit = gameLib.requestConsole()
        if quit:
            return False
    
    return False

# prologue:
# 
# tutorial 1:
# ONLY substance A
# how to OBJ
# how to MOV
# how to SUB
# = submit substance A
# 
# tutorial 2:
# ONLY substance A
#     * sometimes returns substance B
# how to CHK
# how to DEL
# = submit substance A
# 
# tutorial 3:
# ONLY substance A and B
# how to mix using MOV
# = submit substance C
# 
# tutorial 4:
# ONLY substance A and B
# how to create own commands
# 
# tutorial 5:
# access to all substances
# research opportunity
# learn mix of two result in what
# 
# work 1-1, 1-2, 1-3:
# given three random substance with random cost
# given random objective substance different from first three
# get objective substance with minimal cost
# if not, repeat
# 
# work 1-4:
# same as work 1-1 ~ 1-3, but repeat 50 times
# can be skipped
# 
# 
# tutorial 6:
# ONLY access to __ and __
# mix is PROHIBITED
#     * mixing process is dangerous, and now is illegal
#         new process FUS is safe and legal
# how to FUS
#     * fusion module is expensive and new that it is installed
#         in only container 1 and 2
#     * fusion process has its own cost
# = submit substance __
# 
# tutorial 7:
# access to all substances
# research opportunity
# learn FUS of two result in what
# 
# work 2-1, 2-2, 2-3:
# given three random substance with random cost
# given random objective substance different from first three
# get objective substance with minimal cost
# if not, repeat
# 
# work 2-4:
# DEL is unusable
#     * DEL is now very expensive to process
# same as work 1-1 ~ 1-3, but repeat 50 times
# can be skipped
# 
# tutorial 8:
# how to CST
# do CHK then submit substance X
# 
# work 3-1, 3-2, 3-3:
# given two random substances
# given substance X created by casting two substances,
#     figure out what substance X is
# = submit same substance of the X
# 
# work 3-4:
# same as 3-1 ~ 3-3, but repeat 50 times
# can be skipped






