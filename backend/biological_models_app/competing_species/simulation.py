"""
Two Competing Species Simulation
"""
import numpy as np
from collections import deque 
import math

class CompetingSpeciesSimulation:

    def __init__(self, sim_params):
        self.N1 = deque([]) #Holds population 1 values
        self.N1_out = deque([]) #Population 1 values to be outputted
        self.N2 = deque([]) #Holds population 2 values
        self.N1_out = deque([]) #Population 2 values to be outputted
        #Model params
        #Species 1
        self.N1_0 = sim_params[0]
        self.r1 = sim_params[1] #Growth rate 1 [1/yr]
        self.k1 = sim_params[2] #Carrying capacity 1
        self.a1 = sim_params[3] #Competition from species 2 [1/yr]
        #Species 2
        self.N2_0 = sim_params[4]
        self.r2 = sim_params[5] #Growth rate 2
        self.k2 = sim_params[6] #Carrying capacity 2
        self.a2 = sim_params[7] #Competition from species 1 [1/yr]
        
        #Simulation params
        self.dt = 0.0005 #Integration step size [yr]
        self.output_dt = 0.01 #Output step size [yr]
        self.max_t = 30 #[yr]
        
    def Euler_method(self, step, output_step):
        #ODEs
        dN1dt = self.r1*self.N1[-1]*(1-(self.N1[-1] + self.a1*self.N2[-1])/self.k1)
        dN2dt = self.r2*self.N2[-1]*(1-(self.N2[-1] + self.a2*self.N1[-1])/self.k2)
        #Euler method and append to data array
        self.N1.append(dN1dt*self.dt + self.N1[-1])
        self.N2.append(dN2dt*self.dt + self.N2[-1])
        if step % output_step == 0: #Only output on output steps
            self.N1_out.append(self.N1[-1])
            self.N2_out.append(self.N2[-1])

    def run_sim(self):
        #Set initial values
        self.N1.append(self.N1_0)
        self.N1_out.append(self.N1_0)
        self.N2.append(self.N2_0)
        self.N2_out.append(self.N2_0)

        #Convert from time steps to integer step
        max_step = int(round(self.max_t/self.dt))
        output_step = int(round(self.output_dt/self.dt)) #Number of solver steps between output steps

        for step in range(1, max_step, 1):
            self.Euler_method(step, output_step)

def runCompetingSpeciesSim(sim_params):
    #Pass params configured by user
    model = CompetingSpeciesSimulation(sim_params)
    model.run_sim()
    return_arrays = [list(model.N1_out), list(model.N2_out)] #Return simulations data
    largest_val = max([max(return_arrays[0]), max(return_arrays[1])]) #Max value obtained throughout sim's output
    upper_bound = math.ceil(largest_val/10)*10 #Round up to nearest 10
    return return_arrays, model.t_axis, upper_bound