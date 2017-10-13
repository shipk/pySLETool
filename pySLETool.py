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

        self.btnMultiply = Button(frmTop, text='Multiply from 48',  command=self.onMultiply)
        self.btnMultiply.pack(side=LEFT, padx=5, pady=5)

        self.btnMultiply1 = Button(frmTop, text='Multiply1',  command=self.onMultiply1)
        self.btnMultiply1.pack(side=LEFT, padx=5, pady=5)

        self.btnBlock = Button(frmTop, text='Block from 1..48 to 49..96',  command=self.onBlock)
        self.btnBlock.pack(side=LEFT, padx=5, pady=5)

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
    def onMultiply(self):
        s = self.st.get('1.0', END+'-1c')
        s1 = ""
        for i in range(49,96+1):
            sa = re.sub('48', str(i), s)
            s1 = s1 + sa
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s1)
    def onMultiply1(self):
        s = self.st.get('1.0', END+'-1c')
        s1 = ""
        for i in range(2,48+1):
            sa = re.sub('1', str(i), s)
            s1 = s1 + sa
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s1)
    def onBlock(self):
        s = self.st.get('1.0', END+'-1c')
        s1 = s
        for i in range(1,48+1):
            # "xx,"
            ma = re.compile(r'(.*)([^0-9])('+str(i)+'([, \)\-])(.*)', re.DOTALL)
            while True:
                mo = ma.match(s1)
                if mo is None: break
                g = mo.groups()
                #print('s1=%s groups 0=%s 1=%s 2=%s 3=%s' % (s1, g[0], g[1], g[2], g[3]))
                s1 = g[0] + g[1] + str(i+48) + g[3] +g[4]
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, s1)
    def onClear(self):
        self.st.delete('1.0', END)
    def onDestroy(self, event):
        pass

if __name__ == '__main__':
    root = Tk()
    root.title("SLETool")
    SLETool(root).mainloop()
