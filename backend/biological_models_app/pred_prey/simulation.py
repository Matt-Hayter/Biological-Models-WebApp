"""
Predator-Prey (Lotka-Voltera) Simulation

Simulation's output time step is dynamically calculated, allowing the number of output steps to
fit within the configured maximum. Alter simulation params member data to configure this process.
"""
import numpy as np
from collections import deque
import math

class PredatorPreySimulation:
        
    def __init__(self, sim_params):
        """
        Declare and initialise simulation's data. Output data structures are designed for
        usage with chart.js line graph.
        """
        self.N = deque([]) #Holds prey population values
        self.N_out = deque([]) #For outputted steps. Sequence of dicts, each containing a data and time value
        self.P = deque([]) #Holds predator population values
        self.P_out = deque([]) #For outputted steps. Sequence of dicts, each containing a data and time value
        self.dPdt = [1] #Traced for simulation end time
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
        self.dt = 0.0005 #Integration step size, constant [yrs]
        self.min_output_dt = 0.01 #Initial output step size (minimum). Dynamically increases in factors of 2 for long sims [yrs]
        self.max_output_steps = 2500 #Max number of output data steps for simulation
        self.max_troughs = 5 #Length of simulations if oscillating
        self.limit_t = 10000 #Max possible time in sim [yrs]
        
    def Euler_method(self, step):
        """
        Calculate ODE's rates, apply Euler method, then add to output queue if required
        """
        #ODEs
        dNdt = self.N[-1]*(self.a - self.b*self.P[-1])
        self.dPdt.append(self.P[-1]*(self.c*self.N[-1] - self.d))
        #Euler method and append to data array
        self.N.append(dNdt*self.dt + self.N[-1])
        self.P.append(self.dPdt[-1]*self.dt + self.P[-1])

    def run_sim(self):
        """
        Initiate simulation and run Euler iterations for each time step,
        dynamically checking for simulation end points.
        """
        self.N.append(self.N_0)
        self.P.append(self.P_0)

        #Convert from time steps to integer step
        limit_step = int(round(self.limit_t/self.dt)) #Max possible steps in sim
        step = 0
                    
        trough_counter = 0
        #End simulation when desired through or limit is found
        while step < limit_step and trough_counter < self.max_troughs:
            step += 1
            self.Euler_method(step)
            if self.dPdt[-2] < 0 and self.dPdt[-1] >= 0: #Count troughs as they are passed
                trough_counter += 1
    
    def obtain_outputs(self):
        self.N_out.append({"data": self.N_0, "t": 0})
        self.P_out.append({"data": self.P_0, "t": 0})
        output_dt = self.min_output_dt #Start with smallest output step size
        current_steps = len(self.N)/(output_dt/self.dt) #Current number of output data steps

        #Find output_dt
        while current_steps > self.max_output_steps: #While output simulation has too many steps
            output_dt *= 2 #Increase time between outputs
            current_steps = len(self.N)/(output_dt/self.dt)
        
        output_step = int(round(output_dt/self.dt)) #Finalised number of solver steps between output steps
        step = output_step
        #Iterate through all output steps, accessing relevant simulation indices and appending to outputs
        while step < len(self.N):
            next_t = self.N_out[-1]["t"] + output_dt #Add output dt to last t
            self.N_out.append({"data": self.N[step], "t": next_t})
            self.P_out.append({"data": self.P[step], "t": next_t})
            step += output_step

def find_graph_bounds(output_arrays):
    """
    Find suitable upper limits of charts and graphs for visualisation
    """
    x_largest = output_arrays[0][-1]["t"] #Final time value
    y_largest = max([ #Max value obtained throughout sim's output
        max(dict_element["data"] for dict_element in output_arrays[0]),
        max(dict_element["data"] for dict_element in output_arrays[1])])
    axes = ["t", "data"]
    graph_bounds = {} #Return dictionary
    #Produce appropriate upper limits for plots
    for i, axis_largest in enumerate((x_largest, y_largest)):
        if axis_largest >= 1000:
            graph_bounds[axes[i]] = math.ceil(axis_largest/100)*100 #Round up to nearest 100
        elif axis_largest >= 30: 
            graph_bounds[axes[i]] = math.ceil(axis_largest/10)*10 #Round up to nearest 10
        else:
            graph_bounds[axes[i]] = math.ceil(axis_largest) #Round up to nearest while number

    return graph_bounds

def runPredPreySim(sim_params):
    #Pass parameters configured by user
    model = PredatorPreySimulation(sim_params)
    model.run_sim()
    model.obtain_outputs()
    output_arrays = [list(model.N_out), list(model.P_out)] #Return simulations data
    graph_bounds = find_graph_bounds(output_arrays)
    return output_arrays, graph_bounds
    