# from encrypt import *

def linux_signature_terminal(state, text, level):
    'As the name entails'

    if state == 'ENCODE': code = 'Encryption'
    elif state == 'DECODE': code = 'Decryption'
    tab = '\t' * 2
    nl = '\n' * 2
    yellow = '\033[48;5;220m'
    blue = '\033[48;5;18m'
    red = '\033[48;5;196m'
    fred = '\033[38;5;196m'
    green = '\033[48;5;46m'
    black = '\033[38;5;232m'
    white = '\033[48;5;195m'
    back = '\033[0m'

    start = '%s%s%s%s at Level %d%s.%s%s%sTo know more about the levels meet the author %s. To get the real text, it must be decrypted at the particular LEVEL it was encrypted. %s The GENERATED TEXT is between the%s %sSTART%s and%sEND%s %s%s%sSTART%s %s' %(nl, yellow, fred, code, level, back, nl, white, black,author,nl, back, red, back, red, back, nl, tab, red, back, nl)

    end = '%s%s%sEND%s %s%s%sText encryption algorithm by PRMPSmart%s%s' %(nl, tab, red, back, nl, yellow, fred, back, nl)

    front = '\033[48;5;20m %s' % start
    retext = '%s%s%s' %(blue, text, back)
    stamped = start + retext + end

    if yes: print(stamped)

def signature_terminal(state, text, level):
    'As the name entails'

    if state == 'ENCODE': code = 'Encryption'
    elif state == 'DECODE': code = 'Decryption'
    tab = '\t' * 2
    nl = '\n' * 2

    start = '%s%s at Level %d.%sTo know more about the levels meet the author %s. To get the real text, it must be decrypted at the particular LEVEL it was encrypted. %s The GENERATED TEXT is between the START and END %s%sSTART %s' %(nl, code, level, nl, author,nl, nl, tab, nl)

    end = '%s%sEND %sText encryption algorithm by PRMPSmart%s' %(nl, tab, nl, nl)

    stamped = start + text + end

    if yes: print(stamped)

yes = 1

def gateman(text, en_de, level, linux=False):
    'Routing to the Encode or Decode functions'

    if en_de:
        state = 'ENCODE'
        returnable = encode(text, level)

    else:
        state = 'DECODE'
        returnable = decode(text, level)
    sig = linux_signature_terminal if linux else signature_terminal
    sig(state, returnable, level)
    return returnable


def __linux_test():
    '''Command line tool'''
    count = 0
    while True:
        red = '\033[48;5;196m'
        back = '\033[0m'
        q = 'quit IT'
        choice = input('Do want your text hidden? >>> ')

        if 'y' in choice.lower(): word = input('Enter something >>>  \033[8m ')
        else: word = input('Enter something >>> ')

        if word == q: break
        else:
            try:
                codeds = input('\033[0m If its encode press 1 or decode press 2 >>>')
                lev = input('Enter the level >>>  ')

                level = int(lev)
                coded = int(codeds)

                if coded == 1: code = True
                elif coded == 2: code = False

                gateman(word, code, level, linux=1)
            except Exception as e:
                print(e)
                print('%sPlease follow the INSTRUCTIONS carefully%s' %(red, back))

def __test():
    '''Command line tool'''
    count = 0
    while True:
        q = 'quit IT..'

        word = input('Enter something >>> ')

        if word == q: break
        else:
            try:
                codeds = input('If its encode press 1 or decode press 2 >>>')
                lev = input('Enter the level >>>  ')

                level = int(lev)
                coded = int(codeds)

                if coded == 1: code = True
                elif coded == 2: code = False

                gateman(word, code, level)
            except Exception as e:
                print(e)
                print('Please follow the INSTRUCTIONS carefully')

def __maintest2(s):
    en_de = 8
    for a in range(7): gateman(s, en_de, a+1)


# __test()



