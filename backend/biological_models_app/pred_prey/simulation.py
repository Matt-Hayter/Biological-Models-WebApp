"""
Predator-Prey (Lotka-Voltera) Simulation

Simulation output time periods and the simulation's end point are dynamically
calculated, utilising the periodicity of the model's solutions. Alter simulation
params member data to configure this process.
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
        self.dPdt = [1] #Traced for simulation end time
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
        self.dt = 0.01 #Integration step size, constant [yrs]
        self.output_dt = 0.01 #Initial output step size. Increases in factors of 10 for long sims [yrs]
        self.max_troughs = 6 #Length of simulations if oscillating
        self.large_interval = 10 #If first turning point is not found within large interval, output_dt * 4, large_interval * 4 and repeat [yrs]
        self.max_interval = 5000 #If first turning point is not found within max interval, end sim (no periodicity found) [yrs]
        self.max_time = 13000 #End simulation if time exceeds this point [yrs]
        
    def Euler_method(self, step, output_step):
        """
        Calculate ODE's rates, apply Euler method, then add to output queue if required
        """
        #ODEs
        dNdt = self.N[-1]*(self.a - self.b*self.P[-1])
        self.dPdt.append(self.P[-1]*(self.c*self.N[-1] - self.d))
        #Euler method and append to data array
        self.N.append(dNdt*self.dt + self.N[-1])
        self.P.append(self.dPdt[-1]*self.dt + self.P[-1])
        if step % output_step == 0: #Only output on output steps
            self.N_out.append(self.N[-1])
            self.P_out.append(self.P[-1])

    def run_sim(self):
        """
        Initiate simulation and run Euler iterations for each time step,
        dynamically checking for simulation end points.
        """
        self.N.append(self.N_0)
        self.N_out.append(self.N_0)
        self.P.append(self.P_0)
        self.P_out.append(self.P_0)

        #Convert from time steps to integer step
        output_step = int(round(self.output_dt/self.dt)) #Number of solver steps between output steps
        large_interval_step = int(round(self.large_interval/self.dt)) #Above this, output_dts are increased
        max_interval_step = int(round(self.max_interval/self.dt)) #Simulation ends if step this large is found
        max_step = int(round(self.max_time/self.dt)) #

        #Perform Euler until first prey trough is found
        step, output_step = self.first_period_sim(output_step, large_interval_step, max_interval_step)
        if step == -1: #E simulation and calulate t axis if signalled
            self.t_axis = list(np.linspace(0, len(self.N_out)*self.output_dt, len(self.N_out)))
            return
                    
        #Continue iterations now first predator trough is found, until max trough number found
        trough_counter = 1
        while trough_counter < self.max_troughs: #End simulation when desired through is found
            step += 1
            self.Euler_method(step, output_step)
            if self.dPdt[-2] < 0 and self.dPdt[-1] >= 0: #Count troughs as they are passed
                trough_counter += 1
            if step >= max_step: #End sim and calcuate t axis if max time has been reached
                self.t_axis = list(np.linspace(0, len(self.N_out)*self.output_dt, len(self.N_out)))
                return
        
        #Calculate t axis
        self.t_axis = list(np.linspace(0, len(self.N_out)*self.output_dt, len(self.N_out)))
        
    def first_period_sim(self, output_step, large_interval_step, max_interval_step):
        """
        Run simulation until first trough is found. Also determine output step
        for the remainder of the simulation (if period between troughs is large, 
        recursively increase output dt and step until satisfactory or end sim)
        """
        step = 0
        while step < max_interval_step:
            step += 1
            self.Euler_method(step, output_step)
            if self.dPdt[-2] < 0 and self.dPdt[-1] >= 0:
                return step, output_step
            #If first trough hasn't been found before large interval, further increase output steps and restart
            if step >= large_interval_step:
                self.reset_sim()
                large_interval_step *= 2 #For checks within next recursion
                output_step *= 2 #Increase output step for next run
                self.output_dt *= 2
                #Recursion call with new step values
                return self.first_period_sim(output_step, large_interval_step, max_interval_step)
        #If peak hasn't been found before max interval step, end sim
        sim_end_code = -1
        return sim_end_code, sim_end_code #Signals end of simulation

    def reset_sim(self):
        """
        Reset simulation and reassign initial paramaters
        """
        self.N = deque([])
        self.N_out = deque([])
        self.P = deque([])
        self.P_out = deque([])
        self.dPdt = [1]
        self.N.append(self.N_0)
        self.N_out.append(self.N_0)
        self.P.append(self.P_0)
        self.P_out.append(self.P_0)

def runPredPreySim(sim_params):
    #Pass parameters configured by user
    model = PredatorPreySimulation(sim_params)
    model.run_sim()
    return_arrays = [list(model.N_out), list(model.P_out)] #Return simulations data
    largest_val = max([max(return_arrays[0]), max(return_arrays[1])]) #Max value obtained throughout sim's output
    #Produce appropriate upper bound for plots
    if largest_val >= 1000:
        upper_bound = math.ceil(largest_val/100)*100 #Round up to nearest 100
    elif largest_val >= 30: 
        upper_bound = math.ceil(largest_val/10)*10 #Round up to nearest 10
    else:
        upper_bound = math.ceil(largest_val) #Round up to nearest while number
    print(len(model.N_out), len(model.P_out), len(model.t_axis))
    return return_arrays, model.t_axis, upper_bound
    