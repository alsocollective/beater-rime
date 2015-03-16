import gspread

persons = ["Bohdan", "Symon", "Emma", "Antonio", "Lisa"]


def getWorkSheet(pageName):

	gc = gspread.login(googlelogin["user"], googlelogin["password"])
	sh = gc.open("timetrackdjango")
	try:
		return sh.worksheet(pageName)
	except Exception, e:
		return sh.add_worksheet(title=pageName, rows="20", cols="10")





wks = getWorkSheet("People")
count = len(persons)
cell_list = wks.range('A1:C%d'%count)
for i in range(0,count):
	cell_list[(i*3)].value = persons[i]
	cell_list[(i*3)+1].value = "second"
	cell_list[(i*3)+2].value = "thirds"
wks.update_cells(cell_list)

# for count in range(0,len(persons)):
# 	print persons[count]
# 	wks.update_acell('A%s'%(count+1), "%s"%persons[count])



# wks = gc.open("timetrackdjango").sheet1

# wks.update_acell('B2', "it's down there somewhere, let me take another look.")


