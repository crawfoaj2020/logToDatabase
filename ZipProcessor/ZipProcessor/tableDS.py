#Each table an array
#a[0] = table name
#a[1] = list column names
#a[2] = list column types
#a[3] = column patterns

class Table():
    """
    :param tableName: The name of the table
    :type tableName: String
    :param colNames: The names of the columns to create in the table
    :type colNames: list
    :param colNames: The types of the columns. Order should match colNames. Check valid types elsewhere
    :type colNames: list
    :param patternStr: The pattern to match when going through this type of table
    :type patternStr: a complied regular expression
   """
    def __init__(self, tableName, colNames, colTypes, patternStr):
       self.tableArr =  [tableName, colNames, colTypes, patternStr]
    def getName(self):
        return self.tableArr[0]
    def getCols(self):
        return self.tableArr[1]
    def getTypes(self):
        return self.tableArr[2]
    def getPattern(self):
        return self.tableArr[3]



