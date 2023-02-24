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
        self.N2_out = deque([]) #Population 2 values to be outputted
        self.t_axis = deque([]) #Holds time values
        #Model params
        #Species 1
        self.N1_0 = sim_params[0] #Population 1
        self.r1 = sim_params[1] #Growth rate 1 [1/yrs]
        self.k1 = sim_params[2] #Carrying capacity 1
        self.a1 = sim_params[3] #Competition from species 2 [1/yrs]
        #Species 2
        self.N2_0 = sim_params[4] #Population 2
        self.r2 = sim_params[5] #Growth rate 2
        self.k2 = sim_params[6] #Carrying capacity 2
        self.a2 = sim_params[7] #Competition from species 1 [1/yrs]
        
        #Simulation params
        self.dt = 0.001 #Integration step size [yrs]
        self.min_output_dt = 0.01 #Initial output step size (minimum). Dynamically increases in factors of 2 for long sims [yrs]
        self.max_output_steps = 2500 #Max number of output data steps for simulation
        self.min_dxdt = 0.05 #Gradient after which which simulation ends
        self.limit_t = 2000 #Max possible time in sim [yrs]
        
    def Euler_method(self):
        #ODEs
        dN1dt = self.r1*self.N1[-1]*(1-(self.N1[-1] + self.a1*self.N2[-1])/self.k1)
        dN2dt = self.r2*self.N2[-1]*(1-(self.N2[-1] + self.a2*self.N1[-1])/self.k2)
        #Euler method and append to data array
        self.N1.append(dN1dt*self.dt + self.N1[-1])
        self.N2.append(dN2dt*self.dt + self.N2[-1])

        return dN1dt, dN2dt

    def run_sim(self):
        #Set initial values
        self.N1.append(self.N1_0)
        self.N2.append(self.N2_0)

        #Convert from time steps to integer step
        limit_step = int(round(self.limit_t/self.dt)) #Max possible steps in sim
        step = 0

        while step < limit_step:
            step += 1
            dN1dt, dN2dt = self.Euler_method()
            if abs(dN1dt) < self.min_dxdt and abs(dN2dt) < self.min_dxdt: #End sim when stabalised
                return

    def obtain_outputs(self):
        self.N1_out.append({"data": self.N1_0, "t": 0})
        self.N2_out.append({"data": self.N2_0, "t": 0})
        output_dt = self.min_output_dt #Start with smallest output step size
        current_steps = len(self.N1)/(output_dt/self.dt) #Current number of output data steps
        
        #Find output_dt
        while current_steps > self.max_output_steps: #While output simulation has too many steps
            output_dt *= 2 #Increase time between outputs
            current_steps = len(self.N1)/(output_dt/self.dt)
        
        output_step = int(round(output_dt/self.dt)) #Finalised number of solver steps between output steps
        step = output_step
        #Iterate through all output steps, accessing relevant simulation indices and appending to outputs
        while step < len(self.N1):
            next_t = self.N1_out[-1]["t"] + output_dt #Add output dt to last t
            self.N1_out.append({"data": self.N1[step], "t": next_t})
            self.N2_out.append({"data": self.N2[step], "t": next_t})
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

def runCompetingSpeciesSim(sim_params):
    #Pass params configured by user
    model = CompetingSpeciesSimulation(sim_params)
    model.run_sim()
    model.obtain_outputs()
    output_arrays = [list(model.N1_out), list(model.N2_out)] #Return simulations data
    graph_bounds = find_graph_bounds(output_arrays)
    return output_arrays, graph_bounds