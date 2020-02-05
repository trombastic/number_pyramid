#!/usr/bin/python3

# -*- coding: utf-8 -*-
""" A Number Pyramid math trainer written in Python
"""
__author__ = "Martin Schröder"
__copyright__ = "Copyright 2020, Martin Schröder"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Martin Schröder"
__email__ = "info@martin-schroeder.net"
__status__ = "Alpha"
__docformat__ = 'reStructuredText'

try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
    from tkinter import ttk
except ImportError:
    raise ModuleNotFoundError

from random import random
import sys
from time import time


DEBUG = False
FONT = ("Helvetica", 35)
STRINGS = {
    "DE": {"TITLE":"Zahlenmauer","NEW":"Neu", "OK":"OK"},
    "EN": {"TITLE":"Number Pyramid","NEW":"New", "OK":"OK"}
}
LANG = "DE"

class App(object):
    """

    """
    frame = None
    id = 0
    brick_rows = 3
    nrange = 5
    e = {}
    result = False
    start_time = None
    def __init__(self, master, brick_rows=None,nrange=None):
        self.master = master
        self.frame = Frame(master)
        self.master.winfo_toplevel().title(STRINGS[LANG]["TITLE"])
        self.submit = Button (self.frame, text=STRINGS[LANG]["OK"], command=self.submit_callback, font=FONT)
        self.submit.bind('<Return>',self.submit_callback)
        self.new = Button (self.frame, text=STRINGS[LANG]["NEW"], command=self.new_exercise, font=FONT)
        self.new.bind('<Return>',self.new_exercise)
        if brick_rows is not None:
            self.brick_rows = brick_rows
        if nrange is not None:
            self.nrange = nrange

        self.frame.pack()
        self.new_exercise()
        self.submit.grid(row=self.brick_rows+1, column=0, columnspan=self.brick_rows,sticky="NWSE")
        self.new.grid(row=self.brick_rows+1, column=self.brick_rows, columnspan=self.brick_rows,sticky="NWSE")
        self.update_title()

    def submit_callback(self, event=None):
        """
        callback for submit and check result
        """
        result = {}
        prev_value = None
        OK = True
        if self.result:
            return
        for row in range(self.brick_rows,-1,-1):
            prev_value = None
            for col in range(row-1,-1,-1):
                value = self.e["%d_%d"%(row,col)].get()
                if prev_value is not None and value.isdigit() and prev_value.isdigit():
                    result["%d_%d"%(row-1,col)] = int(prev_value) + int(value)
                prev_value = value
                if "%d_%d"%(row,col) in result:
                    if value.isdigit():
                        if int(result["%d_%d"%(row,col)]) == int(value):
                            self.e["%d_%d"%(row,col)].config({"background": "White"})
                        else:
                            OK = False
                            self.e["%d_%d"%(row,col)].config({"background": "Red"})
                    else:
                        OK = False
                        self.e["%d_%d"%(row,col)].config({"background": "Red"})
                        if DEBUG:
                            print('col %d, row %d: %s = %s'%(row,col,value, result["%d_%d"%(row,col)]))
                else:
                    if DEBUG:
                        print('col %d, row %d: %s'%(row,col,value))
        if OK:
            self.result = True
            print('%d[0-%d]: %1.0fs'%(self.brick_rows, self.nrange, time()-self.start_time))
            self.start_time = None
            for row in range(self.brick_rows-1,0,-1):
                for col in range(row):
                    self.e["%d_%d"%(row,col)].config({"background": "Green"})

    @staticmethod
    def entry_fokus_in(event):
        """ clears the ? when an entry gets focus
        """
        if not event.widget.get().isdigit():
            event.widget.delete(0, END)

    def update_title(self):
        """
        """
        self.frame.after(500, self.update_title)
        if self.start_time is None or self.result:
            return
        else:
            self.master.winfo_toplevel().title('%s (%1.0fs)'%(STRINGS[LANG]["TITLE"],time()-self.start_time))

    @staticmethod
    def get_row_col(event):
        cr = event.widget.name.split('_')
        return int(cr[0]), int(cr[1])

    def left_callback(self, event):
        row, col = self.get_row_col(event)
        if '%d_%d'%(row,col-1) in self.e:
            self.e['%d_%d'%(row,col-1)].focus()

    def right_callback(self, event):
        row, col = self.get_row_col(event)
        if '%d_%d'%(row,col+1) in self.e:
            self.e['%d_%d'%(row,col+1)].focus()

    def up_callback(self, event):
        row, col = self.get_row_col(event)
        if '%d_%d'%(row-1,col) in self.e:
            self.e['%d_%d'%(row-1,col)].focus()
        if '%d_%d'%(row-1,col-1) in self.e:
            self.e['%d_%d'%(row-1,col-1)].focus()

    def down_callback(self, event):
        row, col = self.get_row_col(event)
        if '%d_%d'%(row+1,col) in self.e:
            self.e['%d_%d'%(row+1,col)].focus()

    def new_exercise(self, event=None):
        """create a new exercise
        """
        for item in self.e.values():
            item.destroy()
        self.e = {}
        coloffset = self.brick_rows
        for row in range(self.brick_rows+1):
            for col in range(row):
                self.e["%d_%d"%(row,col)] = Entry(self.frame, justify='center', width=4, font=FONT)
                setattr(self.e["%d_%d"%(row,col)],'name',"%d_%d"%(row,col))
                self.e["%d_%d"%(row,col)].bind("<FocusIn>",self.entry_fokus_in)
                self.e["%d_%d"%(row,col)].bind('<Return>',self.submit_callback)
                self.e["%d_%d"%(row,col)].bind('<Left>',self.left_callback)
                self.e["%d_%d"%(row,col)].bind('<Right>',self.right_callback)
                self.e["%d_%d"%(row,col)].bind('<Up>',self.up_callback)
                self.e["%d_%d"%(row,col)].bind('<Down>',self.down_callback)
                self.e["%d_%d"%(row,col)].delete(0, END)
                if row == self.brick_rows:
                    # last Row, add numbers
                    self.e["%d_%d"%(row,col)].insert(0, "%d"%self.random_number())
                    self.e["%d_%d"%(row,col)].config(state='readonly')
                else:
                    self.e["%d_%d"%(row,col)].insert(0, "?")

                self.e["%d_%d"%(row,col)].grid(row=row, column=coloffset+col*2,columnspan=2)
                if DEBUG:
                    print('col %d, row %d'%(col,row))
            coloffset -= 1
        # change tab order
        if DEBUG:
            print(self.e.keys())
        for row in range(self.brick_rows,-1,-1):
            for col in range(row):
                self.e["%d_%d"%(row,col)].lift()
        self.e["%d_%d"%(self.brick_rows-1,0)].focus()
        self.start_time = time()
        self.result = False

    def random_number(self):
        return int(random()*self.nrange)


if __name__ == "__main__":
    """
    the main code block
    """
    root = Tk()  # Tk()
    if len(sys.argv) == 1:
        App(root)
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['-h','--help']:
            print("""number pyramid math trainer
Usage: number_pyramid.py [rows number_range]

rows:           number of brick rows

number_range:   range of numbers for the bottom row [0 to number_range]
            """)
            sys.exit(0)
        App(root, brick_rows=int(sys.argv[1])) # rows
    elif len(sys.argv) >= 2:
        App(root, brick_rows=int(sys.argv[1]), nrange=int(sys.argv[2]))
    root.mainloop()
    sys.exit(0)