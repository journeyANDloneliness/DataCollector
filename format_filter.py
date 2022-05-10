import re
import copy
from pymaybe import maybe
global data

data=	{
		"type" : 0,
		"remote" :-1,
		"tags" : [],
    "job_id":-1,
    "dicord_id":-1,
    "user":-1,
    "full_message":"",
    "summary":{
      "contact":"",
      "sallary":{},
      "fullfiled":{}
    },
    "manage":{
      "reviews":[],
      "update":[],
      "created_date":-1,
      "deleted_date":-1,
      "expire":False,
      "expire_date":-1
    }
}
data_hire={
		"contact" : "test@gmail.com",
		"sallary" : {
			"each" : "week",
			"amount" : "$1"
		}
	}

data_hiring={
		"contact" : "hiring@gmail.com",
		"sallary" : {
			"each" : "week",
			"amount" : "$1"
		}
	}


def make_data(str):
  dt=copy.deepcopy(data)
  clear=re.sub(r"\n> ","\n",str)
  ls = re.split(r"\n(?=.*:.*)",clear)
  dt["full_message"]=clear

  get_tag(dt,ls[0])
  get_info(dt,ls[1:])
  fail =True
  #print(dt)
  return dt
  
def get_info(dt,ls):
  for i,v in enumerate(ls):
    ls[i]=v.split(":")
  for i in ls:
    if i[0] in dt:
      dt["summary"][i[0]] = i[1]
    else:
      dt["summary"][i[0]] = i[1]
      
      

def get_tag(dt,str):


  ls =  re.split(r"(?:\B|\b)(?=\[.+\])",str)
  if len(ls) < 1:
    return False
  for tag in ls:
    if "hire" in tag.lower():
      dt["type"] =1
      dt={**dt,**data_hire}
    elif "hiring" in tag.lower():
      dt["type"] =2
      print("in hiring tag")
      dt={**dt,**data_hiring}
    elif tag != "":
      dt["tags"].append(re.sub(r"[\[\]\n]","",tag))
   

  if dt["type"] == 0:
    return False

  return True

def check_format(data):
  out=""
  if data["type"]==0:
    out="❌ either [hire] or [hiring] tag is required\n"
  if len(data)<8:
    out+="❌ your jobs contains too little information\n"

  if out!="":
    out+="❌ your job didn't passed format checker. please review again your post. see pinned message."
    return out
    