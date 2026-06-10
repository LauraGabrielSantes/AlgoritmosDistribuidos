#Implementa la simulacion del Algoritmo de recorrido en profundidad de Cheung
import sys
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation


class AlgoritmoDFS(Model):
   def init(self):
     print ("Inicio funciones", self.id)
     print ("Mis vecinos son:", self.neighbors)
     self.visitado=False
     self.padre=self.id  
     self.sinVisitar = self.neighbors
   
   # Aqui se definen las acciones concretas que deben ejecutarse cuando se
   # recibe un evento
   def receive(self, event):
    if event.getName()== "INICIA":
     print ("[", self.id, "]: Recibí INICIA y soy el padre en t=",self.clock," \n")
     self.visitado=True
     self.continuaExploracion()
    elif event.getName()== "DESCUBRE":
      print ("[", self.id, "]: Recibí DESCUBRE de", event.getSource()," en t=",self.clock," \n")
      nodoEmisor=event.getSource()
      if nodoEmisor in self.sinVisitar:
        self.sinVisitar.remove(nodoEmisor)
        print("[", self.id, "]: Actualizo vecinos sin visitar: = ", self.sinVisitar, "\n")
      if not self.visitado:
        self.visitado=True
        self.padre=nodoEmisor
        self.continuaExploracion()
      else:
        newevent = Event("RECHAZO", self.clock + 1.0, nodoEmisor, self.id)
        self.transmit(newevent)
    elif event.getName()=="RECHAZO" or event.getName()=="REGRESA":
      print("[", self.id, "]: Recibí ", event.getName()," de ", event.getSource()," en t=",self.clock," \n")
      self.continuaExploracion()

   
   def continuaExploracion(self):
     if len(self.sinVisitar)>0:
      siguienteNodo=self.sinVisitar.pop(0)
      newevent = Event("DESCUBRE", self.clock + 1.0, siguienteNodo, self.id)
      self.transmit(newevent)
     else: 
      if self.id != self.padre:
       print("[",self.id,"]: Ya no tengo nodos que visitar, envío regreso a padre \n")
       newevent = Event("REGRESA", self.clock + 1.0, self.padre, self.id)
       self.transmit(newevent)
      else:
       print("[", self.id,"]: Termina exploración en t=",self.clock," \n")


