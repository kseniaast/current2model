#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import os,sys
import re
#from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import pycx4.qcda as cda

from magnetline_settings import *


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.Magnets = []
        self.vals = {}
        self.chans = {}
        self.Energy = 0
        self.StringFieldsToFile = ''
        self.StringToEmodel = ''
        self.StringToPmodel = ''
        self.initUI()


    def initUI(self):

        self.tog1 = QCheckBox('Electron injection', self)
        self.tog1.move(20, 20)
        #tog1.toggle()
        #tog1.stateChanged.connect(self.listMagnets)

        self.tog2 = QCheckBox('Positron injection', self)
        self.tog2.move(20, 40)
        #tog2.toggle()
        #tog2.stateChanged.connect(self.listMagnets)

        self.tog3 = QCheckBox('Ring', self)
        self.tog3.move(20, 60)
        self.tog3.toggle()
        #tog3.stateChanged.connect(self.listMagnets)

        self.tog4 = QCheckBox('Electron extraction', self)
        self.tog4.move(20, 80)
        #tog4.toggle()
        #tog4.stateChanged.connect(self.listMagnets)

        self.tog5 = QCheckBox('Positron extraction', self)
        self.tog5.move(20, 100)
        #tog5.toggle()
        #tog5.stateChanged.connect(self.listMagnets)

        self.bigbtn1 = QPushButton('Calculate fields!',self)
        self.bigbtn1.move(70,130)
#        self.bigbtn1.clicked.connect(self.findFields)
        self.bigbtn1.clicked.connect(self.datareadNcalc)

        self.bigbtn2 = QPushButton('Update e-model',self)
        self.bigbtn2.move(20,165)
        self.bigbtn2.clicked.connect(self.Eupdate)

        self.bigbtn3 = QPushButton('Update p-model',self)
        self.bigbtn3.move(140,165)
        self.bigbtn3.clicked.connect(self.Pupdate)

        self.setGeometry(300, 300, 270, 200)
        self.setWindowTitle('ReadRing')
        self.show()

#        self.statusBar().showMessage(sender.text() + ' was pressed')


    def listMagnets(self):
        #sender = self.sender()

# Define list of processed magnets:
        if self.tog1.isChecked():
             self.Magnets += MagnetLines['Einjection']
        if self.tog2.isChecked():
             self.Magnets += MagnetLines['Pinjection']
        if self.tog3.isChecked():
             self.Magnets += MagnetLines['Ring']
        if self.tog4.isChecked():
             self.Magnets += MagnetLines['Eextraction']
        if self.tog5.isChecked():
             self.Magnets += MagnetLines['Pextraction']               


    def datareadNcalc(self):
        self.Magnets=[]
        self.listMagnets()
        self.vals={}
        self.chans={}
        self.chans["canhw:12.drm.Iset"]=cda.DChan("canhw:12.drm.Iset")
        print("Read channels...")
        print(self.Magnets)
        for magname in self.Magnets:
            Mcurrents = MagnetType[magname][1]
            for current in Mcurrents:
                if "canhw:{0}.Iset".format(current) not in self.chans.keys():
                    self.chans["canhw:{0}.Iset".format(current)] = cda.DChan("canhw:{0}.Iset".format(current))
        connects = {k:v.valueMeasured.connect(self.callback) for (k,v) in self.chans.items()}
        #print(self.chans.items())
        #print(self.vals.items())

    def callback(self, chan):
        self.vals[chan.name] = chan.val
        #self.chans[chan.name] = chan.name
        #print(self.vals.items())
        #When all data read - start calcs
        if len(self.vals.keys()) >= len(self.chans.keys()):
            print("data collected!")
            #print(self.vals.items())
            self.findFields()
        else:
            print('Still wait...')

    def rmEnergy(self):
        channame = "canhw:12.drm.Iset"
        Irm = self.vals[channame]
        print("Irm = {0} A".format(Irm))
        H0field = -1138.9178 + 28.600754 * Irm -0.04490153* Irm**2 + 7.80301344E-005 * Irm**3  -6.16697411E-008 * Irm**4 + 1.69725511E-011 * Irm**5 #Gs
        self.Energy = 300*H0field*111.1 #MeV
        print("E = {0} eV".format(self.Energy))
        return self.StringToFile

    def findFields(self):
        print('Start calculations...')
        #self.Magnets=[] #reload list
        self.StringToFile = ''
        #self.listMagnets() #get list
        #self.calcEnergy() #read RM data and recalculate
        #print(self.Magnets)
        self.rmEnergy()
        for magname in self.Magnets:
            #print(MagnetType[magname])
            if MagnetType[magname][0] in ['quad60q','quad80q','quad60','quad80','quad20']:
                self.quad(magname)
            if MagnetType[magname][0] in ['sext']:
                self.sext(magname)      
            if MagnetType[magname][0] in ['bm20inj','bm45inj','bm20ext','bm45ext']:
                self.bendmag(magname)
            if MagnetType[magname][0] in ['dcorr60','dcorr80']:
                self.corrquad(magname)
            if MagnetType[magname][0]=='ringmag':
                self.rm(magname)      
#            if MagnetType[magname][0] in ['quad60q','quad80q','quad60','quad80','quad20']:
#                self.StringToFile += self.quad(magname)
#            if MagnetType[magname][0] in ['sext']:
#                self.StringToFile += self.sext(magname)      
#            if MagnetType[magname][0] in ['bm20inj','bm45inj','bm20ext','bm45ext']:
#                self.StringToFile += self.bendmag(magname)
#            if MagnetType[magname][0] in ['dcorr60','dcorr80']:
#                #print(MagnetType[magname][0])
#                self.StringToFile += self.corrquad(magname)
#            if MagnetType[magname][0]=='ringmag':
#                self.StringToFile += self.rm(magname)      
        
    def FindTwiss(self,string):
        workdir = os.getcwd()
        dirname = os.path.dirname(workdir)
        fileInit = os.path.join(dirname,'Saves/currents_cap.sdds')
        fileModel = os.path.join(dirname,'currents_test.sdds')
        fi = open(fileInit,'r')
        fo = open(fileModel,'w+')
        startString=fi.read()
        fo.write(startString)
        fo.write(self.StringToEmodel)
        fi.close()
        fo.close()
#        os.system("""./CountTwiss""")

    def Eupdate(self):
        print('Electrons coordinate system is right-side...')
        self.FindTwiss(self.StringToEmodel)
#        print(self.StringToEmodel)
        
        
    def Pupdate(self):
        print('Positron coordinate system is left-side...')
        self.FindTwiss(self.StringToPmodel)
        #print(self.StringToPmodel)

# Field calculators
    def sext(self,magname):
        Mtype = MagnetType[magname][0]
        Mcurrents = MagnetType[magname][1]
        #print(Mcurrents)
        #Get correct current value for any type
        if len(Mcurrents)==1 and Mtype in ['sext']:
            channame = "canhw:{0}.Iset".format(Mcurrents[0])
            print("Now processing {0} channel".format(channame))          
            I = self.vals[channame]
            #I = 5000
            G2 = 500/12*I*1e-3 #I in mAmpers Gs/cm^2
            K2 = G2/self.Energy*3e8
            self.StringToFile += "{0} G2 {1}\n".format(magname,G2)
            self.StringToEmodel += "{0} K2 {1} \"\" absolute\n".format(magname,K2)
            self.StringToPmodel += "{0} K2 {1} \"\" absolute\n".format(magname,K2)
        return self.StringToFile

    def quad(self,magname):
        Mtype = MagnetType[magname][0]
        Mcurrents = MagnetType[magname][1]
        #print(Mcurrents)
        #Get correct current value for any type
        signG=1 #default
        if MagnetType[magname][2]=='minus':
            signG = -1  
        if MagnetType[magname][2]=='plus':
            signG = 1  
        if len(Mcurrents)==1 and Mtype in ['quad60','quad80','quad20']:
            channame = "canhw:{0}.Iset".format(Mcurrents[0])
            print("Now processing {0} channel".format(channame))          
            I = self.vals[channame]
            #I = 20*signG
            #print(I + 'A')
        if len(Mcurrents)==2 and Mtype in ['quad60q','quad80q']:
            channame = "canhw:{0}.Iset".format(Mcurrents[0])
            corrname = "canhw:{0}.Iset".format(Mcurrents[1])
            print("Now processing {0} and {1} channels".format(channame,corrname))
            I0 = self.vals[channame]
            Ik = self.vals[corrname]
            #print('{0} A, {1} mA'.format(I0,Ik))
            #I0=200*signG #Amper
            #Ik = -1300 #mA
            Atf = AmperTurns[Mtype]
            I = abs(I0-Atf*Ik*1e-3)
        else:
            #I = 0  ????
            pass
        if Mtype in ['quad60','quad60q']:
            #print(magname)
            G=signG*(-16.83524125+2.832126125*I -0.0015659738*I**2 +2.84666125e-6*I**3 -1.83259875e-9*I**4 +1.1924489875e-13*I**5) #Gs/cm
        if Mtype in ['quad80','quad80q']:
            G = signG*(13.38814 + 1.5170534*I + 1.1680249e-3*I**2 - 2.84518241e-6*I**3 +3.0909805e-9 *I**4 -1.2364183e-12*I**5) #Gs/cm
        if Mtype=='quad20':
            G = signG*(5.5e3/9.5*I*1e-3) #I in mAmpers
        #Polarity:
        K1 = G/self.Energy*3e6
        self.StringToFile += "{0} G {1}\n".format(magname,G)
        self.StringToEmodel += "{0} K1 {1} \"\" absolute\n".format(magname,K1)
        self.StringToPmodel += "{0} K1 {1} \"\" absolute\n".format(magname,K1)
        return self.StringToFile
    
    def rm(self,magname):
        if self.Energy == 0:
            self.rmEnergy()
        Mtype = MagnetType[magname][0]
        Mcurrents = MagnetType[magname][1]
        if len(Mcurrents)==2 and Mtype in ['ringmag']:
            channame = "canhw:{0}.Iset".format(Mcurrents[0])
            corrname = "canhw:{0}.Iset".format(Mcurrents[1])
            print("Now processing {0} and {1} channels for RM".format(channame,corrname))
            I0 = self.vals[channame]
            Ik = self.vals[corrname]
            #I0=700 #Amper
            #Ik = 1300 #mA
            I = I0+6.67*Ik*0.001
            #print('I=' + I)
            H = -1138.9178 + 28.600754 * I -0.04490153* I**2 + 7.80301344E-005 * I**3  -6.16697411E-008 * I**4 + 1.69725511E-011 * I**5 #Gs
            G = 100.981701 -1.47689656 * I + 0.0039728* I**2 - 7.0629494E-006 * I**3 + 5.79274578E-009 * I**4 -1.71765978E-012 * I**5 #Gs/cm
            #FSE = (H*300*111.1/self.Energy) - 1
            FSE = H *3e4*(Rbends[Mtype]/self.Energy) - 1    
            K1 = 300*G/self.Energy*1e4
            self.StringToFile += "{0} H {1}\n{0} G {2}\n".format(magname,H,G)
            self.StringToEmodel += "{0} FSE {1} \"\" absolute\n{0} K1 {2} \"\" absolute\n".format(magname,FSE,K1)
            self.StringToPmodel += "{0} FSE {1} \"\" absolute\n{0} K1 {2} \"\" absolute\n".format(magname,FSE,K1)
        return self.StringToFile
      
    def bendmag(self,magname):
        Mtype = MagnetType[magname][0]
        Mcurrents = MagnetType[magname][1]
        if len(Mcurrents)==1 and Mtype in ['corr']:
            channame = "canhw:{0}.Iset".format(Mcurrents[0])
            print("Now processing {0} channel".format(channame))
            #I = 'channame.val' if Flag_valueMeasured == 1...
            I=2000*1e-3 #mA
        if len(Mcurrents)==2 and Mtype in ['bm20inj','bm45inj','bm20ext','bm45ext']:
            channame = "canhw:{0}.Iset".format(Mcurrents[0])
            corrname = "canhw:{0}.Iset".format(Mcurrents[1])
            print("Now processing {0} and {1} channels".format(channame,corrname))
            I0 = self.vals[channame]
            Ik = self.vals[corrname]
            #I0=400 #Amper
            #Ik = -1300 #mA
            Atf = AmperTurns[Mtype]
            I = I0+Atf*Ik*1e-3
        else:
            #I = 0  ????
            pass
        if Mtype in ['bm20inj']:
            H = -1.757669e+02 + 2.210424e+01*I -2.308797e-02*I**2 + 5.929725e-05*I**3 -6.464138e-08 *I**4 + 2.273062e-11*I**5 #Gs/cm
        if Mtype in ['bm45inj']:
            H= -1.908530e+02  + 2.230154e+01*I -2.302947e-02*I**2 + 5.565655e-05*I**3 -5.658736e-08 *I**4 + 1.851561e-11*I**5 #Gs/cm
        if Mtype in ['bm20ext']:
            H = -2.593063e+02 + 5.855757e+01*I -1.767359e-01*I**2 + 1.003086e-03*I**3 -2.426794e-06*I**4 + 1.914091e-09*I**5 #Gs/cm
        if Mtype in ['bm45ext']:
            H= -4.081962e+02  + 6.383789e+01*I -2.328271e-01*I**2 + 1.244745e-03*I**3 -2.851177e-06*I**4 + 2.175583e-09*I**5 #Gs/cm
        FSE = H *3e4*(Rbends[Mtype]/self.Energy) - 1    
        self.StringToFile += "{0} H {1}\n".format(magname,H)
        self.StringToEmodel += "{0} FSE {1} \"\" absolute\n".format(magname,FSE)
        self.StringToPmodel += "{0} FSE {1} \"\" absolute\n".format(magname,FSE)
        #return self.StringToFile

    def corrquad(self,magname):
        Mtype = MagnetType[magname][0]
        Mcurrents = MagnetType[magname][1]
        if len(Mcurrents)==1 and Mtype in ['dcorr60','dcorr80']:
            channame = "canhw:{0}.Iset".format(Mcurrents[0])
            print("Now processing {0} channel".format(channame))
            I = self.vals[channame]
            print("I={0} mA".format(I))
            #I=2000*1e-3 #mA
        if MagnetType[magname][2]=='plus':
            signH=1
        elif MagnetType[magname][2]=='minus':
            signH=-1	  
        if Mtype in ['dcorr60']:
            H = 1.678 +23.2841*I*1e-3 - 0.0204779*(I*1e-3)**2
            KICK = signH*300*H/self.Energy*18
        if Mtype in ['dcorr80']:
            H = 5.186635*5.45*I*1e-3
            KICK = signH*300*H/self.Energy*20
        #self.StringToFile += "{0} H {1}\n".format(magname,H)
        editname = re.sub(r'c',"Q",magname)
        editname = re.sub(r'[xz]',"",editname)
        if MagnetType[magname][3]=='V':
            self.StringToFile += "{0} VKICK {1}\n".format(editname,KICK)
            self.StringToEmodel += "{0} VKICK {1} \"\" absolute\n".format(editname,KICK)
            self.StringToPmodel += "{0} VKICK {1} \"\" absolute\n".format(editname,KICK)
        if MagnetType[magname][3]=='H':
            self.StringToFile += "{0} HKICK {1}\n".format(editname,KICK)
            self.StringToEmodel += "{0} HKICK {1} \"\" absolute\n".format(editname,KICK)
            self.StringToPmodel += "{0} HKICK {1} \"\" absolute\n".format(editname,KICK)

        #return self.StringToFile
        
    
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())