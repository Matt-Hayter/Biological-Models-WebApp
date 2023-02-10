"""
Predator-Prey (Lotka-Voltera) Simulation
"""
import numpy as np
from collections import deque
import math

class PredatorPreySimulation:
        
    def __init__(self, sim_params):
        """
        Declare and initialise simulation's data
        """
        self.N = deque([]) #Holds prey population values
        self.N_out = deque([]) #For outputted steps
        self.P = deque([]) #Holds predator population values
        self.P_out = deque([]) #For outputted steps
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
        self.dt = 0.0005 #Integration step size [yr]
        self.output_dt = 0.01 #Output step size [yr]
        self.max_troughs = 6 #Length of simulations if oscillating
        self.t_max_stop = 600 #max length of time before sim auto stops [years]
        
    def Euler_method(self, step, output_step):
        """
        Calculate ODE's rates, apply Euler method, then add to output queue if required
        """
        #ODEs
        self.dNdt.append(self.N[-1]*(self.a - self.b*self.P[-1]))
        dPdt = self.P[-1]*(self.c*self.N[-1] - self.d)
        #Euler method and append to data array
        self.N.append(self.dNdt[-1]*self.dt + self.N[-1])
        self.P.append(dPdt*self.dt + self.P[-1])
        if step % output_step == 0: #Only output on output steps
            self.N_out.append(self.N[-1])
            self.P_out.append(self.P[-1])

    def run_sim(self):
        """
        Initiate simulation and run Euler iterations for each time step,
        dynamically checking for simulation end points
        """
        self.N.append(self.N_0)
        self.N_out.append(self.N_0)
        self.P.append(self.P_0)
        self.P_out.append(self.P_0)

        #Convert from time steps to integer step
        step = 0
        max_step = int(round(self.t_max_stop/self.dt))
        output_step = int(round(self.output_dt/self.dt)) #Number of solver steps between output steps
        #Perform Euler until first prey trough is found
        while True:
            step += 1
            self.Euler_method(step, output_step)
            if self.dNdt[-2] < 0 and self.dNdt[-1] >= 0:
                break
            #If peak hasn't been found before t_max_stop, end sim
            if step >= max_step:
                return
            
        #Continue iterations now first trough is found
        trough_counter = 1
        while trough_counter < self.max_troughs: #End simulation when desired through is found
            step += 1
            self.Euler_method(step, output_step)
            if self.dNdt[-2] < 0 and self.dNdt[-1] >= 0: #Count troughs as they are passed
                trough_counter += 1
        
        self.t_axis = list(np.linspace(0, len(self.N_out)*self.output_dt, len(self.N_out)))
        
def runPredPreySim(sim_params):
    #Pass parameters configured by user
    model = PredatorPreySimulation(sim_params)
    model.run_sim()
    return_arrays = [list(model.N_out), list(model.P_out)] #Return simulations data
    largest_val = max([max(return_arrays[0]), max(return_arrays[1])]) #Max value obtained throughout sim's output
    upper_bound = math.ceil(largest_val/10)*10 #Round up to nearest 10
    return return_arrays, model.t_axis, upper_bound
    