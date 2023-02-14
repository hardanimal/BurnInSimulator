# encoding: utf-8

__author__ = 'Danzel.Li@finisar.com'

from xml.dom.minidom import parse
import xml.dom.minidom
import pymssql
import time


class BISlotInfo(object):
    
    DB_Connection = ""
    DB_Name = ""
    DB_User = ""
    DB_Password = ""
    DB_TableName = ""
    DataContent = {}
    
    def load_xmldata(self, xmlfile):
        try:
            DOMTree = parse(xmlfile)
            Settings = DOMTree.documentElement
            
            # get database connection info
            self.DB_Connection = Settings.getElementsByTagName('DatabaseConnection')[0].childNodes[0].data
            self.DB_Name = Settings.getElementsByTagName('DatabaseName')[0].childNodes[0].data
            self.DB_User = Settings.getElementsByTagName('DatabaseUser')[0].childNodes[0].data
            self.DB_Password = Settings.getElementsByTagName('DatabasePassword')[0].childNodes[0].data
                        
            self.DB_TableName = Settings.getElementsByTagName('DatabaseTable')[0].childNodes[0].data
            
            # get writing database data
            if len(self.DataContent) != 0:
                self.DataContent.clear()
            for rawdata in Settings.getElementsByTagName('DataContent')[0].childNodes:
                if rawdata.nodeType == 1:
                    self.DataContent[rawdata.nodeName] = rawdata.childNodes[0].data
        except:
            print("Please check config XML file!")
            return False
        
        try:
            conn = pymssql.connect(host=self.DB_Connection, database=self.DB_Name, user=self.DB_User, password=self.DB_Password)
        except:
            print("Please check database connection!")
            return False
        finally:
            if 'conn' in locals().keys():
                conn.close()
        return True

    def write_database(self, action):
        self.DataContent["BI_State"] = action
        return self._SaveSlotInfoToNetDB(self.DB_TableName, self.DataContent)
    
    def _ExecuteCMDSQLNet(self, CMDSQL):
        retryTimes = 0
        ActionOK = False
        while retryTimes < 5:
            try:
                conn = pymssql.connect(host=self.DB_Connection, database=self.DB_Name, user=self.DB_User, password=self.DB_Password)
                cur = conn.cursor()
                cur.execute(CMDSQL)
                conn.commit()
                ActionOK = True
            except:
                ActionOK = False
                print("Retry ...")
            finally:
                if 'cur' in locals().keys():
                    cur.close()
                if 'conn' in locals().keys():
                    conn.close()
            if ActionOK == False:
                time.sleep(1)
                retryTimes += 1
            else:
                break
        return ActionOK
    
    def _SaveSlotInfoToNetDB(self, TableName, data):
        strField = ""
        strData = ""
        for k in data.keys():
            strField = strField + k + ","
            strData = strData + "'" + data[k] + "',"
            
        strField = strField + "RunTime"
        strData = strData + "GetDate()"
        
        strCmd = "insert into " + TableName + " (" + strField + ") values (" + strData + ")"
        return self._ExecuteCMDSQLNet(strCmd)


if __name__ == "__main__":
    BIS = BISlotInfo()
    if BIS.load_xmldata('../../DFB.xml'):
        while True:
            BIS.write_database("Read")
            time.sleep(900)

