# encoding: utf-8

__author__ = 'Danzel.Li@finisar.com'

import os
import sys
sys.path.append("../../src/")   # for debug
sys.path.append("./src/")
sys.path.append("./BIS_GUI/")
print(os.getcwd())
import time
import datetime
import _thread

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

app = QtWidgets.QApplication(sys.argv)

class Program_State(object):
    No_data_loaded = 'No_data_loaded'
    Data_loaded = 'Data_loaded'
    Start_BurnIn = 'Start_BurnIn'
    BurnIn_InProcess = 'BurnIn_InProcess'
    BurnIn_Stuck = 'BurnIn_Stuck'
    BurnIn_Continue = 'BurnIn_Continue'
    BurnIn_Pause = 'BurnIn_Pause'
    BurnIn_Idle = 'BurnIn_Idle'
    BurnIn_Stop = 'BurnIn_Stop'
    
class BurnIn_Action(object):
    StartBI = 'StartBI'
    Read = 'Read'
    Pause = 'Pause'
    AheadFinishBI = 'AheadFinishBI'
    

try:
    import BIS
    from BIS.BISlotInfo import BISlotInfo
except Exception as e:
    msg = QtWidgets.QMessageBox()
    msg.critical(msg, "error", str(e))
    
try:
    from bis_gui import Ui_BIS_GUI
except Exception as e:
    msg = QtWidgets.QMessageBox()
    msg.critical(msg, "error", str(e))



class main_window(QtWidgets.QMainWindow):
    
    def __init__(self):
        self.KeepUpdate = True
        self.RunningState = Program_State.No_data_loaded
        self.ins_DataProcessor = BISlotInfo()
        
        self.BurnInStart = None
        self.BurnInStop = None
        self.NextRecord = None
        self.BurnInInterval = datetime.timedelta(minutes=15)    # 15minutes
    
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_BIS_GUI()
        self.ui.setupUi(self)
        self.ui.btn_LoadConfig.clicked.connect(self.btn_LoadConfig_Click)
        self.ui.btn_START.clicked.connect(self.btn_START_Click)
        self.ui.btn_PAUSE.clicked.connect(self.btn_PAUSE_Click)
        self.ui.btn_STUCK.clicked.connect(self.btn_STUCK_Click)

    def Load_Window(self):
        self.SetProgramState(Program_State.No_data_loaded)
        _thread.start_new_thread(self._function_BurnInBackgroud, ())

    def btn_LoadConfig_Click(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "Chose config", os.getcwd(), "XML Files (*.xml)")
        if self.ins_DataProcessor.load_xmldata(fileName):
            self.SetProgramState(Program_State.Data_loaded)
        else:
            self.SetProgramState(Program_State.No_data_loaded)

    def SetProgramState(self, ps):
        lable_pre_string = "Status: "
        self.AppendTestLog("Setting current state: " + ps)
        self.RunningState = ps

        if ps == Program_State.No_data_loaded:
            self.ui.btn_LoadConfig.setDisabled(False)
            self.ui.lbl_Status.setText(lable_pre_string + "INIT")
            self.ui.btn_START.setDisabled(True)
            self.ui.btn_START.setText("START")
            self.ui.btn_PAUSE.setDisabled(True)
            self.ui.btn_PAUSE.setText("PAUSE")
            self.ui.btn_STUCK.setDisabled(True)
            self.ui.btn_STUCK.setText("STUCK")
            #tssl_config.Text = "No config file loaded."
        elif ps == Program_State.Data_loaded:
            self.ui.btn_LoadConfig.setDisabled(False)
            self.ui.lbl_Status.setText(lable_pre_string + "READY")
            self.ui.btn_START.setDisabled(False)
            self.ui.btn_START.setText("START")
            self.ui.btn_PAUSE.setDisabled(True)
            self.ui.btn_PAUSE.setText("PAUSE")
            self.ui.btn_STUCK.setDisabled(True)
            self.ui.btn_STUCK.setText("STUCK")
            #tssl_config.Text = "Config file loaded."
        elif ps == Program_State.Start_BurnIn or ps == Program_State.BurnIn_InProcess or ps ==Program_State.BurnIn_Continue:
            self.ui.btn_LoadConfig.setDisabled(True)
            self.ui.lbl_Status.setText(lable_pre_string + "BURNIN")
            self.ui.btn_START.setDisabled(False)
            self.ui.btn_START.setText("STOP")
            self.ui.btn_PAUSE.setDisabled(False)
            self.ui.btn_PAUSE.setText("PAUSE")
            self.ui.btn_STUCK.setDisabled(False)
            self.ui.btn_STUCK.setText("STUCK")
            #tssl_config.Text = "BurnIn started."
        elif ps == Program_State.BurnIn_Stuck:
            self.ui.btn_LoadConfig.setDisabled(True)
            self.ui.lbl_Status.setText(lable_pre_string + "STUCK")
            self.ui.btn_START.setDisabled(False)
            self.ui.btn_START.setText("STOP")
            self.ui.btn_PAUSE.setDisabled(True)
            self.ui.btn_PAUSE.setText("PAUSE")
            self.ui.btn_STUCK.setDisabled(False)
            self.ui.btn_STUCK.setText("CONTINUE")
            #tssl_config.Text = "BurnIn stuck."
        elif ps ==  Program_State.BurnIn_Pause or ps == Program_State.BurnIn_Idle:
            self.ui.btn_LoadConfig.setDisabled(True)
            self.ui.lbl_Status.setText(lable_pre_string + "PAUSE")
            self.ui.btn_START.setDisabled(False)
            self.ui.btn_START.setText("STOP")
            self.ui.btn_PAUSE.setDisabled(False)
            self.ui.btn_PAUSE.setText("CONTINUE")
            self.ui.btn_STUCK.setDisabled(True)
            self.ui.btn_STUCK.setText("STUCK")
            #tssl_config.Text = "BurnIn pause."
        elif ps == Program_State.BurnIn_Stop:
            self.ui.btn_LoadConfig.setDisabled(False)
            self.ui.lbl_Status.setText(lable_pre_string + "STOP")
            self.ui.btn_START.setDisabled(False)
            self.ui.btn_START.setText("START")
            self.ui.btn_PAUSE.setDisabled(True)
            self.ui.btn_PAUSE.setText("PAUSE")
            self.ui.btn_STUCK.setDisabled(True)
            self.ui.btn_STUCK.setText("STUCK")
            #tssl_config.Text = "BurnIn stopped."
            
    def _function_BurnInBackgroud(self):
        try:
            while (self.KeepUpdate):
                RunningState = self.RunningState
                if RunningState == Program_State.No_data_loaded or RunningState == Program_State.Data_loaded:
                    # Do nothing
                    pass
                elif RunningState == Program_State.Start_BurnIn:
                    self.BurnInStart = datetime.datetime.now()
                    self.NextRecord = self.BurnInStart + self.BurnInInterval
                    self.ins_DataProcessor.write_database(BurnIn_Action.StartBI)
                    self.SetProgramState(Program_State.BurnIn_InProcess)
                elif RunningState == Program_State.BurnIn_InProcess:
                    if (datetime.datetime.now() > self.NextRecord):
                        self.NextRecord += self.BurnInInterval
                        self.ins_DataProcessor.write_database(BurnIn_Action.Read)
                elif RunningState == Program_State.BurnIn_Stuck:
                    # stop writing log into database when next loop
                    pass
                elif RunningState == Program_State.BurnIn_Continue:
                    # resume BurnIn
                    self.NextRecord = datetime.datetime.now() + self.BurnInInterval
                    self.SetProgramState(Program_State.BurnIn_InProcess)
                elif RunningState == Program_State.BurnIn_Pause:
                    # set BurnIn pause
                    self.ins_DataProcessor.write_database(BurnIn_Action.Pause)
                    self.SetProgramState(Program_State.BurnIn_Idle)
                elif RunningState == Program_State.BurnIn_Idle:
                    # Do nothing
                    pass
                elif RunningState == Program_State.BurnIn_Stop:
                    # set BurnIn stop
                    self.BurnInStop = datetime.datetime.now()
                    self.ins_DataProcessor.write_database(BurnIn_Action.AheadFinishBI)
                    self.SetProgramState(Program_State.Data_loaded)
                time.sleep(1)
            
        except Exception as e:
            print(e.message)
            

    def btn_START_Click(self):
        RunningState = self.RunningState
        if (RunningState == Program_State.Data_loaded or RunningState == Program_State.BurnIn_Stop):
            self.SetProgramState(Program_State.Start_BurnIn)
        elif RunningState == Program_State.Start_BurnIn or RunningState == Program_State.BurnIn_InProcess or \
             RunningState == Program_State.BurnIn_Continue or RunningState == Program_State.BurnIn_Stuck or \
             RunningState == Program_State.BurnIn_Pause or RunningState == Program_State.BurnIn_Idle:
            self.SetProgramState(Program_State.BurnIn_Stop)

    def btn_PAUSE_Click(self):
        RunningState = self.RunningState
        if RunningState == Program_State.Start_BurnIn or RunningState == Program_State.BurnIn_InProcess or RunningState == Program_State.BurnIn_Continue:
            self.SetProgramState(Program_State.BurnIn_Pause)
        elif RunningState == Program_State.BurnIn_Pause or RunningState == Program_State.BurnIn_Idle:
            self.SetProgramState(Program_State.BurnIn_Continue)

    def btn_STUCK_Click(self):
        RunningState = self.RunningState
        if RunningState == Program_State.Start_BurnIn or RunningState == Program_State.BurnIn_InProcess or RunningState == Program_State.BurnIn_Continue:
            self.SetProgramState(Program_State.BurnIn_Stuck)
        elif (RunningState == Program_State.BurnIn_Stuck):
            self.SetProgramState(Program_State.BurnIn_Continue)

    def AppendTestLog(self, text, PrintTime = True):
        display = PrintTime and ("Local time: " + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S") + "\t") or ""
        display += text
        self.ui.rtbLog.append(display)

def start():
    window = main_window()
    window.show()
    window.Load_Window()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    start()
    