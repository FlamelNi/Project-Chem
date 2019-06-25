
import os
import platform
import random
from math import floor
from time import sleep
from time import time
from story import getStory
from story import setSubmission
from story import getObj
from pynput.keyboard import Key, Listener


class CommandError(Exception):
    def __init__(self, message):
        self.message = message

class Substance:
    def __init__(self, sub, display=''):
        self.sub = sub
        self.display = display
        if display == '':
            self.display = sub

class Mail:
    def __init__(self, title, sender, message):
        self.title = title
        self.sender = sender
        self.message = message
    def display(self):
        print(self.title + '\n')
        print('from: ' + self.sender + '\n')
        print(self.message)
    

ANSWER_CHOICE_CHAR = 30;
prevMessage = ''
cost = 0
cursor = 0

totalProcessTime = 0
lastProcessStartedAt = 0
isProcessing = False

mailInbox = []

supplyAccess = {
    'a': True,
    'b': True,
    'c': True,
    'd': True,
    'e': True
}

processTime = {
    'mov': 0,
    'mix': 0,
    'fus': 0,
    'chk': 0,
    'cst': 0,
    'del': 0
}

processRestriction = {
    'mov': False,
    'mix': False,
    'fus': False,
    'chk': False,
    'cst': False,
    'del': False
}

MIX_TABLE = [
    ['a', 'c', 'e', 'e', 'e'],
    ['', 'b', 'a', 'b', 'd'],
    ['', '', 'c', 'c', 'a'],
    ['', '', '', 'd', 'b'],
    ['', '', '', '', 'e']
]

fus_table  = [
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', '']
]

cst_table = ['', '', '', '', '']


def getSupplyAccess():
    global supplyAccess
    return supplyAccess

def setSupplyAccess(access):
    global supplyAccess
    supplyAccess = access

def newMail(m):
    global mailInbox
    mailInbox.insert(0, m)
    

def resetCost():
    global cost
    cost = 0

def resetProcessTime():
    global isProcessing
    global totalProcessTime
    isProcessing = False
    totalProcessTime = 0
    

def startProcess():
    global totalProcessTime
    global isProcessing
    global lastProcessStartedAt
    
    if totalProcessTime == 0:
        resetProcessTime()
        return
    isProcessing = True
    lastProcessStartedAt = time()
    

def displayTable(table=MIX_TABLE):
    a = 0
    print('  a b c d e f')
    print('\\------------')
    for i in table:
        print(chr(ord('a') + a), end='|')
        for j in i:
            print(j, end=' ')
            if j == '':
                print(' ', end='')
        print('')
        a = a + 1

def setUpRandomReactions():
    global fus_table
    global cst_table
    fus_table = randMixTable()
    table = ['a', 'b', 'c', 'd', 'e']
    i = 0
    while i < len(cst_table):
        index  = random.randint(0,len(table)-1)
        cst_table[i] = table[index]
        del table[index]
        i = i + 1
    

def randMixTable(regMix=False):
    mixTable = [
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', '']
    ]
    i = 0
    while i < 5:
        j = 0
        while j <= i:
            mixTable[j][i] = chr(ord('a') + random.randint(0,4))
            if regMix and i == j:
                mixTable[j][i] = chr(ord('a') + i)
            j = j + 1
        i = i + 1
    return mixTable
    
    
    
    

def readPrevMessage():
    return prevMessage

def display(m, doPrint=True):
    prevMessage = m
    if doPrint:
        print(m)

def clearScreen(arg1='', arg2=''):
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Darwin':
        os.system('clear')
    elif platform.system() == 'Linux':
        os.system('clear')

def flush():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    
def askUser(answerChoice):
    i = 1
    for c in answerChoice:
        s = '[' + str(i) + '. ' + c
        while len(s) < ANSWER_CHOICE_CHAR-1:
            s = s+' '
        print(s + ']')
        i = i + 1
    
    userInput = 0
    while userInput <= 0 or userInput > len(answerChoice):
        print('Enter:', end=' ')
        userInput = input()
        if userInput.isdigit():
            userInput = int(userInput)
        else:
            userInput = 0
            continue
    print('\n')
    return userInput

def checkArgs(arg1, arg2, i):
    if arg1 == '':
        raise CommandError('arg1 is missing')
    if i >= 2 and arg2 == '':
        raise CommandError('arg2 is missing')

SUPPLY = ['a', 'b', 'c', 'd', 'e']

CONTAINER = ['1', '2', '3', '4', '5']

container = {
    '1': Substance(''), 
    '2': Substance(''), 
    '3': Substance(''), 
    '4': Substance(''), 
    '5': Substance('')
}

def getArgType(arg):
    i = arg in SUPPLY
    if i:
        return 'SUPPLY'
    i = arg in CONTAINER
    if i:
        return 'CONTAINER'
    return 'INVALID'
def validArgType(arg):
    return getArgType(arg) != 'INVALID'

def setRestriction(action, restriction=True):
    global processRestriction
    processRestriction[action] = restriction
    
def setActionTime(action, newProcessTime=0):
    global processTime
    processTime[action] = newProcessTime

def takeAction(action):
    global processRestriction
    global totalProcessTime
    global processTime
    if processRestriction[action]:
        resetProcessTime()
        raise CommandError(action + ' is not allowed')
    totalProcessTime = totalProcessTime + processTime[action]
    
def getSubstance(pos):
    if getArgType(pos) == 'CONTAINER':
        return container[pos]
    if getArgType(pos) == 'SUPPLY':
        return Substance(pos)
    return 'INVALID'
def setSubstance(pos, sub):
    if getArgType(pos) == 'CONTAINER':
        container[pos].sub = sub.sub
        container[pos].display = sub.display
        return True
    return False
def mix(a, b, table=MIX_TABLE):
    a = ord(a) - ord('a')
    b = ord(b) - ord('a')
    if a > b:
        a = a+b
        b = a-b
        a = a-b
    if table==MIX_TABLE:
        takeAction('mix')
    return table[a][b]
def exitGame(arg1='', arg2=''):
    raise CommandError('QUIT')
def help(arg1='', arg2=''):
    print('COMMANDS:')
    for c in USEABLE_COMMANDS:
        print(c)
    for c in getUserCommand():
        print(c)
def obj(arg1='', arg2=''):
    display(getObj())
def chk(arg1, arg2=''):
    checkArgs(arg1, arg2, 1)
    if getArgType(arg1) != 'CONTAINER':
        raise CommandError('arg1 has to be in CONTAINER')
    display(getSubstance(arg1).display)
    
def removeCon(pos):
    setSubstance(pos, Substance(''))
def rev(arg1, arg2=''):#del->remove
    takeAction('del')
    checkArgs(arg1, arg2, 1)
    if getArgType(arg1) != 'CONTAINER':
        raise CommandError('arg1 has to be in CONTAINER')
    removeCon(arg1)
    
def sub(arg1, arg2=''):
    checkArgs(arg1, arg2, 1)
    if getArgType(arg1) != 'CONTAINER':
        raise CommandError('arg1 has to be in CONTAINER')
    # display('You have submitted: ')
    setSubmission(getSubstance(arg1).sub)

def mov(arg1, arg2):
    checkArgs(arg1, arg2, 2)
    if getArgType(arg2) != 'CONTAINER':
        raise CommandError('arg2 has to be in CONTAINER')
    if getSubstance(arg1).sub == '' or getSubstance(arg1) == 'INVALID':
        raise CommandError('arg1 is INVALID')
    takeAction('mov')
    m = getSubstance(arg1)
    if getSubstance(arg2).sub != '':
        m.sub = mix(getSubstance(arg1).sub, getSubstance(arg2).sub)
        m.display = m.sub
        # if getSubstance(arg1).display == 'X' or getSubstance(arg2).display == 'X':
        #     m.display = 'X'
    setSubstance(arg2, m)
    setSubstance(arg1, Substance(''))
    
def movTutorial(arg1, arg2):
    checkArgs(arg1, arg2, 2)
    if getArgType(arg2) != 'CONTAINER':
        raise CommandError('arg2 has to be in CONTAINER')
    if getSubstance(arg1).sub == '' or getSubstance(arg1) == 'INVALID':
        raise CommandError('arg1 is INVALID')
    takeAction('mov')
    if arg1 == 'a' and getArgType(arg1) == 'SUPPLY':
        arg1 = 'b'
    elif arg1 == 'b' and getArgType(arg1) == 'SUPPLY':
        arg1 = 'a'
    m = getSubstance(arg1)
    if getSubstance(arg2).sub != '':
        m.sub = mix(getSubstance(arg1).sub, getSubstance(arg2).sub)
        m.display = m.sub
        if getSubstance(arg1).display == 'X' or getSubstance(arg2).display == 'X':
            m.display = 'X'
    setSubstance(arg2, m)
    setSubstance(arg1, Substance(''))
    
def cst(arg1, arg2=''):#casting subtance then move to 5
    checkArgs(arg1, arg2, 1)
    a = getSubstance(arg1).sub
    a = ord(a) - ord('a')
    a = cst_table[a]
    takeAction('cst')
    takeAction('mov')
    if getSubstance('5').sub != '':
        a = mix(a, getSubstance('5').sub)
    a = Substance(a, 'X')
    setSubstance('5', a)
    

def fus(arg1='', arg2=''):
    if getSubstance('1').sub == '' or getSubstance('2').sub == '':
        raise CommandError('container 1 and 2 must have substance')
    takeAction('fus')
    takeAction('mov')
    fusOutcome = mix(getSubstance('1').sub, getSubstance('2').sub, fus_table)
    finalOutcome = Substance(fusOutcome)
    if getSubstance('3').sub != '':
        finalOutcome = Substance(mix(fusOutcome, getSubstance('3').sub))
    # if getSubstance('1').display == 'X' or getSubstance('2').display == 'X':
    #     finalOutcome.display = 'X'
    setSubstance('3', finalOutcome)
    setSubstance('1', Substance(''))
    setSubstance('2', Substance(''))
    

USEABLE_COMMANDS = {
    #no arg
    'clear': clearScreen,
    'cls': clearScreen,
    'fus': fus,
    'help': help,
    'obj': obj,
    'quit': exitGame,
    # one arg
    'chk': chk,
    'cst': cst,
    'del': rev,
    'sub': sub,
    # two args
    'mov': mov
}

def tutorial2MoveSet(a=False):
    global USEABLE_COMMANDS
    if a:
        USEABLE_COMMANDS['mov'] = movTutorial
    else:
        USEABLE_COMMANDS['mov'] = mov

from userCode import getUserCommand

exitCounterDisplay = False
def exitCounterDisplayListener(key):
    global exitCounterDisplay
    if key == Key.esc:
        exitCounterDisplay = True
        return False
    

def requestConsole():
    global isProcessing
    
    # if in process
    global totalProcessTime
    global lastProcessStartedAt
    if isProcessing and totalProcessTime - floor(time() - lastProcessStartedAt) > 0:
        
        showProcessCount()
        
        listener = Listener(on_press=exitCounterDisplayListener)
        listener.start()
        # 
        global exitCounterDisplay
        exitCounterDisplay = False
        nowTime = time()
        while totalProcessTime > floor(nowTime - lastProcessStartedAt):
            updateReady = False
            while not updateReady and not exitCounterDisplay:
                updateReady = ( floor(time() - nowTime) > 0 )
            nowTime = time()
            if exitCounterDisplay:
                return True
            showProcessCount()
        resetProcessTime()
        clearScreen()
        return False
        # 
    # if not in process
    print('Enter:', end=' ')
    userInput = input()
    comm = arg1 = arg2 = ''
    i = len(userInput.split())
    if i >= 1:
        comm = userInput.split()[0]
        i = i - 1
    if i >= 1:
        arg1 = userInput.split()[1]
        i = i - 1
    if i >= 1:
        arg2 = userInput.split()[2]
        i = i - 1
    
    commFunct = USEABLE_COMMANDS.get(comm, 'none')
    if commFunct == 'none':
        commFunct = getUserCommand().get(comm, 'none')
    
    if commFunct == 'none':
        print('Error: unknown command')
    else:
        try:
            resetProcessTime()
            commFunct(arg1, arg2)
            startProcess()
        except CommandError as e:
            if e.message == 'QUIT':
                return True
            display('Error: ' + e.message)
        if commFunct != clearScreen:
            print('')
    return False
    


def showProcessCount():
    clearScreen()
    nowTime = time()
    global totalProcessTime
    global lastProcessStartedAt
    timeLeft = totalProcessTime - floor(nowTime - lastProcessStartedAt)
    print('FLAMEL module is processing an action')
    print('Time left: ' + str(timeLeft))
    print('Press ESC to Exit...')
    

exitProgram = False

def consoleApplication():
    clearScreen()
    while True:
        quit = requestConsole()
        if quit:
            break
        
exitMail = False
isMailOpened = False
mailCursor = 0
startingCursor = 0
def mailApplication():
    # TODO: 
    # return False
    global mailInbox
    global mailCursor
    global exitMail
    global isMailOpened
    exitMail = False
    displayInbox = []
    # startingCursor = mailCursor
    global startingCursor
    displaySize = 6
    
    while not exitMail:
        clearScreen()
        if startingCursor + displaySize > len(mailInbox):
            startingCursor = len(mailInbox) - displaySize
        displayInbox.clear()
        i = 0
        while i < displaySize:
            displayInbox.append(mailInbox[startingCursor+i])
            i = i + 1
        i = 0
        for a in displayInbox:
            if mailCursor == i:
                print('->', end='')
            else:
                print('  ', end='')
            print(a.title)
            i = i + 1
        
        isMailOpened = False
        
        with Listener(on_press=cursorMoveMail) as listener:
            listener.join()
        flush()
        
        if mailCursor < 0:
            mailCursor = 0
            startingCursor = startingCursor - 1
        if mailCursor >= displaySize:
            mailCursor = displaySize-1
            startingCursor = startingCursor + 1
        
        if startingCursor < 0:
            startingCursor = 0
            mailCursor = 0
        if mailCursor >= len(mailInbox):
            mailCursor = len(mailInbox)-1
        
        if isMailOpened:
            openMail(mailInbox[startingCursor+mailCursor])
        
        
    

def doQuit():
    global exitProgram
    print('[Exiting the program...]')
    sleep(2)
    exitProgram = True

def waitTilEsc(key):
    if key == Key.esc:
        return False
    

def openMail(mail):
    clearScreen()
    mail.display()
    with Listener(on_press=waitTilEsc) as listener:
        listener.join()
    flush()
    

def cursorMoveMail(key):
    global mailCursor
    global isMailOpened
    global exitMail
    if key == Key.up:
        mailCursor = mailCursor - 1
        return False
    if key == Key.down:
        mailCursor = mailCursor + 1
        return False
    if key == Key.enter:
        isMailOpened = True
        return False
    if key == Key.esc:
        exitMail = True
        return False
    


menuList = {
    'console': consoleApplication,
    'mail': mailApplication,
    'quit': doQuit
}

appFunct = False

def cursorMoveMenu(key):
    global cursor
    global menuList
    global appFunct
    appFunct = False
    if key == Key.up:
        cursor = cursor - 1
        return False
    if key == Key.down:
        cursor = cursor + 1
        return False
    if key == Key.enter:
        i = 0
        for app in menuList:
            if cursor == i:
                appFunct = menuList[app]
                break
            i = i + 1
        return False

def menu():
    global cursor
    global menuList
    global exitProgram
    global appFunct
    while not exitProgram:
        clearScreen()
        i = 0
        for a in menuList:
            if cursor == i:
                print('->', end='')
            else:
                print('  ', end='')
            print(a)
            i = i + 1
        
        with Listener(on_press=cursorMoveMenu) as listener:
            listener.join()
        flush()
        if appFunct != False:
            appFunct()
        cursor = cursor%len(menuList)
    
    
    


