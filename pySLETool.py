from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
import re
import os

class StatusBar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._lblState = Label(self, text='', bd=2, relief=SUNKEN, width=15, anchor = W)
        self._lblState.pack(side=LEFT)

class SLETool(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(side=TOP, fill=BOTH, expand=YES)
        self.iniCtrls()
        self.bind("<Destroy>", self.onDestroy)
    def iniCtrls(self):
        frmTop = Frame(self)
        frmTop.pack(side=TOP, fill=X)
        
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=BOTTOM, fill=X)
        self.status_bar.config(bd=2, relief=SUNKEN)

        frmMiddle = Frame(self)
        frmMiddle.pack(fill=BOTH, expand=YES)

        self.btnCommaCount = Button(frmTop, text='Comma count',  command=self.onCommaCount)
        self.btnCommaCount.pack(side=LEFT, padx=5, pady=5)

        self.btnMultiply48to4996 = Button(frmTop, text='Multiply from 48 to 49..96',  command=self.onMultiply48to4996)
        self.btnMultiply48to4996.pack(side=LEFT, padx=5, pady=5)

        self.btnMultiply48to0196 = Button(frmTop, text='Multiply from 48 to 1..96',  command=self.onMultiply48to0196)
        self.btnMultiply48to0196.pack(side=LEFT, padx=5, pady=5)

        self.btnBlock0148to4996 = Button(frmTop, text='Block from 1..48 to 49..96',  command=self.onBlock0148to4996)
        self.btnBlock0148to4996.pack(side=LEFT, padx=5, pady=5)

        self.btnBlock3340to4148 = Button(frmTop, text='Block from 33..40 to 41..48',  command=self.onBlock3340to4148)
        self.btnBlock3340to4148.pack(side=LEFT, padx=5, pady=5)

        self.btnSplit = Button(frmTop, text='Split',  command=self.onSplit)
        self.btnSplit.pack(side=LEFT, padx=5, pady=5)

        self.btnSubst = Button(frmTop, text='Subst',  command=self.onSubst)
        self.btnSubst.pack(side=LEFT, padx=5, pady=5)

        self.btnScript = Button(frmTop, text='Script',  command=self.onScript)
        self.btnScript.pack(side=LEFT, padx=5, pady=5)

        Button(frmTop, text='Clear',  command=self.onClear).pack(side=RIGHT, padx=5, pady=5)
        
        self.st = ScrolledText(frmMiddle, font=('courier', 9, 'normal'))
        self.st.pack(side=TOP, fill=BOTH, expand=YES)
    def onCommaCount(self):
        """
        Подсчёт количества запятых в тексте
        """
        s = self.st.get('1.0', END)
        cnt = 0
        for c in s:
            if c == ',':
                cnt = cnt + 1
        showinfo("Comma count", 'Comma count is ' + str(cnt))
    def onMultiply48to4996(self):
        """
        Умножение блока текста с номером 48 до текста с номерами от 49 до 96
        """
        s = self.st.get('1.0', END+'-1c')
        s1 = ""
        for i in range(49,96+1):
            sa = re.sub('48', str(i), s)
            s1 = s1 + sa
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s1)
    def onMultiply48to0196(self):
        """
        Умножение блока текста с номером 48 до текста с номерами от 1 до 96
        """
        s = self.st.get('1.0', END+'-1c')
        s1 = ""
        for i in range(1,96+1):
            sa = re.sub('48', str(i), s)
            s1 = s1 + sa
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s1)
    def onBlock0148to4996(self):
        """
        Замена в блоке текста номеров с 1 по 48 на номера с 49 до 96
        """
        s1 = self.st.get('1.0', END+'-1c')
        for i in range(1,48+1):
            # "xx,", "xx ", "xx)", "xx-"
            ma = re.compile(r'(.*)([^0-9])('+str(i)+')([^0-9])(.*)', re.DOTALL)
            while True:
                mo = ma.match(s1)
                if mo is None: break
                g = mo.groups()
                #print('s1=%s groups 0=%s 1=%s 2=%s 3=%s' % (s1, g[0], g[1], g[2], g[3]))
                s1 = g[0] + g[1] + str(i+48) + g[3] +g[4]
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s1)
    def onBlock3340to4148(self):
        """
        Замена в блоке текста номеров с 33 по 40 на номера с 41 до 48
        """
        s1 = self.st.get('1.0', END+'-1c')
        for i in range(33,40+1):
            # "xx,", "xx ", "xx)", "xx-"
            ma = re.compile(r'(.*)([^0-9])('+str(i)+')([^0-9])(.*)', re.DOTALL)
            while True:
                mo = ma.match(s1)
                if mo is None: break
                g = mo.groups()
                #print('s1=%s groups 0=%s 1=%s 2=%s 3=%s' % (s1, g[0], g[1], g[2], g[3]))
                s1 = g[0] + g[1] + str(i+8) + g[3] +g[4]
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s1)
    def onSplit(self):
        """
        Заготовка для разбиения длинной строки на строки по 5 позиций
        """
        s = self.st.get('1.0', END+'-1c')
        ma = re.compile(r'^( *)(.*)')
        mo = ma.match(s)
        s_ident = ''
        s_text = s
        if not mo is None:
            g = mo.groups()
            s_ident = g[0]
            s_text = g[1]
        s_res = ''
        """
        while True:
            for i in range(1, s_text.len()):
                cnt = 0
                if s_text[i] == '+':
                    cnt = cnt + 1
                if cnt mod 5 == 0:
                    s_res = s_res + s_text[:i]
                    s_text = s_text[i:]
                    break
        """
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s_ident + s_res)
    def onSubst(self):
        """
        Разбиение строки с разделителем ";" на отдельные строки
        """
        s = self.st.get('1.0', END+'-1c')
        s2 = ''
        for s1 in s.split(r';'):
            s2 = s2 + '\n' + s1
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s2)
    def onScript(self):
        """
        Генерация SQLPLUS скрипта для наката на БД по каталогу с объектами (в рамках проекта по расширению услуг)
        """
        def t_dir(dname, lname):
            def t_file(name):
                s = ''
                s = s + 'prompt\n'
                s = s + 'prompt Exec ' + name + '\n'
                s = s + 'prompt ===========================\n'
                s = s + '@@' + server_name + '\\' + schema_name + '\\' + name + '\n'
                return s
            def t_ext(ext):
                names = [fname for fname in os.listdir(dname) if (os.path.isfile(os.path.join(dname, fname)) and fname.endswith('.' + ext))]
                s = ''
                for x in names:
                    s = s + t_file(x) + '\n'
                return s
            
            s = ''
            s = s + 'set define off\n'
            s = s + 'spool ' + lname + '\n'
            s = s + '\n'
            s = s + t_ext('tab')
            s = s + t_ext('vw')
            s = s + t_ext('mv')
            s = s + t_ext('sql') # Тоже с view
            s = s + t_ext('tps')
            s = s + t_ext('trg')
            s = s + t_ext('fnc')
            s = s + t_ext('prc')
            s = s + t_ext('pck')
            s = s + 'prompt All done.\n'
            s = s + '\n'
            s = s + 'spool off\n'
            s = s + '\n'
            return s

        root_name = r'C:\Users\KSHIPKOV\Documents\SVN\HS\Materials\Source code\Oracle\48to96\Output'
        s = ''
        server_names = [sname for sname in os.listdir(root_name) if os.path.isdir(os.path.join(root_name, sname))] 
        for server_name in server_names:
            schema_names = [sname for sname in os.listdir(os.path.join(root_name, server_name)) if os.path.isdir(os.path.join(root_name, server_name, sname))] 
            for schema_name in schema_names:
                s = s + 'file: ' + server_name + '_' + schema_name + '.sql\n'
                lname = server_name + '_' + schema_name + '.log'
                dname = os.path.join(root_name, server_name, schema_name)
                s = s + t_dir(dname, lname)

        self.st.insert(END, s)
    def onSubst1(self):
        s = self.st.get('1.0', END+'-1c')
        sr = ''
        ma = re.compile(r'(.*), nach([0-9]*),(.*)')
        for s1 in s.split('\n'):
            mo = ma.match(s1)
            if not mo is None: 
                g = mo.groups()
                s2 = g[0] + ', nullif(nach' + g[1] + ',0) nach' + g[1] + ','+ g[2]
            else:
                s2 = s1
            sr = sr + s2 + '\n'
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, sr)
    def onClear(self):
        self.st.delete('1.0', END)
    def onDestroy(self, event):
        pass

if __name__ == '__main__':
    root = Tk()
    root.title("SLETool1")
    SLETool(root).mainloop()
