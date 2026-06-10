import sys
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation

# Esta clase desciende de la clase Model e implementa los metodos 
# "init()" y "receive()", que en la clase madre se definen como abstractos
class AlgoritmoHS(Model):
  contadorMensajes=0
  def init(self):
    # Aqui se definen e inicializan los atributos particulares del algoritmo
    print ("Inicio funciones", self.id)
    self.sucesor = self.neighbors
    print ("Mis vecinos son:", self.sucesor[0], " y ",self.sucesor[1])
    self.lider=0
    self.electoLanzado=False
    self.ronda=-1
    self.victorias=0

  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    nodoEmisor=event.getSource()
    if event.getName()[0] == "INICIA":
       print ("[", self.id, "]: recibi INICIA en t=",self.clock," \n")
       self.inicioRonda(self.id)

    if  event.getName()[0] == "CANDIDATURA" :
       AlgoritmoHS.contadorMensajes += 1
       candidato_actual= event.getName()[1]
       print("[", self.id, "]: Recibí la candidatura de ",candidato_actual, " proveniente de  ", nodoEmisor," en t = ", self.clock,"\n")
       self.distancia= event.getName()[2]
       self.distancia -=1
       
       if (self.id > candidato_actual and self.ronda == -1):
          self.inicioRonda(self.id)
       elif (self.id < candidato_actual):
          if(self.distancia > 0):
             candidato=["CANDIDATURA",candidato_actual,self.distancia]
             #Se envia por el lado contrario
             proximoSucesor = self.sucesor[0] if self.sucesor[0] != nodoEmisor else self.sucesor[1]
             newevent = Event(candidato, self.clock + 1.0, proximoSucesor, self.id)
             self.transmit(newevent) 
          else:
             ganadorRonda=["GANADOR_RONDA", candidato_actual, None]
             #se envia por el mismo lado
             proximoSucesor = self.sucesor[0] if self.sucesor[0] == nodoEmisor else self.sucesor[1]
             newevent = Event(ganadorRonda, self.clock + 1.0, proximoSucesor, self.id)
             self.transmit(newevent)
       elif (self.id == candidato_actual and not self.electoLanzado):
          print ("[", self.id,"]: ¡Es mi candidatura! Avisaré a todos los nodos  \n")
          self.electoLanzado = True
          electo=["ELECTO", self.id, None]
          #Se envia por el lado contrario
          proximoSucesor=self.sucesor[0] if self.sucesor[0]!= nodoEmisor else self.sucesor[1]
          newevent = Event (electo, self.clock + 1.0, proximoSucesor, self.id)
          self.transmit(newevent)
    elif event.getName()[0] == "GANADOR_RONDA":
     AlgoritmoHS.contadorMensajes += 1
     ganador_actual= event.getName()[1]
     print ("[", self.id,"]: *Recibí el ganador de la ronda: ", ganador_actual," proveniente de  ", nodoEmisor, " en t = ", self.clock,"\n")
     if(self.id == ganador_actual):
      self.victorias += 1
      if self.victorias == 2:
        self.inicioRonda(self.id)
     else:
       ganadorRonda=["GANADOR_RONDA", ganador_actual, None]
       #Se envía por el lado contrario
       proximoSucesor = self.sucesor[0] if nodoEmisor != self.sucesor[0] else self.sucesor[1]
       newevent = Event (ganadorRonda, self.clock + 1.0, proximoSucesor, self.id)
       self.transmit(newevent)
    elif event.getName()[0] == "ELECTO":
      AlgoritmoHS.contadorMensajes += 1
      self.ronda=-1
      self.lider = event.getName()[1]
      print ("[", self.id,"]: El lider es: ", self.lider,  ", t = ",self.clock,"\n")
      if (self.id != self.lider):
        electo=["ELECTO", self.lider, None]
        #Se envía por el lado contrario
        proximoSucesor = self.sucesor[0] if nodoEmisor != self.sucesor[0] else self.sucesor[1]
        newevent = Event (electo, self.clock + 1.0, proximoSucesor, self.id)
        self.transmit(newevent)
      else:
        self.electoLanzado = False
        print ("[", self.id,"]: ¡He sido Electo ^u^! en ", self.clock,"\n")
          
            
    
  def inicioRonda(self, id_candidato):
     self.ronda+=1
     self.victorias=0
     distancia=2**self.ronda
     vecinos=self.sucesor
     antecesor=vecinos[0]
     sucesor=vecinos[1]
     candidato=["CANDIDATURA",id_candidato,distancia]
     print("[", self.id, "]: COMIENZA RONDA ", self.ronda,"\n")
     newevent = Event(candidato, self.clock + 1.0, antecesor, self.id)
     self.transmit(newevent)
     newevent = Event(candidato, self.clock + 1.0, sucesor, self.id)
     self.transmit(newevent)