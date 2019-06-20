from gameLib import clearScreen
from gameLib import fus
from gameLib import help
from gameLib import obj
from gameLib import chk
from gameLib import cst
from gameLib import rev
from gameLib import sub
from gameLib import mov

from gameLib import readPrevMessage
from gameLib import display

# readPrevMessage()
#     get previous message printed on console
#
# display(arg, doPrint=True)
#     display arg to console.
#     * display must be used so that readPrevMessage can work.
#       if regular print function is used,
#       readPrevMessage will NOT read your message
#     * if doPrint is False, then it will update
#       readPrevMessage, but not display arg to console
#
# help(arg1='', arg2='')
#     prints all possible commands
#
# chk(arg1, arg2='')
#     prints the actual substance in arg1
# 
# mov(from, to)
#     moves the substance from "from" to "to
#     avaliable "from" and  "to" are...
#         supplies:
#             a, b, c, d, e,
#         containers:
#             1, 2, 3, 4, 5
#     possible combination is:
#         supply to container
#         container to container
#     if destination container already contains a substance,
#     then two substances will MIX
#     example: a + b = c
# 
# 
# cst
# 
# fus
# 


