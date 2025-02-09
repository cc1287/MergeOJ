import ErrorHook,file
from tkinter import *
from tkinter import ttk,filedialog

class Config():
    def __init__(self,rootWindow:Tk):
        self.root=Toplevel(rootWindow)
        self.root.title('配置')
        self.root.attributes('-toolwindow',True)
        self.file=file.File('json')
        self.draw(self.file.read('\\data\\global.config.json'))
    def draw(self,configType:dict):
        i=1
        self.conf={}
        tmp=[None]
        key=list(configType.keys())
        item=list(configType.values())
        for it in range(len(key)):
            Label(self.root,text=key[it]).grid(column=0,row=i,sticky='e')
            selectType=item[it][0]
            if selectType=='string':
                tmp.append(StringVar())
                Entry(self.root,textvariable=tmp[i],width=28).grid(column=1,row=i,sticky='w')
            elif selectType=='choice':
                tmp.append(StringVar(value=str(list(item[it][1].keys())[-1])))
                OptionMenu(self.root,tmp[i],*item[it][1].keys()).grid(column=1,row=i,sticky='w')
            elif selectType=='file':
                def openFile():
                    self.open_file(list(item[it][1].items()))
                tmp.append(StringVar())
                frame=Frame(self.root)
                Entry(frame,textvariable=tmp[i]).grid(column=0,row=i)
                ttk.Button(frame,text='选择文件',command=lambda:self.open_file(list(item[self.iits][1].items())),iits=it).grid(column=1,row=i,sticky='w')
                frame.grid(column=1,row=i)
            i+=1
    def open_file(self,fileType):
        filetypes=fileType
        filetypes.append(['All files', '*.*'])
        filename = filedialog.askopenfilename(
            title='选择文件',
            filetypes=filetypes)
        return filename
    def mainloop(self):
        self.root.mainloop()
            
if __name__=='__main__':
    root=Tk()
    Config(root)
    root.mainloop()