import pyodbc 

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-9SP3VP3\SQLEXPRESS;"
                      "Database=KTXLDL_AQI;"
                      "Trusted_Connection=yes;")

cursor = cnxn.cursor()
cursor.execute('SELECT * FROM AQI_INFORMATION')
print(cursor)
for row in cursor:
    print('row = %r' % (row,))

SQLCommand = ("INSERT INTO AQI_INFORMATION(NameCity, AQIIndex, Pm25) VALUES (?,?,?)")    
Values = ['Id',4,5]
cursor.execute(SQLCommand,Values)     
cnxn.commit()