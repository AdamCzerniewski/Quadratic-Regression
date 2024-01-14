#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 20:37:23 2023

@author: coco
"""
import array

from sympy import * 

import sys
from ui import Ui_MainWindow
from PyQt5 import QtCore as qtc
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5 import QtWidgets  as qtw
from PyQt5.QtGui import QColor


import os
import pyqtgraph as pg
import math
import numpy as np
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg



class Main(qtw.QMainWindow):
    
    def __init__(self):
        
        super(Main,self).__init__()
        self.port="none"
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        # call functions when the user clicks a button in the GUI
        self.ui.btn_enterParams.clicked.connect(self.organizeValues)
        self.ui.btn_enterParams.clicked.connect(self.calcValues)
        self.ui.btn_enterMatrix.clicked.connect(self.matrixForm)
        
        self.ui.btn_clearParams.clicked.connect(self.clearParams)
        self.ui.btn_clearMatrix.clicked.connect(self.clearMatrix)
        self.ui.btn_clearRREF.clicked.connect(self.clearRREF)       
        
    
    # clears all data from the Params groupbox
    def clearParams(self):
        self.ui.tf_pointA_x.setText("")
        self.ui.tf_pointB_x.setText("")
        self.ui.tf_pointC_x.setText("")
        
        self.ui.tf_pointA_y.setText("")
        self.ui.tf_pointB_y.setText("")
        self.ui.tf_pointC_y.setText("")

    # clears all data from the Matrix groupbox
    def clearMatrix(self):
        self.ui.tf_matrix_sqrdx1.setText("")
        self.ui.tf_matrix_sqrdx2.setText("")
        self.ui.tf_matrix_sqrdx3.setText("")
        
        self.ui.tf_matrix_x1.setText("")
        self.ui.tf_matrix_x2.setText("")
        self.ui.tf_matrix_x3.setText("")
        
        self.ui.tf_matrix_c1.setText("")
        self.ui.tf_matrix_c2.setText("")
        self.ui.tf_matrix_c3.setText("")
        
        self.ui.tf_matrix_y1.setText("")
        self.ui.tf_matrix_y2.setText("")
        self.ui.tf_matrix_y3.setText("")

    # clears all data from the RREF groupbox
    def clearRREF(self):
        self.ui.tf_RREF_a1.setText("")
        self.ui.tf_RREF_a2.setText("")
        self.ui.tf_RREF_a3.setText("")
        
        self.ui.tf_RREF_b1.setText("")
        self.ui.tf_RREF_b2.setText("")
        self.ui.tf_RREF_b3.setText("")
        
        self.ui.tf_RREF_c1.setText("")
        self.ui.tf_RREF_c2.setText("")
        self.ui.tf_RREF_c3.setText("")
        
        self.ui.tf_RREF_val1.setText("")
        self.ui.tf_RREF_val2.setText("")
        self.ui.tf_RREF_val3.setText("")
        
        self.ui.tf_a.setText("")
        self.ui.tf_b.setText("")
        self.ui.tf_c.setText("")
        
        self.ui.tf_equation.setText("")
    
    # takes values from the each groupbox and 'prepares' it for the calcValues() function
    def organizeValues(self):
        
        pointA_x = self.ui.tf_pointA_x.text() ; pointA_y = self.ui.tf_pointA_y.text()
        pointB_x = self.ui.tf_pointB_x.text() ; pointB_y = self.ui.tf_pointB_y.text()
        pointC_x = self.ui.tf_pointC_x.text() ; pointC_y = self.ui.tf_pointC_y.text()
        
        # Convert data to numbers
        self.x1 = float(pointA_x) ; self.y1 = float(pointA_y)
        self.x2 = float(pointB_x) ; self.y2 = float(pointB_y)
        self.x3 = float(pointC_x) ; self.y3 = float(pointC_y)
        
        self.sqrdx1 = self.x1**2
        self.sqrdx2 = self.x2**2
        self.sqrdx3 = self.x3**2
        
        self.matrix = Matrix([[self.sqrdx1, self.x1, 1, self.y1], [self.sqrdx2, self.x2, 1, self.y2], [self.sqrdx3, self.x3, 1, self.y3]])
        
        print(self.matrix)

        values_rref = self.matrix.rref()[0]
        print(values_rref)
        
        # values_simplified = nsimplify(values_rref) 
        
        # print(values_simplified)
        
        self.A = values_rref[0,3]
        self.B = values_rref[1,3]
        self.C = values_rref[2,3]
        
        print("a =", self.A)
        print("b =", self.B)   
        print("c =", self.C)   
        
        self.matrixForm()
 
    # calculates values to graph
    def calcValues(self):
        
        self.a = float(self.A)
        self.b = float(self.B)
        self.c = float(self.C)        
        
        # Array contains x values from -10 to 10, once inputted in the linear function, it will output the y values
        self.x = [-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10]
        self.y = [] # y values will be calculated and appended to this array
        
        # Loop goes through each x value in the array and calculates the output
        for i in range(len(self.x)):
            y = float(self.a) * float(self.a) * self.x[i] * self.x[i] + self.b * self.x[i] + self.c # Calculate
            
            self.y.append(y) # Appends the calculated y values to the array
         
        # Debugs
        print("x values =",self.x)
        print("y values =",self.y)           
        
        self.graphFunction(self.x, self.y)

    # called by calcValues() and is given values to graph       
    def graphFunction(self, xValues, yValues):
        self.ui.wgt1.clear()  
        
        penCustomized = pg.mkPen(color = 'white', width = 1.5)  
        
        self.ui.wgt1.plot(xValues, yValues, pen = penCustomized)
        
        self.ui.wgt1.showGrid(x = True, y = True)
        self.ui.wgt1.setLabel('left', 'Y axis')
        self.ui.wgt1.setLabel('bottom', 'X axis')
    
    
    def matrixForm(self):
        
        if self.sqrdx1 == 0:
            self.ui.tf_matrix_sqrdx1.setText("0")
        else:
            self.sqrdx1 = str(self.sqrdx1).rstrip('0').rstrip('.')
            self.ui.tf_matrix_sqrdx1.setText(str(self.sqrdx1))
        
        
        if self.x1 == 0:
            self.ui.tf_matrix_x1.setText("0")
        else:
            self.x1 = str(self.x1).rstrip('0').rstrip('.')
            self.ui.tf_matrix_x1.setText(str(self.x1))
         

        if self.y1 == 0:
            self.ui.tf_matrix_y1.setText("0")
        else:
            self.y1 = str(self.y1).rstrip('0').rstrip('.')
            self.ui.tf_matrix_y1.setText(str(self.y1))      
        
        
        if self.sqrdx2 == 0:
            self.ui.tf_matrix_sqrdx2.setText("0")
        else:
            self.sqrdx2 = str(self.sqrdx2).rstrip('0').rstrip('.')
            self.ui.tf_matrix_sqrdx2.setText(str(self.sqrdx2))
        
        
        if self.x2 == 0:
            self.ui.tf_matrix_x2.setText("0")
        else:
            self.x2 = str(self.x2).rstrip('0').rstrip('.')
            self.ui.tf_matrix_x2.setText(str(self.x2))
         

        if self.y2 == 0:
            self.ui.tf_matrix_y2.setText("0")
        else:
            self.y2 = str(self.y2).rstrip('0').rstrip('.')
            self.ui.tf_matrix_y2.setText(str(self.y2))      
        
        
        if self.sqrdx3 == 0:
            self.ui.tf_matrix_sqrdx3.setText("0")
        else:
            self.sqrdx3 = str(self.sqrdx3).rstrip('0').rstrip('.')
            self.ui.tf_matrix_sqrdx3.setText(str(self.sqrdx3))
        
        
        if self.x3 == 0:
            self.ui.tf_matrix_x3.setText("0")
        else:
            self.x3 = str(self.x3).rstrip('0').rstrip('.')
            self.ui.tf_matrix_x3.setText(str(self.x3))
         

        if self.y3 == 0:
            self.ui.tf_matrix_y3.setText("0")
        else:
            self.y3 = str(self.y3).rstrip('0').rstrip('.')
            self.ui.tf_matrix_y3.setText(str(self.y3))      
        
        
        self.ui.tf_matrix_c1.setText("1")
        self.ui.tf_matrix_c2.setText("1")
        self.ui.tf_matrix_c3.setText("1")

        
        self.rrefForm()
        
    
    def rrefForm(self):
        
        if self.a == 0:
            self.ui.tf_RREF_val1.setText("0")
            self.ui.tf_a.setText("0")
            self.a_equation = ""
            
        else:
            self.a = str(self.a).rstrip('0').rstrip('.')
            self.ui.tf_RREF_val1.setText(self.a)
            
            self.ui.tf_a.setText(self.a)
            self.a_equation = str(self.a)
        
        
        if self.b == 0:
            self.ui.tf_RREF_val2.setText("0")
            self.ui.tf_b.setText("0")
            self.b_equation = ""
            
        else:
            self.b = str(self.b).rstrip('0').rstrip('.')
            self.ui.tf_RREF_val2.setText(self.b)
 
            self.ui.tf_b.setText(self.b)
            self.b_equation = " + " + str(self.b) + "x" 
       
        if self.c == 0:
            self.ui.tf_RREF_val3.setText("0")
            self.ui.tf_c.setText("0")
            self.c_equation = ""
        
        else:
            self.c = str(self.c).rstrip('0').rstrip('.')
            self.ui.tf_RREF_val3.setText(self.c)
        
            self.ui.tf_c.setText(self.c)
            self.c_equation = " + " + str(self.c)
            
            
        self.ui.tf_RREF_a1.setText("1")
        self.ui.tf_RREF_b1.setText("0")
        self.ui.tf_RREF_c1.setText("0")

        
        self.ui.tf_RREF_a2.setText("0")
        self.ui.tf_RREF_b2.setText("1")
        self.ui.tf_RREF_c2.setText("0")

        
        self.ui.tf_RREF_a3.setText("0")
        self.ui.tf_RREF_b3.setText("0")
        self.ui.tf_RREF_c3.setText("1")
        
        quadraticEquation = self.a_equation + "x²" + self.b_equation + self.c_equation
        
        self.ui.tf_equation.setText(quadraticEquation) 
        
        
        
        
             
            
if __name__=='__main__':
    
    app=qtw.QApplication([])
    
    widget=Main()
    widget.show()
    
    
    app.exec_()

