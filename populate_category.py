import os

def populate():
	#file_obj=open("data_of_rc.csv")
	#print file_obj
	#file_obj.close()
	f=open("category_names.txt")
	for line in f:
		cname=line.replace("\n","")
		cat_added=add_category(cname)
	f.close()

def add_category(cname):
    cat = Category.objects.get_or_create(category=cname,description=cname)[0]#for now description is same as category_names
    print "category " +str(cname)+" added \n"
    return cat

# Start execution here!
if __name__ == '__main__':
    print "Starting population script for adding category..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AakashTechSupport.settings')
    from aakashuser.models import *
    populate()
