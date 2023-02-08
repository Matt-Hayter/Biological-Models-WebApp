"""
Predator-Prey (Lotka-Voltera) Simulation
"""
import numpy as np
from collections import deque

class PredatorPreySimulation:
        
    def __init__(self, sim_params):
        """
        Param bar: 
            2 cards: Predator, Prey
            - Prey: N_0, a: Reproduction rate. b: Impact of predation on prey.
              Pred: P_0, c: Rate of growth of predator poopulation, in response to prey. d: natural death rate
            - Save Config button
        In footer:
            Interesting configs
            Presets
        """
        self.N = deque([]) #Holds prey population values
        self.P = deque([]) #Holds predator population values
        self.dNdt = [1] #Traced for simulation end time
        self.t_axis = None #Holds time values
        #Model params:
        #Prey:
        self.N_0 = sim_params[0]
        self.a = sim_params[1] #Prey natural reproduction rate [1/yr] = births - natural deaths
        self.b = sim_params[2] #Rate of predator consuming prey [1/yr]
        #Predator:
        self.P_0 = sim_params[3]
        self.c = sim_params[4] #Predator reproduction rate after consuming prey
        self.d = sim_params[5] #Predator natural death rate
        #Simulation params
        self.dt = 0.001 #Integration step size [yr]
        self.max_troughs = 4 #Length of simulations if oscillating
        self.t_max_stop = 1000 #max length of time before sim auto stops [years]
        
    def Euler_method(self):
        """
        Calculate ODE's rate and then apply Euler method
        """
        #ODEs
        self.dNdt.append(self.N[-1]*(self.a - self.b*self.P[-1]))
        dPdt = self.P[-1]*(self.c*self.N[-1] - self.d)
        #Euler method and append to data array
        self.N.append(self.dNdt[-1]*self.dt + self.N[-1])
        self.P.append(dPdt*self.dt + self.P[-1])

    def run_sim(self):
        """
        Run Euler iterations for each time step until max_t
        """
        self.N.append(self.N_0)
        self.P.append(self.P_0)
        
        t = 0
        #Perform Euler until first prey trough is found
        while True:
            t += self.dt
            self.Euler_method()
            if self.dNdt[-2] < 0 and self.dNdt[-1] >= 0:
                break
            #If peak hasn't been found before t_max_stop, end sim
            if t >= self.t_max_stop:
                return

        self.t_axis = np.linspace(0, len(self.N)*self.dt, len(self.N))
            
        #Continue iterations now first trough is found
        trough_counter = 1
        while trough_counter < self.max_troughs: #End simulation when desired through is found
            t += self.dt
            self.Euler_method()
            if self.dNdt[-2] < 0 and self.dNdt[-1] >= 0: #Count troughs as they are passed
                trough_counter += 1
        
def runPredPreySim(sim_params):
    #Pass parameters configured by user
    model = PredatorPreySimulation(sim_params)
    model.run_sim()
    return_arrays = [list(model.N), list(model.P)] #Return simulations data
    largest_val = max([max(model.N), max(model.P)]) #Max value obtained throughout sim
    return return_arrays, largest_val
    