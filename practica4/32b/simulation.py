# Este archivo contiene la implementacion de la clase Simulation (11.11.10)
""" Un objeto de la clase Simulation representa un experimento en el que
se ejecuta un algoritmo distribuido sobre una grafica de comunicaciones """

from process import Process
from simulator import Simulator
# ----------------------------------------------------------------------------------------
class Simulation:                   # Descendiente de la clase "object" (default)
    """ Atributos: "engine", "graph", "table", contiene tambien un
    constructor y los metodos "setModel()", "init()", "run()" """
	
    def __init__(self, filename, maxtime):
        """ construye su motor de simulacion, la grafica de comunicaciones y
        la tabla de procesos """
        self.engine = Simulator(maxtime)

        f = open(filename)
        lines = f.readlines() #tiene todas las lineas
        f.close()
        self.graph = []
        for line in lines:
            fields = line.split() #divide la linea usando espacios
            neighbors = [] #Aquí se guardarán los vecinos del nodo actual.
            for f in fields:
                neighbors.append(int(f))
            self.graph.append(neighbors) #Cada que recorre la linea en el primer for,crea una estrucutra para guardarlos y después esa estructura la guarda en self.graph, entonces self.graph va a contener todos los vecinos de cada nodo

        self.table  = [[]]          # la entrada 0 se deja vacia. self.table es la tabla de procesos 
        for i,row in enumerate(self.graph):
            newprocess = Process(row, self.engine, i+1)
            self.table.append(newprocess)
        		
    def setModel(self, model, id):
        """ asocia al proceso con el modelo que debe ejecutar y viceversa """
        process = self.table[id] #realmente se modifica el objeto Process que vive dentro de self.table porque en Python las variables guardan referencias a objetos, no copias. Los cambios se apĺican directamente al objeto que vive en self.table
        process.setModel(model)
 		
    def init(self, event):
        """ inserta un evento semilla en la agenda """
        self.engine.insertEvent(event)

    def run(self):	
        """ arranca el motor de simulacion """
        while self.engine.isOn():
            nextevent = self.engine.returnEvent()
            target = nextevent.getTarget()
            nextprocess = self.table[target] #se obtiene el proceso al que va dirigido
            nextprocess.setTime(nextevent.getTime()) #Se actualiza el reloj local del proceso que recibe el evento. Es decir el evento nuevo le llega al proceso destino en el tiempo t
            nextprocess.receive(nextevent)
