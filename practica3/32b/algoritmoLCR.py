import sys
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation


class AlgoritmoLCR(Model):
  # Esta clase desciende de la clase Model e implementa los metodos 
  # "init()" y "receive()", que en la clase madre se definen como abstractos
  contadorMensajes=0
  def init(self):
    # Aqui se definen e inicializan los atributos particulares del algoritmo
    print ("Inicio funciones", self.id)
    self.sucesor = self.neighbors[0]
    print ("Mi vecino es:", self.sucesor)
    self.lider=0
    self.CandidaturaLanzada=False

  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    if event.getName()[0] == "INICIA":
       print ("[", self.id, "]: recibi INICIA en t=",self.clock," \n")
       self.CandidaturaLanzada=True
       self.enviaCandidatura(self.id)
    elif  event.getName()[0] == "CANDIDATURA" :
       AlgoritmoLCR.contadorMensajes += 1
       if (self.id < event.getName()[1]):
          print("[", self.id, "]: Reenvío la candidatura de ", event.getName()[1], " en t= ", self.clock,"\n" )
          self.enviaCandidatura(event.getName()[1])       
       elif (self.id > event.getName()[1]):
          if (self.CandidaturaLanzada==False):
            print("[", self.id, "]:He recibido la candidatura de ", event.getName()[1], " en t= ", self.clock,"\n" )
            self.CandidaturaLanzada==True
            self.enviaCandidatura(self.id)
          else:
             print("[", self.id, "]: Soy un nodo despierto y detengo la candidatura de ", event.getName()[1], " en t= ", self.clock,"\n" )             
       elif (self.id == event.getName()[1]):
          print("[", self.id, "]: ¡He recibido mi candidatura en t= ", self.clock," !\n" )
          self.enviaElecto(self.id)
    elif event.getName()[0] == "ELECTO" :
       AlgoritmoLCR.contadorMensajes +=1
       if(self.id != event.getName()[1]):
          print("[",self.id,"]: ", event.getName()[1] ," ha ganado la elección en", self.clock," \n")
          self.enviaElecto(event.getName()[1])
       else:
          print("[", self.id,"]: He sido electo en ", self.clock,"\n")
          
  
  def enviaCandidatura(self, id):
     candidatura=("CANDIDATURA", id)
     newevent = Event(candidatura, self.clock + 1.0, self.sucesor, self.id)
     self.transmit(newevent)
  
  def enviaElecto(self, id):
     self.lider=id
     self.CandidaturaLanzada=False
     electo=("ELECTO", id)
     newevent = Event(electo, self.clock + 1.0, self.sucesor, self.id)
     self.transmit(newevent)