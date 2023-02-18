"""
SEIDR simulation
"""
import numpy as np
from collections import deque
import math

class SIRSimulation:
        
    def __init__(self, sim_params):
        self.S = deque([]) #Holds susceptible population values
        self.S_out = deque([]) #S values to be outputted
        self.E = deque([]) #Infected but not yet infectious
        self.E_out = deque([]) #E values to be outputted
        self.I = deque([]) #Holds Infectious population values
        self.I_out = deque([]) #I values to be outputted
        self.D = deque([]) #Holds Dead population values
        self.D_out = deque([]) #D values to be outputted
        self.R = deque([]) #Holds Recovered population values. Recovered individuals are permanently immune
        self.R_out = deque([]) #R values to be outputted
        self.N = deque([]) #Total population
        self.t_axis = deque([]) #Holds time values
        self.dIdt = [-1] #Traced for simulation end time
        #User-variable model params
        self.alpha = sim_params[0] #Disease induced average lethality rate [days-1]
        self.beta = sim_params[1] # Average Rate of infection. probability of disease transmission per contact * number of contacts per unit time
        recip_gamma = sim_params[2] #Average infectious period, = 1/gamma [days]
        recip_epsilon = sim_params[3] #Average incubation period, period between exposure to disease and appearence of first sympotoms. = 1/epsilon [days]
        self.E_0 = sim_params[4] #Initial exposed population
        self.I_0 = sim_params[5] #Initial infectious
        #Model params
        self.N_0 = 10000000 #Initial total poulation (10  mil)
        self.S_0 = self.N_0 - self.E_0 - self.I_0
        self.D_0 = 0
        self.R_0 = 0
        self.epsilon = 1/recip_epsilon #Rate of progression from exposed to infectious
        self.gamma = 1/recip_gamma #Recovery rate of infectious individuals
        recip_mu = 80*365 #Natural life expectancy per capita [days]
        self.mu = 1/recip_mu #Birth rate per capita
        self.Lambda = self.mu*self.N_0 #Per capita birth rate. Births and natural deaths are balanced here
        #Simulation params
        self.dt = 0.01 #Integration step size [days]
        self.output_dt = 0.01 #Minimum output step size [days]
        self.t_max_stop = 2000 #If this time is reached with no infection peak found, end simulation
        
        
    def Euler_method(self, step, output_step):
        #ODEs
        dSdt = self.Lambda - self.mu*self.S[-1] - self.beta*self.S[-1]*self.I[-1]/self.N[-1]
        dEdt = self.beta*self.S[-1]*self.I[-1]/self.N[-1] - (self.mu + self.epsilon)*self.E[-1]
        self.dIdt.append(self.epsilon*self.E[-1] - (self.gamma + self.mu + self.alpha)*self.I[-1])
        dDdt = self.alpha*self.I[-1]
        dRdt = self.gamma*self.I[-1] - self.mu*self.R[-1]
        
        #Euler method and append to data array
        self.S.append(dSdt*self.dt + self.S[-1])
        self.E.append(dEdt*self.dt + self.E[-1])
        self.I.append(self.dIdt[-1]*self.dt + self.I[-1])
        self.D.append(dDdt*self.dt + self.D[-1])
        self.R.append(dRdt*self.dt + self.R[-1])
        self.N.append(self.S[-1] + self.E[-1] + self.I[-1] + self.R[-1])
        
    def run_sim(self):
        self.S.append(self.S_0)
        self.E.append(self.E_0)
        self.I.append(self.I_0)
        self.D.append(self.D_0)
        self.R.append(self.R_0)
        self.N.append(self.N_0)
        
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
            self.Euler_method(step, output_step)

    def obtain_outputs(self):
        self.S_out.append(self.S_0)
        self.E_out.append(self.E_0)
        self.I_out.append(self.I_0)
        self.D_out.append(self.D_0)
        self.R_out.append(self.R_0)
        self.t_axis.append(0)
        max_steps = 5000 #Max number of output data steps for simulation
        current_steps = len(self.S)/(self.output_dt/self.dt) #Current number of output data steps
        
        #Find output_dt
        while current_steps > max_steps: #While output simulation has too many steps
            self.output_dt *= 2 #Increase time between outputs
            current_steps = len(self.S)/(self.output_dt/self.dt)
        
        output_step = int(round(self.output_dt/self.dt)) #Finalised number of solver steps between output steps
        step = output_step
        #Iterate through all output steps, accessing relevant simulation indices and appending to outputs
        while step < len(self.S):
            self.S_out.append(self.S[step])
            self.E_out.append(self.E[step])
            self.I_out.append(self.I[step])
            self.D_out.append(self.D[step])
            self.R_out.append(self.R[step])
            self.t_axis.append(self.t_axis[-1] + self.output_dt)
            step += output_step
     
def runSEIDRSim(sim_params):
    model = SIRSimulation(sim_params)
    model.run_sim()
    model.obtain_outputs()
    return_arrays = [list(model.S_out), list(model.E_out), list(model.I_out),
      list(model.D_out), list(model.R_out)] #Return simulations data
    upper_bound = model.N_0
    return return_arrays, list(model.t_axis), upper_bound