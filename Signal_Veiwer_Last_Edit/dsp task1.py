import statistics

from PyQt5 import QtCore,QtGui,QtWidgets
from matplotlib.backends.backend_pdf import PdfPages
from PyQt5.QtWidgets import QFileDialog
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.figure import Figure
from PyPDF2 import PdfFileMerger,PdfFileReader
import pdfkit
from PyQt5 import QtWidgets,QtCore,QtGui,uic
from pyqtgraph import PlotWidget,plot
from mainwindow import Ui_MainWindow
import matplotlib.pyplot as plot
from random import randint
from threading import Timer
from scipy import signal
import pyqtgraph as pg
import pandas as pd
import numpy as np
import pathlib
import sys  # We need sys so that we can pass argv to QApplication
import os
import csv
import pyautogui
from PIL import Image

# open requirements
from PyQt5.QtWidgets import QApplication,QWidget,QInputDialog,QLineEdit,QFileDialog,QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# generate pdf
# import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
import random
import statistics
from reportlab.graphics import renderPDF
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,Table
from io import BytesIO
from svglib.svglib import svg2rlg
from fpdf import FPDF
import pyqtgraph.exporters
from PyPDF2 import PdfFileMerger,PdfFileReader
import pdfkit

list_files=[]
file_path=0


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__()
        # Load the UI Page
        uic.loadUi('mainwindow.ui',self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        # Samplingfrequency=2*Fmax
        self.samplingfrequency=300
        # Updating iterators
        self.data1=[]
        self.i_1=0
        self.l1=0
        self.data2=[]
        self.i_2=0
        self.data3=[]
        self.i_3=0

        self.figure_2=Figure()
        self.figure_canvas_2=FigureCanvas(self.figure_2)
        self.ui.verticalLayout_2.addWidget(self.figure_canvas_2)

        # Actions of open menulist
        self.ui.actionopenSignal_1.triggered.connect(self.read_data1)
        self.ui.actionopenSignal_2.triggered.connect(self.read_data2)
        self.ui.actionopenSignal_3.triggered.connect(self.read_data3)
        # Actions of open colorslist
        self.ui.actioncolorsignal1.triggered.connect(self.colorpalette1)
        self.ui.actioncolorsignal2.triggered.connect(self.colorpalette2)
        self.ui.actioncolorsignal3.triggered.connect(self.colorpalette3)

        # Actions of open spectrogramlist
        self.ui.menuspectrosignal1.triggered.connect(self.spectro1)
        self.ui.menuspectrosignal2.triggered.connect(self.spectro2)
        self.ui.menuspectrosignal3.triggered.connect(self.spectro3)
        # Actions of speed

        self.ui.actionfast.triggered.connect(self.fast)
        self.ui.actionnormal.triggered.connect(self.normal)
        self.ui.actionslow.triggered.connect(self.low)
        # Timers
        self.timer1=QtCore.QTimer()
        self.timer2=QtCore.QTimer()
        self.timer3=QtCore.QTimer()
        # pause&resume buttons
        # ch_1
        self.ui.PlayButton.clicked.connect(self.resume_1)
        self.ui.PuaseButton.clicked.connect(self.pause_1)

        # Actions for zooming in:
        self.ui.ZoominButton.clicked.connect(lambda: self.zoomin1())

        # Actions for zooming out:
        self.ui.ZoomoutButton.clicked.connect(lambda: self.zoomout1())

        # Action for Scrolling:
        self.ui.RightButton.clicked.connect(lambda: self.scroll_left1())
        self.ui.LeftButton.clicked.connect(lambda: self.scroll_right1())
        self.ui.UpButton.clicked.connect(lambda: self.scroll_down())
        self.ui.DownButton.clicked.connect(lambda: self.scroll_up())

        # Action for save:
        self.ui.actionSave.triggered.connect(self.save_pdf)

        # Action for hiding:
        self.ui.show_signal1.stateChanged.connect(lambda: self.hide1(self.data_line1))
        self.ui.show_signal2.stateChanged.connect(lambda: self.hide2(self.data_line2))
        self.ui.show_signal3.stateChanged.connect(lambda: self.hide3(self.data_line3))
        # limit of slider
        self.min_slider=0
        self.avg_slider=(5000 - 1) // 2
        self.max_slider=5000
        self.ui.horizontalSlider.setMinimum(self.min_slider)
        self.ui.horizontalSlider.setMaximum(self.avg_slider - 1)
        self.ui.horizontalSlider_2.setMinimum(self.avg_slider + 1)
        self.ui.horizontalSlider_2.setMaximum(self.max_slider)
        self.min=self.ui.horizontalSlider.value()
        self.max=self.ui.horizontalSlider_2.value()

    ####################################
    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        self.openFileNameDialog()
        self.openFileNameDialog()
        self.openFileNameDialog()
        fname=list_files[0]
        if (fname[0] != ''):
            self.read_data1()
        else:
            pass
        fname=list_files[1]
        if (fname[0] != ''):
            self.read_data2()
        else:
            pass
        fname=list_files[2]
        if (fname[0] != ''):
            self.read_data3()
        else:
            pass

    def color_picker(self):
        color=QtWidgets.QColorDialog.getColor()
        return color

    def colorpalette1(self):
        self.pen1=pg.mkPen(self.color_picker())

    def colorpalette2(self):
        self.pen2=pg.mkPen(self.color_picker())

    def colorpalette3(self):
        self.pen3=pg.mkPen(self.color_picker())
        self.pallete="viridis"
    def change_pallete(self):
        self.pallete = self.ui.comspectropallete.currentText()
        print(self.pallete)

    def openFileNameDialog(self):
        options=QtWidgets.QFileDialog.Options()
        files=QtWidgets.QFileDialog.getOpenFileName(self,'Open only txt or CSV or xls',os.getenv('HOME'),
                                                    "csv(*.csv);; text(*.txt) ;; xls(*.xls)",options = options)
        if files:
            list_files.append(files)
            print(files)
            print(list_files)

        # Loading different formatted files

    def read_data1(self):
        self.fname1=QtWidgets.QFileDialog.getOpenFileName(self,'Open only txt or CSV or xls',os.getenv('HOME'),
                                                          "csv(*.csv);; text(*.txt) ;; xls(*.xls)")
        path=self.fname1[0]
        # self.name1= self.fname1

        if pathlib.Path(path).suffix == ".txt":
            self.data1=np.genfromtxt(path,delimiter = ',')
            self.x1=self.data1[:,0]
            self.y1=self.data1[:,1]
            self.x1=list(self.x1[:])
            self.y1=list(self.y1[:])
        elif pathlib.Path(path).suffix == ".csv":
            self.data1=np.genfromtxt(path,delimiter = ' ')
            self.x1=self.data1[:,0]
            self.y1=self.data1[:,1]
            self.x1=list(self.x1[:])
            self.y1=list(self.y1[:])
        elif pathlib.Path(path).suffix == ".xls":
            self.data1=np.genfromtxt(path,delimiter = ',')
            self.x1=self.data1[:,0]
            self.y1=self.data1[:,1]
            self.x1=list(self.x1[:])
            self.y1=list(self.y1[:])

        self.channel1(self.data1)
        self.ui.label_1.setText("Signal 1")
        # self.spectro1(self.data1)

    def read_data2(self):
        fname=QtWidgets.QFileDialog.getOpenFileName(self,'Open only txt or CSV or xls',os.getenv('HOME'),
                                                    "csv(*.csv);; text(*.txt) ;; xls(*.xls)")
        path=fname[0]

        if pathlib.Path(path).suffix == ".txt":
            self.data2=np.genfromtxt(path,delimiter = ',')
            self.x2=self.data2[:,0]
            self.y2=self.data2[:,1]
            self.x2=list(self.x2[:])
            self.y2=list(self.y2[:])
        elif pathlib.Path(path).suffix == ".csv":
            self.data2=np.genfromtxt(path,delimiter = ' ')
            self.x2=self.data2[:,0]
            self.y2=self.data2[:,1]
            self.x2=list(self.x2[:])
            self.y2=list(self.y2[:])
        elif pathlib.Path(path).suffix == ".xls":
            self.data2=np.genfromtxt(path,delimiter = ',')
            self.x2=self.data2[:,0]
            self.y2=self.data2[:,1]
            self.x2=list(self.x2[:])
            self.y2=list(self.y2[:])

        self.channel2(self.data2)
        self.ui.label_2.setText("Signal 2")

    def read_data3(self):
        fname=QtWidgets.QFileDialog.getOpenFileName(self,'Open only txt or CSV or xls',os.getenv('HOME'),
                                                    "csv(*.csv);; text(*.txt) ;; xls(*.xls)")
        path=fname[0]

        if pathlib.Path(path).suffix == ".txt":
            self.data3=np.genfromtxt(path,delimiter = ',')
            self.x3=self.data3[:,0]
            self.y3=self.data3[:,1]
            self.x3=list(self.x3[:])
            self.y3=list(self.y3[:])
        elif pathlib.Path(path).suffix == ".csv":
            self.data3=np.genfromtxt(path,delimiter = ' ')
            self.x3=self.data3[:,0]
            self.y3=self.data3[:,1]
            self.x3=list(self.x3[:])
            self.y3=list(self.y3[:])
        elif pathlib.Path(path).suffix == ".xls":
            self.data3=np.genfromtxt(path,delimiter = ',')
            self.x3=self.data3[:,0]
            self.y3=self.data3[:,1]
            self.x3=list(self.x3[:])
            self.y3=list(self.y3[:])
        self.channel3(self.data3)
        self.ui.label_3.setText("Signal 3")
        # Updating plots and repeating signals

    def update_plot_data1(self,data_line,data):
        x=self.x1[:self.idx1]
        y=self.y1[:self.idx1]
        self.idx1+=10
        if self.idx1 > len(self.x1):
            self.idx1=0
        if self.x1[self.idx1] > 0.5:
            self.ui.graphicsView.setLimits(xMin = min(x,default = 0),
                                           xMax = max(x,default = 0))  # disable paning over xlimits
        self.ui.graphicsView.plotItem.setXRange(max(x,default = 0) - 0.5,max(x,default = 0))
        self.data_line1.setData(x,y)

    def update_plot_data2(self,data_line,data):
        x=self.x2[:self.idx2]
        y=self.y2[:self.idx2]
        self.idx2+=10
        if self.idx2 > len(self.x2):
            self.idx2=0
        if self.x2[self.idx2] > 0.5:
            self.ui.graphicsView.setLimits(xMin = min(x,default = 0),
                                           xMax = max(x,default = 0))  # disable paning over xlimits
        self.ui.graphicsView.plotItem.setXRange(max(x,default = 0) - 0.5,max(x,default = 0))
        self.data_line2.setData(x,y)

    def update_plot_data3(self,data_line,data):
        x=self.x3[:self.idx3]
        y=self.y3[:self.idx3]
        self.idx3+=10
        if self.idx3 > len(self.x3):
            self.idx3=0
        if self.x3[self.idx3] > 0.5:
            self.ui.graphicsView.setLimits(xMin = min(x,default = 0),
                                           xMax = max(x,default = 0))  # disable paning over xlimits

        self.ui.graphicsView.plotItem.setXRange(max(x,default = 0) - 0.5,max(x,default = 0))
        self.data_line3.setData(x,y)

        # Displaying signals

    def channel1(self,data):
        self.ui.graphicsView.setBackground('w')
        self.data_line1=self.ui.graphicsView.plot(self.x1,self.y1,pen = self.pen1)
        self.ui.graphicsView.plotItem.setLimits(xMin = 0,xMax = 12,yMin = -1,yMax = 1)
        self.idx1=0
        self.ui.graphicsView.plotItem.getViewBox().setAutoPan(x = True,y = True)
        self.timer1.setInterval(60)
        self.timer1.timeout.connect(lambda: self.update_plot_data1(self.data_line1,data))
        self.timer1.start()
        self.ui.graphicsView.show()
        self.ui.graphicsView.setXRange(0,0.002 * len(data))

    def channel2(self,data):
        self.ui.graphicsView.setBackground('w')
        self.data_line2=self.ui.graphicsView.plot(self.x2,self.y2,pen = self.pen2)
        self.ui.graphicsView.plotItem.setLimits(xMin = 0,xMax = 12,yMin = -1,yMax = 1)
        self.idx2=0
        self.ui.graphicsView.plotItem.getViewBox().setAutoPan(x = True,y = True)
        self.timer1.setInterval(60)
        self.timer1.timeout.connect(lambda: self.update_plot_data2(self.data_line2,data))
        self.timer1.start()
        self.ui.graphicsView.show()
        self.ui.graphicsView.setXRange(0,0.002 * len(data))

    def channel3(self,data):
        self.ui.graphicsView.setBackground('w')
        self.data_line3=self.ui.graphicsView.plot(self.x3,self.y3,pen = self.pen3)
        self.ui.graphicsView.plotItem.setLimits(xMin = 0,xMax = 30,yMin = -1,yMax = 1)
        self.idx3=0
        self.ui.graphicsView.plotItem.getViewBox().setAutoPan(x = True,y = True)
        self.timer1.setInterval(60)
        self.timer1.timeout.connect(lambda: self.update_plot_data3(self.data_line3,data))
        self.timer1.start()
        self.ui.graphicsView.show()
        self.ui.graphicsView.setXRange(0,0.002 * len(data))

    def hide1(self,data_line1):
        if (self.ui.show_signal1.isChecked()):
            self.data_line1.hide()
        else:
            self.data_line1.show()

    def hide2(self,data_line2):
        if (self.ui.show_signal2.isChecked()):
            self.data_line2.hide()
        else:
            self.data_line2.show()

    def hide3(self,data_line3):
        if (self.ui.show_signal3.isChecked()):
            self.data_line3.hide()
        else:
            self.data_line3.show()

    # resume&pause
    def resume_1(self):
        self.timer1.start()

        self.ui.PlayButton.setEnabled(False)
        self.ui.PuaseButton.setEnabled(True)

    def pause_1(self):
        self.timer1.stop()

        self.ui.PuaseButton.setEnabled(False)
        self.ui.PlayButton.setEnabled(True)

    def zoomin1(self):
        center_x=(self.ui.graphicsView.plotItem.getAxis("bottom").range[0] +
                  self.ui.graphicsView.plotItem.getAxis("bottom").range[1]) / 2
        center_y=0
        self.ui.graphicsView.plotItem.getViewBox().scaleBy(y = 0.9,x = 0.9,center = (center_x,center_y))

    def zoomout1(self):
        center_x=(self.ui.graphicsView.plotItem.getAxis("bottom").range[0] +
                  self.ui.graphicsView.plotItem.getAxis("bottom").range[1]) / 2
        center_y=0
        self.ui.graphicsView.plotItem.getViewBox().scaleBy(y = 1 / 0.9,x = 1 / 0.9,center = (center_x,center_y))

        # Scrolling Left,right

    def scroll_right1(self):
        self.ui.graphicsView.plotItem.getViewBox().translateBy(x = -0.2,y = 0)

    def scroll_left1(self):
        self.ui.graphicsView.plotItem.getViewBox().translateBy(x = 0.2,y = 0)

    def scroll_up(self):
        self.ui.graphicsView.plotItem.getViewBox().translateBy(x = 0,y = 0.2)

    def scroll_down(self):
        self.ui.graphicsView.plotItem.getViewBox().translateBy(x = 0,y = -0.2)

    def fast(self):
        self.timer1.setInterval(20)

    def normal(self):
        self.timer1.setInterval(60)

    def low(self):
        self.timer1.setInterval(100 * 5)

    # Signal Power density spectogram

    # Signal Power density spectogram
    def spectro1(self):
        if len(self.data1) != 0:
        # SP1=self.data1.flatten()
            y=self.y1
            ax=self.figure_2.gca()
            ax.cla()
            ax.set_xlim(y[self.min],y[self.max])
            ax.set_title("Signal 1")
            data=y[self.min: self.max]
            ax.specgram(data,NFFT = 64,Fs = 32000,Fc = None,noverlap = 24,cmap = "rainbow")
            self.figure_canvas_2.draw()
            self.figure_canvas_2.flush_events()
        else:
            ax=self.figure_2.clear()
    def spectro2(self):
        ax=self.figure_2.clear()
        if len(self.data2) != 0:
            # SP2=self.data2.flatten()
            y=self.y2
            ax=self.figure_2.gca()
            ax.cla()
            ax.set_xlim(y[self.min],y[self.max])
            ax.set_title("Signal 2")
            data=y[self.min: self.max]
            ax.specgram(data,NFFT = 130,Fs = 3200,Fc = None,noverlap = 24,cmap = "rainbow")
            self.figure_canvas_2.draw()
            self.figure_canvas_2.flush_events()
        else:
            ax=self.figure_2.clear()

    def spectro3(self):
        if len(self.data3) != 0:
            # SP3=self.data3.flatten()
            y=self.y3
            ax=self.figure_2.gca()
            ax.cla()
            ax.set_xlim(y[self.min],y[self.max])
            ax.set_title("Signal 3")
            data=y[self.min: self.max]
            ax.specgram(data,NFFT = None,Fs = self.samplingfrequency,Fc = None,cmap = "viridis")
            self.figure_canvas_2.draw()
            self.figure_canvas_2.flush_events()
        else:
            ax=self.figure_2.clear()
    def statistics(self):
        statisticspdf=canvas.Canvas('tables.pdf')
        statisticspdf.setPageSize((900,900))
        if len(self.data1) != 0:
            data_1=[['mean','standard deviation','max value','min value'],
                    [statistics.mean(self.y1),statistics.stdev(self.y1),
                     max(self.y1),
                     min(self.y1)]]
            table_1=Table(data_1,colWidths = 70 * mm,rowHeights = 20 * mm)
            table_1.setStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ('FONTSIZE',(0,0),(-1,-1),18),

                              ("ALIGN",(0,0),(-1,-1),"CENTER"),
                              ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
                              ('BOX',(0,0),(-1,-1),0.25,colors.black),])
            table_1.wrapOn(statisticspdf,900,1200)
            table_1.drawOn(statisticspdf,9 * mm,225 * mm)
        if len(self.data2) != 0:
            data_2=[['mean','standard deviation','max value','min value'],
                    [statistics.mean(self.y2),
                     statistics.stdev(self.y2),
                     max(self.y2),
                     min(self.y2)]]

            table_2=Table(data_2,colWidths = 70 * mm,rowHeights = 20 * mm)

            table_2.setStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ('FONTSIZE',(0,0),(-1,-1),18),

                              ("ALIGN",(0,0),(-1,-1),"CENTER"),
                              ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
                              ('BOX',(0,0),(-1,-1),0.25,colors.black),])

            table_2.wrapOn(statisticspdf,900,1200)
            table_2.drawOn(statisticspdf,9 * mm,165 * mm)

        if len(self.data3) != 0:
            data_3=[['mean','standard deviation','max value','min value'],
                    [statistics.mean(self.y3),
                     statistics.stdev(self.y3),
                     max(self.y3),
                     min(self.y3)]]

            table_3=Table(data_3,colWidths = 70 * mm,rowHeights = 20 * mm)

            table_3.setStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ('FONTSIZE',(0,0),(-1,-1),18),
                              ("ALIGN",(0,0),(-1,-1),"CENTER"),
                              ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
                              ('BOX',(0,0),(-1,-1),0.25,colors.black)])

            table_3.wrapOn(statisticspdf,900,1200)
            table_3.drawOn(statisticspdf,9 * mm,105 * mm)

        styles=getSampleStyleSheet()
        style=ParagraphStyle(
            name = 'Normal',
            fontSize = 18,
        )
        if len(self.data1) != 0:
            data1_text=" signal  1 "
            data1_text_style=Paragraph(data1_text,style = style)
            data1_text_style.wrapOn(statisticspdf,300 * mm,300 * mm)  # size of 'textbox' for linebreaks etc.
            data1_text_style.drawOn(statisticspdf,30 * mm,270 * mm)  # position of text / where to draw
        if len(self.data2) != 0:
            data2_text=" signal 2 "
            data2_text_style=Paragraph(data2_text,style = style)
            data2_text_style.wrapOn(statisticspdf,300 * mm,
                                    300 * mm)  # size of 'textbox' for linebreaks etc.
            data2_text_style.drawOn(statisticspdf,30 * mm,210 * mm)  # position of text / where to draw
        if len(self.data3) != 0:
            data3_text=" signal 3 "
            data3_text_style=Paragraph(data3_text,style = style)
            data3_text_style.wrapOn(statisticspdf,300 * mm,
                                    300 * mm)  # size of 'textbox' for linebreaks etc.
            data3_text_style.drawOn(statisticspdf,30 * mm,150 * mm)
            # position of text / where to draw
        statisticspdf.showPage()

        statisticspdf.save()

    def imagegraph(self):
        pdf=FPDF()
        pdf.add_page()

        exporter=pg.exporters.ImageExporter(self.ui.graphicsView.plotItem)
        exporter.parameters()['width']=250
        exporter.parameters()['height']=250
        exporter.export('fileName' + '.png')

        pdf.image('fileName' + '.png',x = None,y = None,w = 180,h = 70)

        pdf.output('image.pdf')

    def imagespectro(self):
        pdfspectro=PdfPages('./Spectro.pdf')
        pdfspectro.savefig(self.figure_2)
        pdfspectro.close()

    def save_pdf(self):
        self.statistics()
        self.imagegraph()
        self.imagespectro()
        merged_pdf=PdfFileMerger()
        merged_pdf.append(PdfFileReader('./tables.pdf','rb'))
        merged_pdf.append(PdfFileReader('./image.pdf','rb'))
        merged_pdf.append(PdfFileReader('./Spectro.pdf','rb'))
        merged_pdf.write('./Report.pdf')


def main():
    app=QtWidgets.QApplication(sys.argv)
    main=MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
