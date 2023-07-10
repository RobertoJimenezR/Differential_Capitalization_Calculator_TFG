import tkinter
from functools import partial


class Table(tkinter.Frame):
    def __init__(self, widget, heading, data, master=None, editablefields: list[bool] =None, readonly:bool= True):
        """Generates a Frame within the Widget widget, which contains a table of data. The table has a scrollbar subscribed to the master scroll event. You can indicate editable fields with an editable Boolean list. By default it is indicated that readonly which would prevent alado and delete data, it can be made editable with readonly = False"""

        super().__init__(widget)

        def deleterow(r, i):
            """Deletes the selected row"""
            r.destroy()
            del dic[i]
            self.dic=dic

        def addrow():
            """Add a new row"""
            frameaux = tkinter.Frame(frame)
            j = max(dic.keys()) + 1
            i = 0
            dicaux = {}
            for r in heading:
                if not editablefields is None:
                    if editablefields[i] and (not readonly):
                        dicaux[i] = tkinter.StringVar(frameaux, value=dic[0][i].get())
                        tkinter.Entry(frameaux, textvariable=dicaux[i]).grid(row=0, column=i)
                    else:
                        dicaux[i] = tkinter.StringVar(frameaux, value=dic[0][i].get())
                        tkinter.Entry(frameaux, textvariable=dicaux[i], state="readonly").grid(row=0, column=i)
                else:
                    dicaux[i] = tkinter.StringVar(frameaux, value=dic[0][i].get())
                    tkinter.Entry(frameaux, textvariable=dicaux[i], state="readonly").grid(row=0, column=i)
                dic[0][i].set("")
                i += 1

            if not readonly: tkinter.Button(frameaux, text="Eliminar", command=partial(deleterow, frameaux, j)).grid(row=0,
                                                                                                    column=i)
            dic[j] = dicaux
            frameaux.pack(side="bottom")

        def addheadings():
            """Add the table header"""
            frameh = tkinter.Frame(widget)
            i = 0
            for r in heading:
                sv = tkinter.StringVar(frameh)
                sv.set(r)
                tkinter.Entry(frameh, textvariable=sv, state="readonly").grid(row=0, column=i)
                i += 1
            frameh.pack()

        self.dic= {}
        dic = self.dic

        addheadings()


        dicaux = {}

        if (not readonly):
            frame0 = tkinter.Frame(widget)
            frameaux = tkinter.Frame(frame0)
            i = 0
            for r in heading:
                if not editablefields is None:
                    if editablefields[i]:
                        dicaux[i] = tkinter.StringVar(frameaux)
                        tkinter.Entry(frameaux, textvariable=dicaux[i]).grid(row=0, column=i)
                    else:
                        dicaux[i] = tkinter.StringVar(frameaux)
                        tkinter.Entry(frameaux, textvariable=dicaux[i], state="readonly").grid(row=0, column=i)
                else:
                    dicaux[i] = tkinter.StringVar(frameaux)
                    tkinter.Entry(frameaux, textvariable=dicaux[i], state="readonly").grid(row=0, column=i)
                i += 1
            dic[0] = dicaux

            tkinter.Button(frameaux, text="Añadir", command=addrow).grid(row=0, column=i)
            frameaux.pack()
            frame0.pack()

        canvas = tkinter.Canvas(widget)
        frame = tkinter.Frame(canvas)
        vertscroll = tkinter.Scrollbar(canvas, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=vertscroll.set)

        def on_mouse_scroll(event):
            if frame.winfo_height() > canvas.winfo_height():
                if event.delta:
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
                else:
                    canvas.yview_scroll(1 if event.num == 5 else -1, 'units')

        if not (master is None):
            master.bind('<Configure>', lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
            master.bind('<MouseWheel>', lambda event: on_mouse_scroll(event))
            master.bind('<Button-4>', lambda event: on_mouse_scroll(event))
            master.bind('<Button-5>', lambda event: on_mouse_scroll(event))

        canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        cw = canvas.create_window((0, 0), window=frame, anchor="nw", tags="cw")
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(cw, width=event.width))
        vertscroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        j = 1
        for r in data:
            frameaux = tkinter.Frame(frame)
            i = 0
            dicaux = {}
            for c in r:
                if not editablefields is None:
                    if editablefields[i] and (not readonly):
                        dicaux[i] = tkinter.StringVar(frameaux, value=c)
                        tkinter.Entry(frameaux, textvariable=dicaux[i]).grid(row=0, column=i)
                    else:
                        dicaux[i] = tkinter.StringVar(frameaux, value=c)
                        tkinter.Entry(frameaux, textvariable=dicaux[i], state="readonly").grid(row=0, column=i)
                else:
                    dicaux[i] = tkinter.StringVar(frameaux, value=c)
                    tkinter.Entry(frameaux, textvariable=dicaux[i], state="readonly").grid(row=0, column=i)
                i += 1
            if not readonly: tkinter.Button(frameaux, text="Eliminar", command=partial(deleterow, frameaux, j)).grid(row=0, column=i)
            frameaux.pack(expand=1)
            dic[j] = dicaux
            j += 1


    def getlistedited(self):
        listedited=[]
        if 0 in self.dic.keys(): del self.dic[0]

        for i in self.dic.keys():
            aux = []
            for j in self.dic[i].keys():
                aux.append(self.dic[i][j].get())
            listedited.append(aux)

        return listedited
