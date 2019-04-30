import _thread
from tkinter.ttk import *
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import requests
import json
import ast as ast

APPLICATION_TITLE="HTTP Request Tool"
APPLICATION_BACKGROUND="#fefefa"
LABEL_FONT=("DejaVu Sans Condensed",12)
TEXT_FONT=("DejaVu Sans Condensed",12)
REQUEST_FONT=("Consolas",12)
REQUEST_FONT_BOLD=("Consolas",12,"bold")
ERROR_COLOR="#ed2b2b"
SUCCESS_COLOR="#07c7c7"

class MainFrame:
 def __init__(self):
  root=Tk()
  root.title(APPLICATION_TITLE)
  root.iconbitmap('logo1.ico')
  self.screen_height=root.winfo_screenheight()
  self.screen_width=root.winfo_screenwidth()
  mainFrameWidth=1000
  mainFrameHeight=730-20
  onScreenX=self.screen_width/2-mainFrameWidth/2
  onScreenY=(self.screen_height-50)/2-mainFrameHeight/2
  root.geometry("%dx%d+%d+%d"%(mainFrameWidth,mainFrameHeight,onScreenX,onScreenY))
  root.config(bg=APPLICATION_BACKGROUND)
  root.grid_rowconfigure(2, weight=1)
  root.grid_rowconfigure(0, weight=1)
  Label(root,text=APPLICATION_TITLE,font=("DejaVu Sans Condensed",40),bg=APPLICATION_BACKGROUND).place(x=10,y=0,height=65,width=980)
  self.requestPanel=PanedWindow(root,bg=APPLICATION_BACKGROUND)
  self.requestPanel.place(x=10,y=65,height=350-50,width=980)
  self.responsePanel=PanedWindow(root,bg=APPLICATION_BACKGROUND)
  self.responsePanel.place(x=10,y=10+350+10,height=350-20,width=980)
  self.initRequestPanel()
  self.initResponsePanel()
  root.resizable(False, False)
  root.mainloop()

 def initRequestPanel(self):
     lm=10
     tm=10
     self.methodCaptionLabel=Label(self.requestPanel, text="METHOD",font=LABEL_FONT,fg="gray18",bg=APPLICATION_BACKGROUND)
     self.methodCaptionLabel.place(x=lm,y=tm,height=20,width= 70)
     self.schemeCaptionLabel=Label(self.requestPanel, text=" SCHEME :// HOST [ \":\" PORT ] [ PATH [ \"?\" QUERY ]] ",font=LABEL_FONT,fg="gray18",bg=APPLICATION_BACKGROUND)
     self.schemeCaptionLabel.place(x=lm+15+100,y=tm,height=20,width=390)
     self.requestPanel.option_add("*TCombobox*Listbox*Font",font.Font(family="DejaVu Sans Condensed",size=30))
     self.methodCombobox=ttk.Combobox(self.requestPanel,textvariable=StringVar(),state="readonly",font=font.Font(family="Arimo",size=14))
     self.methodCombobox['values']=("GET","POST")
     self.methodCombobox.current(0)
     self.methodCombobox.place(x=lm,y=tm+2+20,height=30,width=100)
     self.URLentry=ttk.Entry(self.requestPanel,textvariable=StringVar(),font=font.Font(family="Consolas",size=12))
     self.URLentry.place(x=lm+100+15,y=tm+2+20,height=30,width=700+15+15)
     self.sendButtonPhoto=ImageTk.PhotoImage(Image.open('send1.png'))
     self.sendButton=Button(self.requestPanel,image=self.sendButtonPhoto,background='#1c8adb',activebackground='#1c8adb',command=self.sendRequest)
     self.sendButton.place(x=lm+100+15+700+15+15+15,y=tm+2+20,height=30,width=100)
     self.bodyCaptionLabel=Label(self.requestPanel, text="BODY",font=LABEL_FONT,fg="gray18",bg=APPLICATION_BACKGROUND)
     self.bodyCaptionLabel.place(x=290+90,y=tm+2+20+30+10,height=20,width=50)
     self.headerCaptionLabel=Label(self.requestPanel, text="HEADER",font=LABEL_FONT,fg="gray18",bg=APPLICATION_BACKGROUND)
     self.headerCaptionLabel.place(x=10,y=tm+2+20+30+10,height=20,width=64)
     self.requestTextAreaPanel=PanedWindow(self.requestPanel)
     self.requestTextArea=Text(self.requestTextAreaPanel,spacing1=2,spacing3=2,font=REQUEST_FONT,padx=5,pady=2,relief="groove",border=2)
     self.requestTextAreaScrollbar_V=Scrollbar(self.requestTextAreaPanel,cursor="arrow")
     self.requestTextArea.config(yscrollcommand=self.requestTextAreaScrollbar_V.set)
     self.requestTextAreaScrollbar_V.config(command=self.requestTextArea.yview)
     self.requestTextAreaScrollbar_V.pack(side='right', fill='y')
     self.requestTextArea.pack()
     self.requestTextAreaPanel.place(x=290+90,y=tm+2+20+30+20+10,height=250-50,width=680-90)
     self.requestHeaderTextAreaPanel=PanedWindow(self.requestPanel)
     self.requestHeaderTextArea=Text(self.requestHeaderTextAreaPanel,spacing1=2,spacing3=2,font=REQUEST_FONT,padx=4,pady=2,wrap=NONE) #,relief="groove",border=2)
     self.requestHeaderTextAreaScrollbar_H=Scrollbar(self.requestHeaderTextAreaPanel,orient='horizontal',cursor="arrow")
     self.requestHeaderTextArea.config(xscrollcommand=self.requestHeaderTextAreaScrollbar_H.set)
     self.requestHeaderTextAreaScrollbar_H.config(command=self.requestHeaderTextArea.xview)
     self.requestHeaderTextAreaScrollbar_H.pack(side='bottom', fill='x')
     self.requestHeaderTextAreaScrollbar_V=Scrollbar(self.requestHeaderTextAreaPanel,cursor="arrow")
     self.requestHeaderTextArea.config(yscrollcommand=self.requestHeaderTextAreaScrollbar_V.set)
     self.requestHeaderTextAreaScrollbar_V.config(command=self.requestHeaderTextArea.yview)
     self.requestHeaderTextAreaScrollbar_V.pack(side='right', fill='y')
     self.requestHeaderTextArea.pack()
     self.requestHeaderTextAreaPanel.place(x=10,y=tm+2+20+30+20+10,height=250-50,width=260+90)
     self.requestHeaderTextArea.bind("<FocusIn>",self.handleHeader_focusIn)
     self.requestHeaderTextArea.bind("<FocusOut>",self.handleHeader_focusOut)
     self.methodCombobox.bind("<<ComboboxSelected>>",self.comboboxItemChanged)
     self.requestHeaderTextArea.tag_configure("eg", foreground="gray70")
     self.insertHeaderEg()
     self.requestTextArea.config(state="disabled")
     self.requestHeaderTextArea.config(state="disabled")
 def comboboxItemChanged(self,event=None):
     if self.methodCombobox.get()=="GET":
        self.requestTextArea.config(state="disabled")
        self.requestHeaderTextArea.config(state="disabled")
     else:
        self.requestTextArea.config(state="normal")
        self.requestHeaderTextArea.config(state="normal")
 def insertHeaderEg(self):
        self.requestHeaderTextArea.insert("end","Eg:-\n\"content-type\":\"applicatin/json\",\n\"Content-Length\" : \'13\'","eg")
 def handleHeader_focusIn(self,event=None):
        if(self.requestHeaderTextArea.get(1.0,1.2)=="Eg"):
         self.requestHeaderTextArea.delete(1.0,"end")
 def handleHeader_focusOut(self,event=None):
        if(len(self.requestHeaderTextArea.get(1.0,"end").strip())==0):
            self.insertHeaderEg()
 def initResponsePanel(self):
     self.responseLabel=Label(self.responsePanel, text="RESPONSE",font=("DejaVu Sans Condensed",30),fg="gray18",bg=APPLICATION_BACKGROUND,anchor=W,justify=LEFT)
     self.responseLabel.place(x=10,y=0,height=45,width=960)
     self.responseCodeLabel=Label(self.responsePanel,font=("DejaVu Sans Condensed",15),fg="gray18",bg=APPLICATION_BACKGROUND,anchor=SW,justify=LEFT)
     self.responseCodeLabel.place(x=10+200,y=0,height=45,width=960)
     ttk.Separator(self.responsePanel,orient="horizontal").place(x=10,y=45,height=2,width=960)
     lm=25
     tm=10
     bodyLabel=Label(self.responsePanel, text="BODY",font=LABEL_FONT,fg="gray18",bg=APPLICATION_BACKGROUND)
     bodyLabel.place(x=290+90,y=50+5,height=20,width=50)
     headerLabel=Label(self.responsePanel, text="HEADER",font=LABEL_FONT,fg="gray18",bg=APPLICATION_BACKGROUND)
     headerLabel.place(x=10,y=50+5,height=20,width=64)
     self.responseTextAreaPanel=PanedWindow(self.responsePanel)
     self.responseTextArea=Text(self.responseTextAreaPanel,spacing1=2,spacing3=2,font=TEXT_FONT,padx=5,pady=2,relief="groove",border=2)
     self.responseTextAreaScrollbar_v=Scrollbar(self.responseTextAreaPanel,cursor="arrow")
     self.responseTextArea.config(yscrollcommand=self.responseTextAreaScrollbar_v.set)
     self.responseTextAreaScrollbar_v.config(command=self.responseTextArea.yview)
     self.responseTextAreaScrollbar_v.pack(side='right', fill='y')
     self.responseTextArea.pack()
     self.responseTextAreaPanel.place(x=290+90,y=50+5+20,height=265-20,width=680-90)
     self.responseHeaderTextAreaPanel=PanedWindow(self.responsePanel)
     self.responseHeaderTextArea=Text(self.responseHeaderTextAreaPanel,spacing1=2,spacing3=2,font=TEXT_FONT,wrap=NONE,padx=4,pady=2)
     self.responseHeaderTextAreaScrollbar=Scrollbar(self.responseHeaderTextAreaPanel,orient='horizontal',cursor="arrow")
     self.responseHeaderTextArea.config(xscrollcommand=self.responseHeaderTextAreaScrollbar.set)
     self.responseHeaderTextAreaScrollbar.config(command=self.responseHeaderTextArea.xview)
     self.responseHeaderTextAreaScrollbar.pack(side='bottom', fill='x')
     self.responseHeaderTextAreaScrollbar_v=Scrollbar(self.responseHeaderTextAreaPanel,cursor="arrow")
     self.responseHeaderTextArea.config(yscrollcommand=self.responseHeaderTextAreaScrollbar_v.set)
     self.responseHeaderTextAreaScrollbar_v.config(command=self.responseHeaderTextArea.yview)
     self.responseHeaderTextAreaScrollbar_v.pack(side='right', fill='y')
     self.responseHeaderTextArea.pack()
     self.responseHeaderTextAreaPanel.place(x=10,y=50+5+20,height=265-20,width=350)
     self.responseHeaderTextArea.config(state="disabled")
     self.responseTextArea.config(state="disabled")
 def setResponseCode(self,code):
     self.responseCodeLabel.place_forget()
     code=str(code);
     if code[0]=="2":
         self.responseLabel.config(text="RESPONSE - "+code,bg=SUCCESS_COLOR)
     else:
         self.responseLabel.config(text="RESPONSE - "+code,bg=ERROR_COLOR)

 def setResponseError(self,message):
    self.responseLabel.config(text="RESPONSE",bg=ERROR_COLOR)
    self.responseCodeLabel.place(x=10+200,y=0,height=45,width=960)
    self.responseCodeLabel.config(text=message,bg=ERROR_COLOR)
 def sendRequest(self):
     method=self.methodCombobox.get()
     URL=self.URLentry.get().strip()
     if len(URL)==0:
         self.URLentry.focus()
         return
     self.responseHeaderTextArea.config(state="normal")
     self.responseTextArea.config(state="normal")
     self.responseTextArea.delete(1.0,"end")
     self.responseHeaderTextArea.delete(1.0,"end")
     r=None
     if method=="GET":
        try:
         r = requests.get(URL)
        except:
         self.setResponseError("This site can’t be reached")
         return
     if method=="POST":
        try:
         header=self.requestHeaderTextArea.get(1.0,"end").strip()
         body=self.requestTextArea.get(1.0,"end").strip()
         if header=="Eg:-\n\"content-type\":\"applicatin/json\",\n\"Content-Length\" : \'13\'":
            if len(body.strip())==0:
                self.requestTextArea.focus()
                return
                #r = requests.post(URL)
            else:
                if header.lower().find("json")>0:
                 r=requests.post(URL,data=json.loads(body))
         else:
            headers=ast.literal_eval("{"+header+"}")
            if len(body)==0:
                r = requests.post(URL,headers=headers)
            else:
                if header.lower().find("json")>0:
                 r=requests.post(URL,data=json.loads(body),headers=headers)
        except:
         self.setResponseError("Invalid header or body")
         return
     if r.headers['content-type'].lower().find("html")>0:
        self.insertHTML(str(r.text))
     elif r.headers['content-type'].lower().find("json")>0:
        self.insertJSON(str(r.text))
     else:
        self.responseTextArea.insert("end",str(r.text))
     self.insertHeader(str(r.headers))
     self.setResponseCode(str(r.status_code))
     self.responseHeaderTextArea.config(state="disabled")
     self.responseTextArea.config(state="disabled")

 def insertHeader(self,data):
     self.responseHeaderTextArea.tag_configure("name", foreground="Black" ,font=REQUEST_FONT_BOLD)
     self.responseHeaderTextArea.tag_configure("value", foreground="red4")
     length=len(data)
     i=0;
     qouteStart=-1
     qouteEnd=-1
     count=0
     while(i<length):
         if qouteStart!=-1 :
          x=qouteStart
          while qouteEnd==-1:
             qouteEnd=data.find("\'",x+1)
             x=qouteEnd
             count=0
             for j in range(qouteEnd-1,qouteStart,-1):
                 if data[j]=="\\" : count+=1
                 else : break
             if count%2!=0 : qouteEnd=-1
          if data[qouteEnd+1]==',' or data[qouteEnd+1]=='}' or data[qouteEnd+1]==',' or data[qouteEnd+1]==']':
            self.responseHeaderTextArea.insert("end",data[qouteStart:qouteEnd+1],"value")
          else:
            self.responseHeaderTextArea.insert("end",data[qouteStart:qouteEnd+1],"name")
          i=qouteEnd+1
          qouteEnd=-1
          qouteStart=-1
          continue
         if(data[i]=="{"):
          self.responseHeaderTextArea.insert("end","{\n","tag")
          i+=1
          continue;
         if(data[i]=="["):
          self.responseHeaderTextArea.insert("end","[\n","tag")
          i+=1
          continue
         if(data[i]=="}"):
          if (i+1)<length and (data[i+1]==","):
                   self.responseHeaderTextArea.insert("end","\n},\n","tag")
                   i+=2
                   continue
          if (i+1)==length or data[i+1]=="]":
              self.responseHeaderTextArea.insert("end","\n}","tag")
          else:
              self.responseHeaderTextArea.insert("end","\n}\n","tag")
          i+=1
          continue
         if(data[i]=="]"):
          if (i+1)<length and (data[i+1]==","):
           self.responseHeaderTextArea.insert("end","\n],\n","tag")
           i+=2
           continue
          self.responseHeaderTextArea.insert("end","\n]\n","tag")
          i+=1
          continue;
         if(data[i]==":"):
          self.responseHeaderTextArea.insert("end"," : ","tag")
          i+=1;
          continue
         if(data[i]==","):
          self.responseHeaderTextArea.insert("end",",\n","tag")
          i+=1
          continue
         if(data[i]==" "):
          i+=1
          continue
         if str(data[i]).isalnum()==True:
          x=data.find(",",i+1)
          self.responseHeaderTextArea.insert("end",data[i:x],"value")
          i=x
          continue
         qouteStart=data.find("\'",i)
         i+=1
 def insertHTML(self,data):
     self.responseTextArea.tag_configure("innerHTML", foreground="Black")
     self.responseTextArea.tag_configure("tag", foreground="#871280")
     self.responseTextArea.tag_configure("tagVariableName", foreground="#994500")#"red4")
     self.responseTextArea.tag_configure("tagVariableValue", foreground="#1a1aa8")#"deep sky blue")
     i=0.0;
     data=data.split("\n")
     for d in data:
         d=d.strip()
         if len(d)==0: continue
         l1=[]
         x=d.find("<")
         y=d.find(">")
         while x!=-1 and y!=-1:
             if(x!=-1 and y!=-1):
                 l1.append((x,y))
                 x=d.find("<",x+1)
                 y=d.find(">",y+1)
         x=-1
         y=-1
         x1=-1
         y1=-1
         for l in l1:
             x1=x
             y1=y
             x=l[0]
             y=l[1]
             if(x1!=-1 and y1!=-1):
                 self.responseTextArea.insert("end",d[y1+1:x],"innerHTML")
             if x1==-1:
                 self.responseTextArea.insert("end",d[:x],"innerHTML")
             line=d[x:y+1]
             i=1
             for x in line[1:]:
                 if(x==' '): i+=1
                 else: break;
             if(i>1):
                 x2=line.find(" ",i+1);
             else:
                 x2=line.find(" ");
             if(line.startswith("=",i)):
                 x=1
                 self.responseTextArea.insert("end",line[x-1:y+1],"innerHTML")
                 continue
             if(x2!=-1):
                 self.responseTextArea.insert("end",line[:x2+1],"tag")
                 line1=line[x2:len(line)-1].split("=")
                 i=1
                 for q in line1:
                     if len(q)==0: continue
                     if(i==1):
                         self.responseTextArea.insert("end",q,"tagVariableName")
                         if i!=len(line1):
                             self.responseTextArea.insert("end","=","tag")
                         i+=1
                         continue
                     if i==len(line1):
                         self.responseTextArea.insert("end",q,"tagVariableValue")
                         i+=1
                         continue

                     start=q[0]
                     if start=='\'' or start=="\"":
                         end=q.find(start,1)
                         self.responseTextArea.insert("end",q[:end+1],"tagVariableValue")
                         self.responseTextArea.insert("end"," ","tagVariableValue")
                         self.responseTextArea.insert("end",q[end+1:],"tagVariableName")
                         self.responseTextArea.insert("end","=","tagVariableName")
                     else:
                         space=q.find(" ")
                         self.responseTextArea.insert("end",q[:space+1],"tagVariableValue")
                         self.responseTextArea.insert("end"," ","tagVariableValue")
                         self.responseTextArea.insert("end",q[space+1:],"tagVariableName")
                         self.responseTextArea.insert("end","=","tagVariableName")
                     i+=1
                 self.responseTextArea.insert("end",line[len(line)-1:],"tag")
             else:
                  self.responseTextArea.insert("end",line[:],"tag")
         if(y+1<len(d)):
             self.responseTextArea.insert("end",d[y+1:]+"\n","innerHTML")
         else:
             self.responseTextArea.insert("end","\n","innerHTML")
 def insertJSON(self,data):
     self.responseTextArea.tag_configure("tag", foreground="Black" )
     self.responseTextArea.tag_configure("name", foreground="Black" ,font=REQUEST_FONT_BOLD)
     self.responseTextArea.tag_configure("value", foreground="red4")
     length=len(data)
     i=0;
     qouteStart=-1
     qouteEnd=-1
     count=0
     while(i<length):
         if qouteStart!=-1 :
          x=qouteStart
          while qouteEnd==-1:
             qouteEnd=data.find("\"",x+1)
             x=qouteEnd
             count=0
             for j in range(qouteEnd-1,qouteStart,-1):
                 if data[j]=="\\" : count+=1
                 else : break
             if count%2!=0 : qouteEnd=-1
          if data[qouteEnd+1]==',' or data[qouteEnd+1]=='}' or data[qouteEnd+1]==',' or data[qouteEnd+1]==']':
            self.responseTextArea.insert("end",data[qouteStart:qouteEnd+1],"value")
          else:
            self.responseTextArea.insert("end","  "+data[qouteStart:qouteEnd+1],"name")
          i=qouteEnd+1
          qouteEnd=-1
          qouteStart=-1
          continue
         if(data[i]=="{"):
          self.responseTextArea.insert("end","{\n","tag")
          i+=1
          continue;
         if(data[i]=="["):
          self.responseTextArea.insert("end","[\n","tag")
          i+=1
          continue
         if(data[i]=="}"):
          if (i+1)<length and (data[i+1]==","):
                   self.responseTextArea.insert("end","\n},\n","tag")
                   i+=2
                   continue
          if (i+1)==length or data[i+1]=="]":
              self.responseTextArea.insert("end","\n}","tag")
          else:
              self.responseTextArea.insert("end","\n}\n","tag")
          i+=1
          continue;
         if(data[i]=="]"):
          if (i+1)<length and (data[i+1]==","):
           self.responseTextArea.insert("end","\n],\n","tag")
           i+=2
           continue
          self.responseTextArea.insert("end","\n]\n","tag")
          i+=1
          continue;
         if(data[i]==":"):
          self.responseTextArea.insert("end"," : ","tag")
          i+=1;
          continue;
         if(data[i]==","):
          self.responseTextArea.insert("end",",\n","tag")
          i+=1
          continue
         if(data[i]==" "):
          i+=1
          continue

         if str(data[i]).isalnum()==True:
          x=data.find(",",i+1);
          self.responseTextArea.insert("end",data[i:x],"value")
          i=x;
          continue
         qouteStart=data.find("\"",i)
         i+=1



MainFrame()
