from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP
from threading import Thread
from coapthon import defines
import sys,json
from rdflib import Graph,URIRef,Namespace,RDF,Literal,XSD

def parse_Sensor_Graph():
  g=Graph()
  g.parse("sensor.ttl",format="turtle")
  SOSA = Namespace("http://www.w3.org/ns/sosa/")
  g.bind('sosa',SOSA)
  return g

def parse_Actuator_Graph():
  g=Graph()
  g.parse("actuator.ttl",format="turtle")
  SOSA = Namespace("http://www.w3.org/ns/sosa/")
  g.bind('sosa',SOSA)
  return g

class temperature(Resource):
  
  def __init__(self,name="Sensor",coap_server=None,uid='xme2340'):
    super(temperature,self).__init__(name,coap_server,visible=True,observable=True,allow_children=True)
    self.pay={"rt":["oic.r.temperature"],"id":uid,"temperature":20.0,"units":"C","range":[0.0,100.0]}
    self.resource_type = "oic.r.temperature"
    self.content_type = "application/json"
    self.interface_type = "oic.if.a"

  def render_GET(self,request):
    g=parse_Sensor_Graph()
    q="{} sosa:hasSimpleResult ?val .".format("<coap://observation/temperature/"+self.pay['id']+">")
    q="{"+q+"}"

    qres = g.query(
    """SELECT ?val
          WHERE {}""".format(q))
    for row in qres.bindings:
            #print row['val']
            self.pay["temperature"]=row['val'].split()[-2]
    self.payload = (defines.Content_types["application/json"], json.dumps(self.pay))
    return self

class humidity(Resource):
   
   def __init__(self,name="Res",coap_server=None,uid='bmp3400'):
      super(humidity,self).__init__(name,coap_server,visible=True,observable=True,allow_children=True)
      self.pay={"rt":["oic.r.humidity"],"id":uid,"humidity":40,"desiredHumidity":40}
      self.resource_type = "oic.r.humidity"
      self.content_type = "application/json"
      self.interface_type = "oic.if.a"

   def render_GET(self,request):
    g=parse_Actuator_Graph()
    q="{} sosa:hasSimpleResult ?val .".format("<coap://observation/humidity/"+self.pay['id']+">")
    q="{"+q+"}"

    qres = g.query(
    """SELECT ?val
          WHERE {}""".format(q))
    for row in qres.bindings:
            self.pay["humidity"]=row['val'].split()[-2]
    self.payload = (defines.Content_types["application/json"], json.dumps(self.pay))
      #self.payload = (defines.Content_types["application/json"], json.dumps(value))
    return self

    def render_PUT(self,request):
     g=parse_Actuator_Graph()


