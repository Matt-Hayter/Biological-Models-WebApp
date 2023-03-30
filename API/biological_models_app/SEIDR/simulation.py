"""
SEIDR simulation
"""
import numpy as np
from collections import deque
import math

class SIRSimulation:
        
    def __init__(self, sim_params):
        """
        Declare and initialise simulation's data.
        """
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
        self.min_output_dt = 0.01 #Initial output step size (minimum). Dynamically increases in factors of 2 for long sims [yrs]
        self.max_output_steps = 2500 #Max number of output data steps for simulation
        self.end_infected = 100  #End point for tail end of simulation
        self.limit_t = 2000 #Max time in sim before infection peak is found [yrs]
        
    def Euler_method(self):
        """
        Calculate current simulation step's rates using model ODEs, apply Euler method,
        then append to data.
        """
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
        """
        Initiate simulation and run Euler iterations for each time step, dynamically
        checking for simulation end points.
        """
        self.S.append(self.S_0)
        self.E.append(self.E_0)
        self.I.append(self.I_0)
        self.D.append(self.D_0)
        self.R.append(self.R_0)
        self.N.append(self.N_0)
        
        #Convert from time steps to integer step
        max_step = int(round(self.limit_t/self.dt))
        step = 0

        #Perform Euler until infection peak is found
        while True:
            step += 1
            self.Euler_method()
            if self.dIdt[-2] > 0 and self.dIdt[-1] <= 0:
                break
            #If peak hasn't been found before max step, end sim
            if step >= max_step:
                return

        #After peak is found, perform Euler until infections are low
        while self.I[-1] > self.end_infected or step <= 500:
            step += 1
            self.Euler_method()


    def obtain_outputs(self):
        """
        Select data to be outputted, at time intervals depending on simulated data length.
        Output data structures are designed for usage within chart.js line graph.
        """
        self.S_out.append({"data": self.S_0, "t": 0})
        self.E_out.append({"data": self.E_0, "t": 0})
        self.I_out.append({"data": self.I_0, "t": 0})
        self.D_out.append({"data": self.D_0, "t": 0})
        self.R_out.append({"data": self.R_0, "t": 0})
        output_dt = self.min_output_dt #Start with smallest output step size
        current_steps = len(self.S)/(output_dt/self.dt) #Current number of output data steps
        
        #Find output_dt
        while current_steps > self.max_output_steps: #While output simulation has too many steps
            output_dt *= 2 #Increase time between outputs
            current_steps = len(self.S)/(output_dt/self.dt)
        
        output_step = int(round(output_dt/self.dt)) #Finalised number of solver steps between output steps
        step = output_step
        #Iterate through all output steps, accessing relevant simulation indices and appending to outputs
        while step < len(self.S):
            next_t = self.S_out[-1]["t"] + output_dt #Add output dt to last t
            self.S_out.append({"data": self.S[step], "t": next_t})
            self.E_out.append({"data": self.E[step], "t": next_t})
            self.I_out.append({"data": self.I[step], "t": next_t})
            self.D_out.append({"data": self.D[step], "t": next_t})
            self.R_out.append({"data": self.R[step], "t": next_t})
            step += output_step

def find_graph_bounds(output_arrays, N_0):
    """
    Find suitable upper limits of charts and graphs for visualisation.
    """
    x_largest = output_arrays[0][-1]["t"] #Final time value
    graph_bounds = {"data": N_0} #Upper data limit is already known (N_0)
    #Produce appropriate upper limits for time in plots
    if x_largest >= 1000:
        graph_bounds["t"] = math.ceil(x_largest/100)*100 #Round up to nearest 100
    elif x_largest >= 30: 
        graph_bounds["t"] = math.ceil(x_largest/10)*10 #Round up to nearest 10
    else:
        graph_bounds["t"] = math.ceil(x_largest) #Round up to nearest while number
    return graph_bounds
     
def runSEIDRSim(sim_params):
    """
    Run simulation, given user selected parameters
    """
    model = SIRSimulation(sim_params)
    model.run_sim()
    model.obtain_outputs()
    output_arrays = [list(model.S_out), list(model.E_out), list(model.I_out),
      list(model.D_out), list(model.R_out)] #Return simulations data
    graph_bounds = find_graph_bounds(output_arrays, model.N_0)
    return output_arrays, graph_bounds