

def oya(names):
    temp = 'try: import %s\nexcept: ...\n'
    for name in names: print(temp%name)

oya(['ctypes', 'subprocess', 'functools', 'os'])