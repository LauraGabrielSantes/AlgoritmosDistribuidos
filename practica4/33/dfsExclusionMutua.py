#Implementa la simulacion del Algoritmo de recorrido en profundidad de Cheung
import sys
import random
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation

class RecursoCompartido():
    articulos=30

class AlgoritmoDFSExclusionMutua(Model):
   def __init__(self, recursoCompartido=None):
     self.recursoCompartido= recursoCompartido
   contadorMensajes=0
   
   def init(self):
     print ("Inicio funciones", self.id)
     self.sucesor = self.neighbors[0]
     print ("Mis vecinos son:", self.neighbors)
     self.visitado=False
     self.padre=self.id
     self.sinVisitar= self.neighbors
     self.solicitud_sc=False
     
   # Aqui se definen las acciones concretas que deben ejecutarse cuando se
   # recibe un evento
   def receive(self, event):
    if event.getName()== "INICIA":
     print("\n\nArtículos al comienzo de la simulación =", self.recursoCompartido.articulos,"\n\n")
     print ("[", self.id, "]: recibi INICIA y soy el padre en t=",self.clock," \n")
     self.visitado=True
     self.padre=self.id
     self.solicitd()
    elif event.getName()== "DESCUBRE":
      AlgoritmoDFSExclusionMutua.contadorMensajes+=1
      print ("[", self.id, "]: recibi DESCUBRE de", event.getSource()," en t=",self.clock," \n")
      nodoEmisor=event.getSource()
      if nodoEmisor in self.sinVisitar:
        self.sinVisitar.remove(nodoEmisor)
        print("[", self.id, "]:Actualizo vecinos sin Visitar: = ", self.sinVisitar, "\n")
      if not self.visitado:
        self.visitado=True
        self.padre=nodoEmisor
        self.solicitd()
      else:
        newevent = Event("RECHAZO", self.clock + 1.0, nodoEmisor, self.id)
        self.transmit(newevent)
    elif event.getName()=="RECHAZO" or event.getName()=="REGRESA":
      AlgoritmoDFSExclusionMutua.contadorMensajes+=1
      print("[", self.id, "]: Recibí ", event.getName()," de ", event.getSource()," en t=",self.clock," \n")
      self.continuaExploracion()
    elif event.getName() == "SOLICITUD":
      AlgoritmoDFSExclusionMutua.contadorMensajes+=1
      self.solicitud_sc=True
      print("[",self.id,"]: Solicitaré artículos\n")
    elif event.getName() == "OK":
      AlgoritmoDFSExclusionMutua.contadorMensajes+=1
      articulosObtenidos=random.randint(1,5)
      self.recursoCompartido.articulos = self.recursoCompartido.articulos - articulosObtenidos
      print("[", self.id,"]: Obteniendo ", articulosObtenidos," artículos en t=",self.clock," \n")
      self.unlock()
    elif event.getName() == "LIBERA":
      AlgoritmoDFSExclusionMutua.contadorMensajes+=1
      self.solicitud_sc=False
      print("[", self.id,"]: LIBERANDO la sección crítica en t=",self.clock," \n")
      self.continuaExploracion()  
   
   def solicitd(self):
     if self.solicitud_sc:
       self.lock()
     else:
       self.continuaExploracion()
    
   def lock(self):
    newevent = Event("OK", self.clock + 1.0, self.id , self.id)
    self.transmit(newevent)
   
   def unlock(self):
    newevent = Event("LIBERA", self.clock + 1.0, self.id , self.id)
    self.transmit(newevent)       
     
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


