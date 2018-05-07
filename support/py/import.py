import login
import re, os, sys
from io import StringIO, BytesIO
from time import strftime

def browse_panel():
	URL = "https://cusis.cuhk.edu.hk/psc/csprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL"
	payload = {'ICType':'Panel'}
	r = cusis.session.post(URL, data=payload)
	return r.status_code


def browse_scheduler():
	URL = "https://cusis.cuhk.edu.hk/psc/csprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL"
	semester_code = '1845' 	#You should find semester code in Cusis system and put it here yourself. (2014-15 sem 1 => 1835)
	payload = {
		'ICType':'Panel',
		'ICAction':'DERIVED_SSS_SCT_SSR_PB_GO',
		'SSR_DUMMY_RECV1$sels$0' : '0'
	}
	r = cusis.session.post(URL,data=payload)
	return r.status_code

def dumplist(tofile):
	URL = "https://cusis.cuhk.edu.hk/psc/csprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL"
	payload = {'ICType':'Panel','ICAction':'DERIVED_REGFRM1_SA_LINK_PRINTER'}
	r = cusis.session.post(URL,data=payload)

	course_info = re.findall(r"<table cellspacing='0' (.+?)</table>", r.text, re.DOTALL)
	course_name = re.findall(r"<td class='PAGROUPDIVIDER' align='left'>(.+?)</td>", r.text)
	print(course_name)
	course_num = len(course_name)
	with open(tofile,'w') as f:
		f.write(''' 
<html dir='ltr' lang='en'>
<!-- Copyright (c) 2000, 2007, Oracle. All rights reserved. -->
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><body><table border='1' cellpadding='3' cellspacing='0'>
<tr>
<th>Course Name</th><th>Status</th><th>Units</th><th>thGrading</th>
<th>Class Nbr</th><th>Section</th>
<th>Component</th><th>Days & Times</th>
<th>Room</th><th>Instructor</th>
<th>Start/End Date</th>
</tr>
''')
		i = 0
		new_entry = True
		for entry in course_info:
			l = re.findall(r"(?:<span  class=.+?>(.+?)</span>|<td align='CENTER'  class='PSLEVEL3GRIDROW' >(.+?)</td>)", entry, re.DOTALL)
			flat_list = [item for sublist in l for item in sublist]
			item = [x for x in filter(None, flat_list)]
			if len(item) == 4:
				new_entry = True
				f.write("<tr>\n")
				f.write("<td>" + course_name[i] + "</td>\n")
				i += 1
				for col in item[0:3]:
					if col == "&nbsp;":
						col = ""
					f.write("<td>" + col + "</td>\n")
			else:
				for k in range(len(item)//7):
					if k != 0:
						f.write("<tr>\n")
						for j in range(4):
							f.write("<td>""</td>\n")
					for col in item[7*k : 7*(k+1)]:
						if col == "&nbsp;":
							col = ""
						f.write("<td>" + col + "</td>\n")


def main():
	browse_panel()
	browse_scheduler()
	dumplist("a.xls")

if __name__ == '__main__':
	cusis = login.Cusis()
	cusis.login(sys.argv[1], sys.argv[2])
	main()