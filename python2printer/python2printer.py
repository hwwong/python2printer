#!/usr/bin/env python3

# pip install pywin32

# https://stackoverflow.com/questions/49778740/how-to-arrange-return-content-in-pywin32

import sys
import time
import win32ui
import win32gui
import win32con
import win32print
import os
import datetime


class pyprinter:

    def __init__(self):
        print("Create Printer obj")
        # self.dc = object

        self.FontSize = 100
        self.FontType = "Lucida Console"
        self.FontWeight = 400

        self.PageSize = (210, 297)
        self.Origin = (105, 74.5)

        self.font = win32ui.CreateFont(
            {
                "name":  self.FontType ,
                "height": self.FontSize,
                "weight": self.FontWeight,
            })

        self.printer_name = win32print.GetDefaultPrinter()

    def EnumPrinter(self):
        handle = win32print.OpenPrinter(self.printer_name)
        win32print.GetPrinter(handle)
        win32print.ClosePrinter(handle)
        printers = []
        for p in win32print.EnumPrinters(2):
            printers.append(p[1].split(',')[0])
        return printers

    def SetActivePrinter(self, prn):
        self.printer_name = prn

    def SetPrinter(self, printer, isPortrait):
        self.printer_name = printer
        # self.printer_name = 'Microsoft Print to PDF'
        # self.printer_name = 'HP LaserJet MFP M28-M31 PCLm-S (Network)'
        self.device = win32print.OpenPrinter(printer)
        self.devmode = win32print.GetPrinter(self.device, 2)["pDevMode"]

        print('paper size:', self.devmode.PaperSize)
        # http://timgolden.me.uk/pywin32-docs/PyDEVMODE.html
        # 1 = portrait, 2 = landscape
        self.devmode.Orientation = 1 if isPortrait else 2
        self.devmode.PaperSize = 10   # A4 = 10
        # self.devmode.PaperLength = 4
        # self.devmode.PaperWidth = 4

        self.hdc = win32gui.CreateDC(
            "WINSPOOL", self.printer_name, self.devmode)
        self.dc = win32ui.CreateDCFromHandle(self.hdc)
        # self.printer_name = 'HP LaserJet MFP M28-M31 PCLm-S (Network)'
        # print(win32print.EnumPrinterDrivers())
        # dc.SetBkColor(0x000000FF)

    def CreateDoc(self, docName, pageSize, isPortrait=True):
        print("Create", docName, "Document")
        # handle = win32print.OpenPrinter(self.printer_name )

        self.SetPrinter(self.printer_name, isPortrait)
        self.PageSize = (int(2970 - pageSize[0]), int(1050 - pageSize[1]/2))

        self.Document_Name = docName
        # self.dc = win32ui.CreateDC()
        # self.dc.CreatePrinterDC(self.printer_name)
        # https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-setmapmode
        self.dc.SetMapMode(win32con.MM_LOMETRIC)
        self.dc.StartDoc(docName)
        self.dc.SetBkMode(win32con.TRANSPARENT)
        self.dc.SelectObject(self.font)
        self.pen = win32ui.CreatePen(0, 0, 0)

    def SetFontSize(self, fs):
        self.FontSize = fs
        self.SetFont(self.FontType, self.FontSize, self.FontWeight)

    def SetFontType(self, ft):
        self.FontType = ft
        self.SetFont(self.FontType, self.FontSize, self.FontWeight)

    def SetFont(self, fType, fSize, fWeight):
        self.font = win32ui.CreateFont(
            {
                "name": fType,
                "height": fSize,
                "weight": fWeight
            })
        self.dc.SelectObject(self.font)

    def EndDoc(self):
        print("End", self.Document_Name, "Document")
        self.dc.EndDoc()

    def AddPage(self):
        self.dc.StartPage()

    def EndPage(self):
        self.dc.EndPage()

    def DrawBox(self, x, y, width, height):
        x, y = self.Offset(x, y)
        self.dc.Rectangle((x, y, x + width, y - height))

    def DrawLine(self, x1, y1, x2, y2):
        x1, y1 = self.Offset(x1, y1)
        x2, y2 = self.Offset(x2, y2)
        self.dc.MoveTo(x1, y1)
        self.dc.LineTo(x2, y2)

    def Text(self, x, y, txt, frame=False):
        if frame:
            w, h = self.dc.GetTextExtent(txt)       
            self.DrawBox(x, y, w, h)

        x, y = self.Offset(x, y)
        self.dc.TextOut(x, y, txt)
       

    def GetTextSize(self,txt):
        return  self.dc.GetTextExtent(txt) 

    def Offset(self, x, y):
        x = self.PageSize[0] + x
        y = -y - self.PageSize[1]
        return x, y


if __name__ == "__main__":

    print('test')
    printer = pyprinter()
    printer.SetActivePrinter('Microsoft Print to PDF')
    printer.CreateDoc("testing", (1720, 890), False)
    printer.AddPage()

    printer.DrawBox(0, 0, *(1720, 890))
    txt = "1234567890WWWWiiiijgT^"
    printer.DrawLine(10, 10, 200, 200)
    printer.Text(100, 100, txt, True)

    printer.SetFontSize(100)
    printer.Text(100, 130, txt)
    printer.SetFontType("Arial")
    printer.Text(100, 230, str(datetime.datetime.now()), True)

    printer.EndPage()
    printer.EndDoc()

    # for x in printer.EnumPrinter():
    #     print (x)

    # https://newcenturycomputers.net/projects/pythonicwindowsprinting.html

    del printer

    os.startfile('C:\\Users\\wongh\\Desktop\\test.pdf')
