
import os


from prmp_lib.prmp_miscs.prmp_setup import PRMP_Setup

a = PRMP_Setup('build_ext', 'pngs.py', version='1.0')



binaries = {'app/encrypt.cp39-win_amd64.pyd': '.', 'app/prmp_gui.cp39-win_amd64.pyd': '.', 'app/prmp_miscs.cp39-win_amd64.pyd': '.'}
binaries = {}

# a = PRMP_Setup('pyinstaller', name='PRMP_Encrypt', console=1, binaries=binaries, onefile=0, icon=r'C:\Windows\System32\EhStorAuthn.exe', noconfirm=0, scripts='app/main.py')

a = PRMP_Setup('inno_setup', 'PRMP_Encrypt.iss')



# a = PRMP_Setup('build_ext', 'encrypt.py')

a.build()


# os.system(r'dist\PRMP_Encrypt1\PRMP_Encrypt_c.exe')
# os.system(r'dist\PRMP_Encrypt\PRMP_Encrypt_c.exe')
# os.system(r'dist\PRMP_Encrypt.exe')

# C:\ProgramData\Anaconda3\Scripts\cythonize prmp_images.py