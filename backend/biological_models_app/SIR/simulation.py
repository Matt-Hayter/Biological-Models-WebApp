"""
SIR, Disease Spread Simulation
"""
import numpy as np
from collections import deque
import math

class SIRSimulation:
        
    def __init__(self, sim_params):
        self.S = deque([]) #Holds susceptible population values
        self.S_out = deque([]) #S values to be outputted
        self.I = deque([]) #Holds Infectious population values
        self.I_out = deque([]) #I values to be outputted
        self.R = deque([]) #Holds Recovered population values
        self.R_out = deque([]) #R values to be outputted
        self.t_axis = None #Holds time values
        self.dIdt = [-1] #Traced for simulation end time
        #User variable model params
        self.I_0 = sim_params[0] #Initial infections
        self.beta = sim_params[1] #Rate of infection. probability of disease transmission per contact * number of contacts per unit time [days-1]
        recip_gamma = sim_params[2] #Average infectious period, = 1/gamma [days]
        #Model params
        self.R_0 = 0 #Initial recovered
        self.gamma = 1/recip_gamma #Recovery rate of infectious individuals
        self.N_0 = 10000000
        self.S_0 = self.N_0 - self.I_0 #Initial susceptible poulation (10  mil)
        #Simulation params
        self.dt = 0.0005 #Integration step size [days]
        self.output_dt = 0.01 #Output step size [days]
        self.t_max_stop = 2000 #If this time is reached with no infection peak found, end simulation
        
    def Euler_method(self, step, output_step):
        #ODEs
        dSdt = -self.beta*self.S[-1]*self.I[-1]/self.N_0
        self.dIdt.append(self.beta*self.S[-1]*self.I[-1]/self.N_0 - self.gamma*self.I[-1])
        dRdt = self.gamma*self.I[-1]
        
        #Euler method and append to data array
        self.S.append(dSdt*self.dt + self.S[-1])
        self.I.append(self.dIdt[-1]*self.dt + self.I[-1])
        self.R.append(dRdt*self.dt + self.R[-1])

        if step % output_step == 0: #Only output on output steps
          self.S_out.append(self.S[-1])
          self.I_out.append(self.I[-1])
          self.R_out.append(self.R[-1])

    def run_sim(self):
        #Set initial values
        self.S.append(self.S_0)
        self.S_out.append(self.S_0)
        self.I.append(self.I_0)
        self.S_out.append(self.I_0)
        self.R.append(self.R_0)
        self.S_out.append(self.R_0)
        
        #Convert from time steps to integer step
        max_step = int(round(self.t_max_stop/self.dt))
        output_step = int(round(self.output_dt/self.dt)) #Number of solver steps between output steps
        step = 0

        #Perform Euler until infection peak is found
        while True:
            step += 1
            self.Euler_method(step, output_step)
            if self.dIdt[-2] > 0 and self.dIdt[-1] <= 0:
                break
            #If peak hasn't been found before t_max_stop, end sim
            if step >= max_step:
                return
        #After peak is found, perform Euler until infections are low
        while self.I[-1] > 100:
            self.Euler_method()
        
        self.t_axis = list(np.linspace(0, len(self.S_out)*self.output_dt, len(self.S_out)))

def runSIRSim(sim_params):
    model = SIRSimulation(sim_params)
    model.run_sim()
    return_arrays = [list(model.S_out), list(model.I_out), list(model.R_out)] #Return simulations data
    largest_val = max([max(return_arrays[0]), max(return_arrays[1]), max(return_arrays[2])]) #Max value obtained throughout sim's output
    upper_bound = math.ceil(largest_val/10)*10 #Round up to nearest 10
    return return_arrays, model.t_axis, upper_bound