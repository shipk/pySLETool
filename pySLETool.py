from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
import re

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

        Button(frmTop, text='Clear',  command=self.onClear).pack(side=RIGHT, padx=5, pady=5)
        
        self.st = ScrolledText(frmMiddle, font=('courier', 9, 'normal'))
        self.st.pack(side=TOP, fill=BOTH, expand=YES)
    def onCommaCount(self):
        s = self.st.get('1.0', END)
        cnt = 0
        for c in s:
            if c == ',':
                cnt = cnt + 1
        showinfo("Comma count", 'Comma count is ' + str(cnt))
    def onMultiply48to4996(self):
        s = self.st.get('1.0', END+'-1c')
        s1 = ""
        for i in range(49,96+1):
            sa = re.sub('48', str(i), s)
            s1 = s1 + sa
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s1)
    def onMultiply48to0196(self):
        s = self.st.get('1.0', END+'-1c')
        s1 = ""
        for i in range(1,96+1):
            sa = re.sub('48', str(i), s)
            s1 = s1 + sa
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s1)
    def onBlock0148to4996(self):
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
        s = self.st.get('1.0', END+'-1c')
        s2 = ''
        for s1 in s.split(r';'):
            s2 = s2 + '\n' + s1
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s2)
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
    root.title("SLETool")
    SLETool(root).mainloop()
