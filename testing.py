import MySQLdb
import xlsxwriter
import mysql.connector  
import datetime  
import logging
import sys



from xml.dom import minidom

doc = minidom.parse("mykong.xml")

majors = doc.getElementsByTagName("major")

get_user = doc.getElementsByTagName("user")[0]
get_pwd = doc.getElementsByTagName("password")[0]
get_db = doc.getElementsByTagName("dbname")[0]
get_host = doc.getElementsByTagName("host")[0]
user = get_user.firstChild.data
pwd = get_pwd.firstChild.data
dbn = get_db.firstChild.data
host = get_host.firstChild.data
log = open("myprog.log", "a")
sys.stdout = log


db = mysql.connector.connect(user=user, password=pwd,
                              host=host,
                              database=dbn)
                              
                              

cursor = db.cursor()

for major in majors:

  title = major.getElementsByTagName("title")[0]
  heading = title.firstChild.data
  sql = major.getElementsByTagName("sql")[0]
  location = major.getElementsByTagName("location")[0]
  loc = location.firstChild.data
  query=sql.firstChild.data 
  try:  
          print query
          
          cursor.execute(query)
          
          result = cursor.fetchall()
          num_fields = len(cursor.description)
        
          field_names = [i[0] for i in cursor.description]
          print result
          workbook = xlsxwriter.Workbook(loc)
          worksheet = workbook.add_worksheet()


                      
        
          bold = workbook.add_format({'bold': True})
          date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
          time_format = workbook.add_format({'num_format': 'hh:mm:ss'})
          timestamp_format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
          format = workbook.add_format()
          size = workbook.add_format()
          align = workbook.add_format()
          format.set_border()
          date_format.set_border()
          time_format.set_border()
          timestamp_format.set_border()
          align.set_border()
          format.set_bg_color('cyan')
          size.set_font_size(20)  
          align.set_align('left')
          date_format.set_align('left')
          time_format.set_align('left')
          timestamp_format.set_align('left')
          worksheet.write(0,0,heading,size)
          worksheet.set_column(0,6,10)
          format.set_bold()
          

          row=1
          col=0
          j = 0
          for rows in field_names:

              worksheet.write(row,col,field_names[j],format)

              col = col + 1
              j = j + 1
          n=0
          for rows in result:
            col=0
            row = row + 1
            for cols in rows:
                if type(result[n][col]) is datetime.date:
                  worksheet.write(row,col,result[n][col],date_format)
                if type(result[n][col]) is datetime.timedelta :
                  worksheet.write(row,col,result[n][col],time_format)
                if type(result[n][col]) is datetime.datetime:
                  worksheet.write(row,col,result[n][col],timestamp_format)

                else:
                  
                  worksheet.write(row,col,result[n][col],align)

                col = col + 1
            n = n+1
                


            
          
    
  except Exception as inst:
        print "database & workbook is closing due to Exception"
        
      
      

workbook.close()
db.close()
print "database closed"
print "fine"