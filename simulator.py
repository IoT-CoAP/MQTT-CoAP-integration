import Tkinter as tk
import paho.mqtt.client as mqtt
from threading import Thread
import json

broker = "localhost"
client = mqtt.Client(client_id="c1",clean_session=False)
client.loop_start()
client.connect(broker)

root = tk.Tk()
root.geometry('%dx%d+%d+%d'%(370,250,200,150))
root.title('Node-Simulator')

w = tk.Label(root,text="rt :",fg="black").grid(row=0)
w = tk.Label(root,text="bn :",fg="black").grid(row=1)
w = tk.Label(root,text="id :",fg="black").grid(row=2)
w = tk.Label(root,text="---Parameters---",fg="black").grid(row=3)
w = tk.Label(root,text="Parameter name :",fg="black").grid(row=4)
w = tk.Label(root,text="Parameter value :",fg="black").grid(row=5)
w = tk.Label(root,text="Parameter Unit :",fg="black").grid(row=6)

var = tk.StringVar(root)
var.set("choose resource type")

var2 = tk.StringVar(root)
var2.set("choose base name")

#w = tk.Label(root,text="value :",fg="black").grid(row=1)


#text1 = tk.Entry(root)
#text1.grid(row=1,column=1)

text2 = tk.Entry(root)
text2.grid(row=2,column=1)

text3 = tk.Entry(root)
text3.grid(row=4,column=1)

text4 = tk.Entry(root)
text4.grid(row=5,column=1)

text5 = tk.Entry(root)
text5.grid(row=6,column=1)


rt_list=["","oic.r.temperature","oic.r.humidity"]
option = tk.OptionMenu(root,var,*rt_list).grid(row=0,column=1)

bn_list=["","IIITb/IoTLab/test/temperature","IIITb/IoTLab/test/humidity"]
option2 = tk.OptionMenu(root,var2,*bn_list).grid(row=1,column=1)


def endclient():
  global client
  while 1:
    try:
      pass
    except KeyboardInterrupt:
      client.disconnect()
      exit()

def select():
  global var,var2,text2,text3,text4,text5,client
  payload={}
  payload["rt"]=var.get()
  payload["bn"]=var2.get()
  payload["id"]=text2.get()
  payload["e"]=[{"n":text3.get(),"v":text4.get(),"u":text5.get()}]
  rc=client.publish(payload['bn'],json.dumps(payload),retain=True)
  print ("rc=",rc)
  #print var.get()
  #print text1.get()
  print (payload)

if __name__ == '__main__':
  thread = Thread(target = endclient)
  thread.setDaemon(True)
  thread.start()
  button = tk.Button(root,text="Create",command=lambda: select()).grid(row=7,column=2)
  
  
  root.mainloop()
