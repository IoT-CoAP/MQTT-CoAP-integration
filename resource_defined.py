import paho.mqtt.client as mqtt
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP
from threading import Thread
from coapthon import defines
import sys,json
import thingsv3 as t

ser=None
object_list = []

def on_connect(client, userdata, flags, rc):
        print ("connected to broker...")
        client.subscribe([("IITM/ComLab/test/#", 1)])   

def choose(val,ide):
  if val == "oic.r.temperature":
    return t.temperature(uid=ide)
  else :
    return t.humidity(uid=ide)


def callback(client, userdata, msg):
  payload=json.loads(msg.payload)
  global ser,object_list
  r_list = {"oic.r.temperature":t.temperature(),"oic.r.humidity":t.humidity()}
  uid=str(payload['id'])
  name = str(payload['bn']).split('/')
  name = name[-1]+"_"+str(uid)
  if uid not in object_list :
    object_list.append(uid)
    #obj=globals()[str(r_list[str(payload['rt'])])+"(uid={})".format("'"+uid+"'")]
    #obj = choose(str(payload['rt']),uid)
    obj = r_list[str(payload['rt'])]
    obj.pay['id']=uid
    ser.add_resource("/"+str(name), obj)
    print (ser.root.dump())

class CoAPServer(CoAP):
  def __init__(self, host, port, multicast=False):
    CoAP.__init__(self,(host,port),multicast)
    self.add_resource('sens-Me/',t.temperature())
    self.add_resource('act-Me/',t.humidity())
    print ("CoAP server started on {}:{}".format(str(host),str(port)))
    print (self.root.dump())

def main():
  global ser
  ip = "0.0.0.0"
  port = 5683
  multicast=False

  server = CoAPServer(ip,port,multicast)
  ser=server
  broker = "localhost"
  client = mqtt.Client(client_id="resource_creator",clean_session=False)
  client.on_connect = on_connect
  client.on_message = callback
  try:
        client.connect('localhost')
  except:
        print ("ERROR: Could not connect to MQTT")

  client.loop_start()

  try:
    server.listen(10)
    
  except KeyboardInterrupt:
    print ("Closing Server...")
    print (server.root.dump())
    client.loop_stop()
    client.disconnect()
    server.close()
    sys.exit()

if __name__=="__main__":
  main()
