import os

def populate():
	#file_obj=open("data_of_rc.csv")
	#print file_obj
	#file_obj.close()
	import csv
	dataReader = csv.reader(open("data_of_rc.csv"), delimiter=',', quotechar='"')
	for row in dataReader:
		rcID= int(row[0])
		rcName=row[1]
		count=row[2]
		start_tab_id=row[3]
		end_tab_id=row[4]
		city=row[5]	
		tab_added=add_tablet(rcID, rcName, start_tab_id, end_tab_id,count,city)
    

def add_tablet(rcID, rcName, start_tab_id, end_tab_id,count,city):
    tab = Tablet_info.objects.get_or_create(rcID=rcID, rcName=rcName, start_tab_id=start_tab_id, end_tab_id=end_tab_id,count=count,city=city)[0]
    print "rc " +str(rcID)+"added \n"
    return tab

# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AakashTechSupport.settings')
    from aakashuser.models import *
    populate()
