
import os
import platform
import random
from time import sleep
from story import getStory
from story import setSubmission
from story import getObj

class CommandError(Exception):
    def __init__(self, message):
        self.message = message

class Substance:
    def __init__(self, sub, display=''):
        self.sub = sub
        self.display = display
        if display == '':
            self.display = sub

ANSWER_CHOICE_CHAR = 30;
prevMessage = ''
cost = 0

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

def resetCost():
    cost = 0

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

def display(m, doPrint=True, end=''):
    prevMessage = m
    if doPrint:
        print(m, end=end)

def clearScreen(arg1='', arg2=''):
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Darwin':
        os.system('clear')
    elif platform.system() == 'Linux':
        os.system('clear')

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
def takeAction(action):
    processTime = {
        'mov': 0
    }
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
    printCommands()
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
        if getSubstance(arg1).display == 'X' or getSubstance(arg2).display == 'X':
            m.display = 'X'
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
    
def cst(arg1, arg2=''):
    checkArgs(arg1, arg2, 1)
    a = arg1.sub
    a = ord(a) - ord('a')
    a = cst_table(a)
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
    finalOutcome = Substance(mix(fusOutcome, getSubstance('3').sub))
    if getSubstance('1').display == 'X' or getSubstance('2').display == 'X':
        finalOutcome.display = 'X'
    setSubstance('3', finalOutcome)
    setSubstance('1', Substance(''))
    setSubstance('2', Substance(''))


# sub - submit


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

def printCommands():
    print('COMMANDS:')
    for c in USEABLE_COMMANDS:
        print(c)
    for c in getUserCommand():
        print(c)
def requestConsole():
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
            commFunct(arg1, arg2)
        except CommandError as e:
            if e.message == 'QUIT':
                return True
            display('Error: ' + e.message)
        if commFunct != clearScreen:
            print('')
    return False


