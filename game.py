
import gameLib
import story

gameLib.setUpRandomReactions()

# PLEASE DO NOT READ

# Code below contains save code
# If you wish to skip, please use skip code
# Do not use save code to skip


# debugging code!!
while 1:
    gameLib.requestConsole()
# story.tutorial2()
# print('FULL STOP')
# input()
# debugging code!!

def waitLoad(waitTime=0.5):
    gameLib.sleep(waitTime)
    print('.')
    gameLib.sleep(waitTime)
    print('.')
    gameLib.sleep(waitTime)
    print('.')
    gameLib.sleep(waitTime)
    print('Done!\n')

gameLib.clearScreen()
print('Loading...')
waitLoad()

gameLib.sleep(0.5)
print('Checking secure connection...')
waitLoad()
gameLib.sleep(0.5)
print('[Breach tool ready]\n')
gameLib.sleep(0.5)

print('[Please enter entry point code]')
print('Enter:', end=' ')
entry = input()

episode = ''

if entry == 'zerozerozerozero':
    episode = story.prologue
elif entry == 'won':
    episode = story.tutorial1
else:
    print('Invalid code was entered. Terminating sequence')
    episode = False

if episode != False:
    print('\nValid code was entered. Connecting to the server...')
    waitLoad()
    gameLib.sleep(2)
    gameLib.clearScreen()
while episode != False:
    episode = episode()

# gameLib.askUser(['apple', 'pear', 'banana'])

# while True:
#     gameLib.requestConsole()


# a = gameLib.randMixTable()
# gameLib.displayTable(a)
# print('')
# print(gameLib.mix('a','b', a))

