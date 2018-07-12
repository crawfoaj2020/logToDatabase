#Handle: 
#Error checking
#Headers

#Consider:
#File with all regular expressions - basically a list of constants
#Are headers always the same
#any level of user control over formating
#Using forigen keys in createTable
#Use drop down or similar for entering type of thing in GUI
#Column ordering - ie does the pattern have to be in the same order as the table (currently yes)
#Table name vs file name (currently same)

#Goal:
#Create GUI that allows user to select file location, destination
#Also always user template for creating new tables
#file name, column names, types, format (use regular expressions, with examples)
#something like pattern 1, .... pattern 2, build the combined string myself



import re
import os
import sqlite3
import tableDS

def createTable(tableInfo):
    """ 
    :param tableInfo: Contains information about the table to be created
    :type tableInfo: Table
    """
    colsList = makeColsList(tableInfo.getCols(), tableInfo.getTypes())
    sql = 'Create table if not exists {tn} ({cols})'.format(tn = tableInfo.getName(), cols = colsList)
    c.execute(sql)

def makeColsList(colNames, colTypes):
    """ Helper for createTable """
    if len(colNames) != len(colTypes):
        raise RuntimeError ('The length of col names must equal the length of col types')
    if len(colTypes) == 0:
        raise RuntimeError('Must contain at least one column')
    result = ""
    index = 0
    for col in colNames:
        result += '[{col}] {type}, '.format(col = col, type = colTypes[index])
        index += 1
    result = result[0: -2]
    return result

def insertFileContents(contents, table):
    """
    :param contents: the contents of the file
    :type contents: string
    :param table: the table object that describes the table to be inserted into
    :param table: Table
   """
    results = re.findall(table.getPattern(), contents)
    for infoResult in results:
        columns = makeList(table.getCols(), '[', ']')
        vals = makeList(infoResult, '\'', '\'')
        try:
            c.execute('insert into {tn}  ({cols}) values ({vals})'.format(tn = table.getName(), cols = columns, vals = vals))
            break
        except sqlite3.OperationalError:
            newResult = stringReplaceQuotes(infoResult)
            vals = makeList(newResult, '\'', '\'')
            c.execute('insert into {tn}  ({cols}) values ({vals})'.format(tn = table.getName(), cols = columns, vals = vals))


def makeList(listOfStrs, leftAdd, rightAdd):
    """
    :param list: The list of elements to convert into a formated string list
    :type list: list
    :param leftAdd: What to add to the left of each element
    :type leftAdd: String
    :param rightAdd: What to add to the right of each element
    :type rightAdd: String
    """
    result = ""
    for str in listOfStrs:
        result += '{left}{str}{right}, '.format(left = leftAdd, right = rightAdd, str=str)
    result = result[0: -2]
    return result

def stringReplaceQuotes(strArr):
    result = []
    for str in strArr:
        result.append(str.replace('\'', '\'\''))
    return result



def makeTwoColTable(tableName):
    cols = ['dateTime', 'desc']
    types = ['text', 'text']
    table = tableDS.Table(tableName, cols, types, dateAndValue)
    createTable(table)
    return table

def makeThreeColTable(tableName):
    cols = ['dateTime', 'status', 'desc']
    types = ['text', 'text', 'text']
    table = tableDS.Table(tableName, cols, types, dateLabelValue)
    createTable(table)
    return table



#Used by: Errors, pipetting, span8 pipetting, span8Transfer, Unified pipetting, unified transfer 
dateAndValue = re.compile(r'.*?(\d\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d),(.*?)\n', re.DOTALL)
#Used by: Details
dateLabelValue = re.compile(r'.*?(\d\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d),(.*?):\n(.*?)\n', re.DOTALL) #Expects new line before value


#Paths
sqlite_file = 'noHeadersLastTry.db3'
folderPath = 'C:\\Users\\AJCRAWFORD\\Documents\\Example from Praveena\\R0273091_2018.06.21_1236\\Logs\\Biomek Logs\\Logs'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

tables = []

#Make tables
tables.append(makeTwoColTable('Pipetting'))
tables.append(makeTwoColTable('Errors'))
tables.append(makeTwoColTable('Span8Pipetting'))
tables.append(makeTwoColTable('Span8Transfer'))
tables.append(makeTwoColTable('UnifiedPipetting'))
tables.append(makeTwoColTable('UnifiedTransfer'))
tables.append(makeThreeColTable('Details'))



#Do actual load
for filename in os.listdir(folderPath):
    file = os.path.join(folderPath, filename)
    temp = open(file, 'r')
    content = temp.read()
    for table in tables:
        tableName = table.getName()
        if filename.startswith(tableName):
            insertFileContents(content, table)
  
print("Load complete")


conn.commit()
conn.close()