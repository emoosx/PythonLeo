import re
import os
import PythonLeo
from Tkinter import *
import threading

URL_LIST = {"current_module":"http://leo.rp.edu.sg/workspace/studentModule.asp?", #to get project_id , group_id
				"current_problem":"http://leo3.rp.edu.sg//projectweb/project_menu.asp?", #to get topic_id, year2,3=>leo3, year1=>leo1
				"problem_download":"http://leo.rp.edu.sg/projectweb/projectupload/savefolderas.asp?folder=/databank/projectbank/"
};

def download():
	response.set("Connecting") 
	leo = PythonLeo.PythonLeo(username_field.get(),password_field.get()) #e.g. 91224, 12345
	project_id_list = leo.parse_id("projectid",leo.open_url(URL_LIST["current_module"]))
	group_id_list = leo.parse_id("groupid",leo.open_url(URL_LIST["current_module"]))
	topic_id_list = leo.parse_id("topicid",leo.open_url(URL_LIST["current_problem"]+
										"projectid="+str(project_id_list[-1])+
										"&groupid="+str(group_id_list[-1])))
										
	get_download_url = leo.open_url(URL_LIST["problem_download"]+topic_id_list[-1])
	
	download_url = "http://leo.rp.edu.sg"+ re.search('HREF=\"(.+?zip)',get_download_url.read()).groups()[0]
	print download_url
	response.set("Downloading")
	os.chdir(os.path.expanduser("~/Desktop"))
	zip_file = open("problem.zip","wb")
	zip_file.write(	leo.open_url(download_url).read() )
	zip_file.close()
	
	response.set("Done!")
	
def download_thread(dummy=1):	
	threading.Thread(target=download).start()

if __name__ == "__main__":
	root = Tk()
	root.title("LEO PS Downloader")
	
	main_frame = Frame(root,width=200,height=120)
	main_frame.grid(column=0,row=0)
	
	username_label = Label(main_frame, text="Username")
	username_label.grid(column=0,row=0)
	
	username_field =Entry(main_frame)
	username_field.grid(column=1,row=0,columnspan=2)
	
	password_label = Label(main_frame, text="Password")
	password_label.grid(column=0,row=1)
	
	password_field =Entry(main_frame,show="*")
	password_field.grid(column=1,row=1,columnspan=2)
	password_field.bind("<Return>",download_thread)
	
	response = StringVar()
	response.set("")
	
	response_label = Label(main_frame, textvariable=response,fg="red",anchor=W,justify=LEFT)
	response_label.grid(column=0,row=2)

	dl_button = Button(main_frame,text="Download",command=download_thread)
	dl_button.grid(column=2,row=2)
	
	root.mainloop()

	
	
	
	
	