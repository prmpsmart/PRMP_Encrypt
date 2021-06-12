
from prmp_gui import *
from tkinter.simpledialog import askstring

import random, base64, zlib


zen = """Gur Mra bs Clguba, ol Gvz Crgref

Ornhgvshy vf orggre guna htyl.
Rkcyvpvg vf orggre guna vzcyvpvg.
Fvzcyr vf orggre guna pbzcyrk.
Pbzcyrk vf orggre guna pbzcyvpngrq.
Syng vf orggre guna arfgrq.
Fcnefr vf orggre guna qrafr.
Ernqnovyvgl pbhagf.
Fcrpvny pnfrf nera'g fcrpvny rabhtu gb oernx gur ehyrf.
Nygubhtu cenpgvpnyvgl orngf chevgl.
Reebef fubhyq arire cnff fvyragyl.
Hayrff rkcyvpvgyl fvyraprq.
Va gur snpr bs nzovthvgl, ershfr gur grzcgngvba gb thrff.
Gurer fubhyq or bar -- naq cersrenoyl bayl bar --boivbhf jnl gb qb vg.
Nygubhtu gung jnl znl abg or boivbhf ng svefg hayrff lbh'er Qhgpu.
Abj vf orggre guna arire.
Nygubhtu arire vf bsgra orggre guna *evtug* abj.
Vs gur vzcyrzragngvba vf uneq gb rkcynva, vg'f n onq vqrn.
Vs gur vzcyrzragngvba vf rnfl gb rkcynva, vg znl or n tbbq vqrn.
Anzrfcnprf ner bar ubaxvat terng vqrn -- yrg'f qb zber bs gubfr!"""

class ENDE:
    def __init__(self, text, level, mode):
        self.mode = mode
        self.text = text
        self.level = level

class CryptFrame(LabelFrame):
    def __init__(self, master, _type='', command=None, **kwargs):

        text = 'Encrypt' if _type == 'en' else 'Decrypt'
        _type = 'de' if _type == 'en' else 'en'

        super().__init__(master, text=text+'ion Tab', **kwargs)

        self.desc_de = LabelLabel(self, topKwargs=dict(text=text+'ion at Level'), place=dict(relx=.02, rely=.01, relh=.07, relw=.7), orient='h', longent=.8, bottomKwargs=dict(text='1'))

        self.text = Text(self, cursor="spider", font="-family {Times New Roman} -size 12 -weight bold", insertbackground="black", relief="raised", selectbackground="#c4c4c4", selectforeground="black", undo="1", wrap="word", place=dict(relx=.011, rely=.1, relh=.815, relw=.981), highlightable=0)

        self.level = LabelCombo(self, topKwargs=dict(text='Level', relief='flat'), place=dict(relx=.021, rely=.92, relh=.07, relw=.33), orient='h', bottomKwargs=dict(foreground='white', _type='number', very=1, relief='flat', values=list(range(1,10))))

        Button(self, text=f'{_type.title()}crypt', place=dict(relx=.787, rely=.92, relh=.07, relw=.2), command=command)

    def set(self, text, level):
        self.text.set(text)
        level = int(level)
        if level < 10:
            self.level.set(level)
            self.desc_de.set(level)

    def get(self):
        level = self.level.get() or 1
        level = int(level)
        text = self.text.get()
        if level > 9:
            PRMP_MsgBox(title="Required", msg="Number must be in range 1 ... 9", _type='error', yes=dict(text='Ok'))
            return
        if not text:
            PRMP_MsgBox(title="Required", msg="Empty Text", _type='error', yes=dict(text='Ok'))
            return

        return dict(text=text, level=level)

class FileWid(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.encrypt_tab = master.master.encrypt_tab
        self.decrypt_tab = master.master.decrypt_tab

        self.path = LabelEntry(self, topKwargs=dict(text='Path->', font='PRMP_FONT', relief='flat'), place=dict(relx=0, rely=0, relh=.45, relw=.8), orient='h', longent=.13, bottomKwargs=dict(_type='path', foreground='white', very=1))

        Button(self, text='Browse', place=dict(relx=.81, rely=.05, relh=.4, relw=.17), command=self.browse)

        Button(self, text='Open', place=dict(relx=.05, rely=.5, relh=.4, relw=.1), command=self.open)
        self.mode = Checkbutton(self, text='Encrypt?', place=dict(relx=.2, rely=.5, relh=.4, relw=.1), var=1)
        self.folder = Checkbutton(self, text='Folder?', place=dict(relx=.7, rely=.5, relh=.4, relw=.1), var=1)
        Button(self, text='Save', place=dict(relx=.85, rely=.5, relh=.4, relw=.1), command=self.save)

    def browse(self):
        filetypes = PRMP_TkMixins().tkFormatedFileTypes('penc', ['penc'])
        folder = self.folder.get()
        dic = dict(filetypes=filetypes) if not folder else {}
        file = dialogFunc(path=1, folder=folder, **dic)
        self.path.set(file)

    @property
    def _path(self):
        if self.path.verify(): return self.path.get()
        else: PRMP_MsgBox(title='Error', msg='Provide a file.', _type='warn', yes=dict(text='Ok'))

    def open(self):
        if self._path:
            fileObj = PRMP_File(self._path)
            fileObj = PRMP_File(data=fileObj.decompressedData)
            obj = fileObj.loadObj()
            if obj:
                if obj.mode == 'en':
                    self.encrypt_tab.set(obj.text, obj.level)
                    self.master.master.decryptbutton()

                else:
                    self.decrypt_tab.set(obj.text, obj.level)
                    self.master.master.encryptbutton()

            else: PRMP_MsgBox(title='Error', msg='Invalid PRMP_Encrypt file.', _type='warn', yes=dict(text='Ok'))

    def save(self):
        path = self._path
        if path:
            if os.path.isdir(path):
                name = askstring('Filename', 'Enter file name without extension.')
                if not name: return
                path = os.path.join(path, name+'.penc')

            if self.mode.get():
                data = self.encrypt_tab.get()
                data['mode'] = 'en'
            else:
                data = self.decrypt_tab.get()
                data['mode'] = 'de'

            obj = ENDE(**data)
            fileObj = PRMP_File(path)
            fileObj.saveObj(obj)
            fileObj = PRMP_File(data=fileObj.compressedData)
            fileObj.save(path)

class EN_DE(Tk):
    def __init__(self, themeIndex=7, geo=(940, 700), title="Encryption Program by PRMPSmart", **kwargs):
        super().__init__(themeIndex=themeIndex, geo=geo, title=title, **kwargs)
        self.level = '1'

      #########  Decrypt Frame
        self.decrypt_tab = CryptFrame(self.container, _type='de', place=dict(relx=0, rely=0, relh=.8, relw=.5), command=self.encryptbutton)

      ########### Encrytion Tab
        self.encrypt_tab = CryptFrame(self.container, _type='en', place=dict(relx=.5, rely=.0, relh=.8, relw=.5), command=self.decryptbutton)

        self.Test = Button(self.container, text='Test', command=lambda: self.encrypt_tab.set(zen, 1), place=dict(relx=.38, rely=.07, relh=.05, relw=.1))

       ######### Frame Load from file Decrypt
        self.file_de_tab = FileWid(self.container, text='.penc File',highlightcolor="black", place=dict(relx=.021, rely=.8, relh=.19, relw=.957), font='DEFAULT_LABEL_FONT')

        self.start()

    def encryptbutton(self):
        """
        warn if encrypt level not correctly set
        get the text on Encryption_Text or Decrypted Tab
        process the text based on level
        give the level and encrypted to Decryption or Encrypted Tab
        """
        # self.status = "Encryption"
        datas = self.decrypt_tab.get()
        if not datas: return

        text = datas.get('text')
        level = datas.get('level')

        try:
            newtext = self.encode(text, level)
            self.encrypt_tab.set(newtext, level)
        except: PRMP_MsgBox(title='Encryption Error', msg='Can\'t be encrypted at this level!\nTry another level!', _type='error', bell=1, yes=dict(text='Ok'))

    def decryptbutton(self):
        """
        warn if decrypt level not correctly set
        get the text on Decryption_Text or Encrypted Tab
        process the text based on level
        give the level and decrypted to Encryption or Decrypted Tab
        """
        # self.status = "Decryption"
        datas = self.encrypt_tab.get()
        if not datas: return

        text = datas.get('text')
        level = datas.get('level')

        try:
            newtext = self.decode(text, level)
            self.decrypt_tab.set(newtext, level)
        except: PRMP_MsgBox(title='Decryption Error', msg='Can\'t be decrypted at this level!\nTry another level!', _type='error', bell=1, yes=dict(text='Ok'))

    # Writing result to file
    def en_to_file(self):
        """
        gets text from en_Text
        format it then
        calls asksaveasfilename then write the gotten text to the file
        """
        data = self.en_Text.get(0.0, "end")
        self.write_file(data)

    def de_to_file(self):
        """
        gets text from de_Text
        format it then
        calls asksavefile then write the gotten text to the file
        """
        data = self.de_Text.get(0.0, "end")
        self.write_file(data)

    def write_file(self, data):
        filename = asksaveasfilename(title="Choose file to save to or create a new one", defaultextension=".rmen", filetypes=(("Text files", "*.txt"),("Text files", "*.rmen")), confirmoverwrite=True)
        if filename:
            level = self.level
            status = self.status
            data_dict = {"status": status, "data": data, "level": level}
            self.write_to_file(filename, data_dict)


    # Reading data from file
    def en_from_file(self):
        self.status = "Encryption"
        self.show = self.en_Text
        self.read_file()

    def de_from_file(self):
        self.status = "Decryption"
        self.show = self.de_Text
        self.read_file()

    def read_file(self):
        filename = askopenfilename(title=f"Choose a file to perform {self.status}", defaultextension=".rmen", filetypes=(("Text files", "*.txt"),("Text files", "*.rmen")))
        if filename:
            if filename.endswith(".rmen") or filename.endswith(".txt"):
                data = self.read_from_file(filename)
                if len(data) == 3:
                    status = data['status']
                    level = int(data['level'])
                    text = data['data']
                    if status == 'Encryption':
                        self.encrypt_level.configure(text=level)
                        self.decrypt_level.configure(text=level)
                        self.en_Text.delete(0.0, 'end')
                        self.en_Text.insert(0.0, text)
                        decrypt = self.decode(text, level)
                        self.de_Text.delete(0.0, "end")
                        self.de_Text.insert(0.0, decrypt)
                    if status == 'Decryption':
                        self.decrypt_level.configure(text=level)
                        self.encrypt_level.configure(text=level)
                        self.de_Text.delete(0.0, 'end')
                        self.de_Text.insert(0.0, text)
                        encrypt = self.encode(text, level)
                        self.en_Text.delete(0.0, "end")
                        self.en_Text.insert(0.0, encrypt)
                else:
                    self.show.insert(0.0, data)

    # Reads from file
    def read_from_file(self, filename):
        " Reads the data from file to get the format "
        with open(filename, 'r') as f:
            data_lines = f.readlines()
            return self.read_lines(data_lines)

    #== Functions that work underground for "read_from_txt  (filename)" ==#
    def get_details(self, datalines):
        " called if 'is_formatted(datalines)' to organise the format of the data"
        top = datalines[0].split()
        status = top[0]
        level = top[-1]
        data = self.re_format(datalines[4:-1])
        return {'status': status, 'level': level, 'data': data}

    def read_lines(self, datalines):
        " Read lines of data to check if it can be automated "
        if self.is_formated(datalines):
            data_details = self.get_details(datalines)
            return data_details
        else: return self.re_format(datalines)

    def is_formated(self, datalines):
        " Confirms the if data has a format "
        if datalines[0].split()[1] == 'Level'and datalines[2]   == 'START\n' and datalines[-1] == 'END': return 1
        else: return 0

    def re_format(self, datalines):
        " called to re-organise data frome lines to full text   "
        return '\n'.join(datalines)

    #========================================================#

    # Write to file
    def write_to_file(self, filename, data_dict):
        formatted = self.signature_text(data_dict)
        with open(filename, 'w') as f: f.write(formatted)

    #=== Functions that work underground for "write_to_txt  (filename)" ===#
    def signature_text(self, data_dict):
        dd = data_dict

        level = ' Level ' + dd['level']
        start = 'START'
        end = 'END'
        nl = '\n\n'
        formats = dd['status'] + level + nl + start + nl + dd['data'] + nl + end
        return formats

    #=== function that do the actual encryption and decryption
    def space_dealer(self, text, with_space=1):
        'Deals with the insertion or removal of space " " : in the actual text'


        space=[chr(35) + chr(97) + chr(35), chr(35) + chr(97) + chr(98) + chr(35), chr(35) + chr(98) + chr(97) + chr(35), chr(35) + chr(98) + chr(35)]
        comad = chr(32)

        if with_space:
            reset = []
            for letter in text:
                if letter == comad: rep = random.choice(space)
                else: rep = letter
                reset.append(rep)
            text = ''.join(reset)
        else:
            while True:
                for on in space:
                    if on in text: text = text.replace(on,comad)
                if space[0] or space[1] or space[2] or space[3] not in text: break

        return text

    def easy_en_decode(self, text):
        'As the name entails'

        d = {}
        for c in (65, 97):
            for i in range(26): d[chr(i+c)] = chr((i+13) % 26 + c)

        easy = ''.join(d.get(c,c) for c in text)

        return easy

    def hard_en_decode(self, text):
        'As the name entails'

        f = {}
        f[chr(95)] = chr(96)
        f[chr(96)] = chr(95)
        f[chr(97)] = chr(126)
        f[chr(126)] = chr(97)

        for a in range(58, 65): f[chr(a)] = chr(a + 7) # +7
        for a in range(65, 72): f[chr(a)] = chr(a - 7) # -7
        for a in range(81, 85): f[chr(a)] = chr(a + 10) # +10
        for a in range(91, 95): f[chr(a)] = chr(a - 10) # -10
        for a in range(72, 78): f[chr(a)] = chr(a + 13) # +13
        for a in range(85, 91): f[chr(a)] = chr(a - 13) # -13
        for a in range(78, 81): f[chr(a)] = chr(a + 45) # +45
        for a in range(123, 126): f[chr(a)] = chr(a - 45) # -45
        for a in range(33,  58): f[chr(a)] = chr(a + 65) # +65
        for a in range(98,  123): f[chr(a)] = chr(a - 65) # -65

        hard = ''.join(f.get(c,c) for c in text)

        return hard

    def encode(self, text, level=1):
        'The different levels of encryptions'

        if level == 1: returnable = self.easy_en_decode(text)

        elif level == 2:
            a = self.space_dealer(text, with_space=1)
            b = self.hard_en_decode(a)
            returnable = self.easy_en_decode(b)

        elif level == 3:
            a = self.space_dealer(text)
            b = self.easy_en_decode(a)
            returnable = self.hard_en_decode(b)

        elif level == 4:
            a = self.hard_en_decode(text)
            returnable = base64.b64encode(a.encode())

        elif level == 5:
            a = self.easy_en_decode(text)
            b = self.hard_en_decode(a)
            returnable = base64.b64encode(b.encode())

        elif level == 6:
            a = self.hard_en_decode(text)
            b = self.easy_en_decode(a)
            returnable = base64.b64encode(zlib.compress(zlib.compress(b.encode())))

        elif level == 7:
            a = self.hard_en_decode(text)
            returnable = base64.b64encode(base64.b64encode(base64.b64encode(base64.b64encode(a.encode()))))

        elif level == 8: returnable = base64.b64encode(zlib.compress(text.encode()))

        elif level == 9:
            a = base64.b64encode(zlib.compress(zlib.compress(zlib.compress(text.encode()))))
            returnable = str(a)

        return str(returnable)

    def decode(self, text, level=1):
        'The different levels of encryptions'
        if isinstance(text, str) and text.startswith("b'"):
            text = text[2:-1]
            text = text.encode()

        if level == 1: returnable = self.easy_en_decode(text)

        elif level == 2:
            a = self.easy_en_decode(text)
            b = self.hard_en_decode(a)
            returnable = self.space_dealer(b, with_space=0)

        elif level == 3:
            a = self.hard_en_decode(text)
            b = self.easy_en_decode(a)
            returnable = self.space_dealer(b, with_space=False)

        elif level == 4:
            a = base64.b64decode(text)
            returnable = self.hard_en_decode(a.decode())

        elif level == 5:
            a = base64.b64decode(text)
            a = self.hard_en_decode(a.decode())
            returnable = self.easy_en_decode(a)

        elif level == 6:
            a = zlib.decompress(zlib.decompress(base64.b64decode(text)))
            b = self.easy_en_decode(a.decode())
            returnable = self.hard_en_decode(b)

        elif level == 7:
            a = base64.b64decode(base64.b64decode(base64.b64decode(base64.b64decode(text))))
            returnable = self.hard_en_decode(a.decode())

        elif level == 8: returnable = zlib.decompress(base64.b64decode(text)).decode()

        elif level == 9: returnable = zlib.decompress(zlib.decompress(zlib.decompress(base64.b64decode(text)))).decode()

        return str(returnable)

if __name__ == '__main__': EN_DE(tm=0, be=1, tipping=1)


