#$Id$
from __future__ import with_statement
from com.adventnet.zoho.client.report.python.ReportClient import ReportClient
import sys


class Config:
     LOGINEMAILID="<your login email id>"
     AUTHTOKEN="<your authtoken>"
     DATABASENAME="<your db name>"
     TABLENAME="<your table name>"

    
class Sample:

    rc = None

    def test(self):

        rc = self.getReportClient()
        opt = self.getOption()
        if(opt == 6):
             uri = rc.getDBURI(Config.LOGINEMAILID,Config.DATABASENAME)
        else:
               uri = rc.getURI(Config.LOGINEMAILID,Config.DATABASENAME,Config.TABLENAME)
        if(opt == 1):
             self.addSingleRow(rc,uri)
        elif(opt == 2):
             self.updateData(rc,uri)
        elif(opt == 3):
             self.deleteData(rc,uri)
        elif(opt == 4):
             self.importData(rc,uri)
        elif(opt == 5):
             rc.exportData(uri,"CSV",sys.stdout,None,None)
        elif(opt == 6):
             sql = "select Region from " + Config.TABLENAME
             rc.exportDataUsingSQL(uri,"CSV",sys.stdout,sql,None)

    def getReportClient(self):
            
        if(Config.AUTHTOKEN == ""):
            raise Exception,"Configure AUTHTOKEN in Config class"
            
        if(Sample.rc == None):
            Sample.rc = ReportClient(Config.AUTHTOKEN)
        return Sample.rc;

  
    def addSingleRow(self,rc,uri):
        rowData = {"Date":"01 Jan, 2009 00:00:00","Region":"East","Product Category":"Samples",
                   "Product":"SampleProduct","Customer Name":"Sample","Sales":2000,
                   "Cost":2000}
        result = rc.addRow(uri,rowData,None)
        print result

    def updateData(self,rc,uri):
        updateInfo = {"Region":"West","Product":"SampleProduct_2"}
        rc.updateData(uri,updateInfo,"\"Customer Name\"='Sample'",None);
      

    def deleteData(self,rc,uri):
        rc.deleteData(uri,"\"Customer Name\"='Sample'",None);

    def importData(self,rc,uri):
        try:
            with open('StoreSales.csv', 'r') as f:
                importContent = f.read()
        except Exception,e:
            print "Error Check if file StoreSales.csv exists in the current directory!! "
            print "(" + str(e) + ")"
            return
          
        impResult = rc.importData(uri,"APPEND",importContent,None)
        print "Added Rows :" +str(impResult.successRowCount) + " and Columns :" + str(impResult.selectedColCount)

    def getOption(self):
        print "\n\nOptions\n 1 - Add Single Row\n 2 - Update Data\n 3 - Delete Data\n 4 - Import Data\n 5 - Export Data\n 6 - Export Data Using SQL"
        print "\nEnter option : "
        option = sys.stdin.readline().strip()
        while((option == "") or (int(option) < 1) or (int(option) > 6)):
            print "Enter proper option."
            option = sys.stdin.readline().strip()
        return int(option)
              
  
if __name__ == "__main__":
    Sample().test()
