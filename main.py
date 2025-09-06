import oracledb
try:
    connection = oracledb.connect(
        user="sys",
        password="pass", 
        dsn="ip:port/dbname",
        mode=oracledb.AUTH_MODE_SYSDBA
    )
    print("Connection successful!")
except oracledb.Error as e:
    print(f"Connection error: {e}")

cursor = connection.cursor()
# cursor.execute("SELECT sys_context('USERENV', 'ORACLE_HOME') FROM dual")   
# cursor.execute("SELECT snap_id, begin_interval_time, end_interval_time FROM dba_hist_snapshot WHERE begin_interval_time >= SYSDATE-1 ORDER BY snap_id DESC")   
# print(cursor.fetchall())


while True:
    fileType=input("Enter value for report_type: ")

    if fileType=="" or fileType.lower()=="html":
        fileType = "html"
        print("You have selected the default html format") 
        break 
        
    # elif fileType.lower()=="text":
    #     fileType = "text"
    #     print("You have selected text format")
    #     break
    else:
        print("Only HTML format available")
          
while True:    
    numDays=input("Enter value for num_days: ")
    if numDays=="":
        numDays=1
        print("You have chosen default Number of days whihc is one")
        break
    else:
        try:
            num=int(numDays) 
            if num >0 and num<=30:
                print(f"You have entered {num}")
                break
            else:
                print("Eneter only the valid number form 1-30") 
        except ValueError:
            print("Please enter a valid number")                

query=f"SELECT snap_id, begin_interval_time FROM dba_hist_snapshot WHERE begin_interval_time >= SYSDATE- {numDays} ORDER BY snap_id "
cursor.execute(query)
result=cursor.fetchall() 
# print(result)      
print("Snap Id       Snap Started")
snap_id_list=[]
for align in result:
    snap_id, begin_interval_time=align 
    snap_id_list.append(snap_id)
    formatted_time = begin_interval_time.strftime("%d %b %Y %H:%M")
    print(snap_id,f"   ",formatted_time)
# while True:
#     beginSnapId=input("Enter value for begin_snap: ")
#     try:
#         beginSnap=int(beginSnapId)
#         if beginSnap in snap_id_list:        
#             break
#     except ValueError:
#             print("Please enter a valid number")
# while True:
#     endSnapId=input("Enter value for end_snap: ")
#     try:
#         endSnap=int(endSnapId)
#         if endSnap in snap_id_list: 
#             if endSnap>beginSnap:       
#                 break
#             else:
#                 print("End Snap must be grater than the begin snap id")
#     except ValueError:
#             print("Please enter a valid number")
# userBeginId=[]
# userEndId=[]
while True:
    beginSnapId=input("Enter value for begin_snap: ")
    try:
        beginSnap=int(beginSnapId)
        # userBeginId.append(beginSnap)
        if beginSnap in snap_id_list:
            endSnapId=input("Enter value for end_snap: ")
            endSnap=int(endSnapId)
            # userEndId.append(endSnap)
            if endSnap in snap_id_list: 
                if endSnap>beginSnap:       
                    break
                else:
                    print("End Snap must be grater than the begin snap id")
            else:
              print("Please enter a valid Snap id")
        else:
            print("Please enter the valid snap id from the lsit")
    except ValueError:
        print("Please enter a valid number")
defaultFileName=f"awrrpt_{beginSnap}_{endSnap}.{fileType}"
reportName=input(f"Enter value for report_name (default name is {defaultFileName}): ")
if reportName=="":
    reportName=defaultFileName
# elif reportName=='<'or reportName=='>'or reportName==':'or reportName=='"'or reportName=='|'or reportName=='?'or reportName=='*'or reportName=='/':
elif reportName !="":
    for char in ['<','>',':','"','|','?','*','/']:
        if char in reportName:
            print("Invalid filename using the default report name.")
            reportName=defaultFileName
            break

cursor.execute("SELECT dbid FROM v$database")
dbId=cursor.fetchone()[0]
cursor.execute("SELECT instance_number FROM v$instance")
instNum=cursor.fetchone()[0]
mainQuery=f"""SELECT output
FROM TABLE(
    DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_HTML(
        {dbId},   -- DBID from v$database
        {instNum},            -- Instance number from v$instance
        {beginSnap},          -- Begin snapshot ID
        {endSnap},          -- End snapshot ID
        0             -- Report options
    )
)
"""
cursor.execute(mainQuery)
awrRptResult=cursor.fetchall()
# print(awrRptResult)

# fullReport=""
# for row in awrRptResult:
#     line=row[0]
#     if line is not None:
#         fullReport+=line
# print(fullReport)

# lines=[row[0] for row in awrRptResult if row[0] is not None] 
lines=[]
for row in awrRptResult:
    if row[0] is None:
        lines.append("\n")
    else:
        lines.append(row[0] + "\n")
fullReport="".join(lines)

# none_count = 0
# for row in awrRptResult:
#     if row[0] is None:
#         none_count += 1

# print(f"Found {none_count} None values out of {len(awrRptResult)} total rows")
# print(f"Percentage of None values: {(none_count/len(awrRptResult))*100:.1f}%")

# print(fullReport) 

with open(rf"C:\Users\ECS\Desktop\Learn\PY\database_awr\reports\{reportName}","w") as finalReport:
    finalReport.write(fullReport)
cursor.close()
connection.close()
