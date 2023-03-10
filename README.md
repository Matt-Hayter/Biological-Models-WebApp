# Biological Models Visualiser - Web Application

## Description
Visualiser for population models (predator-prey, competing species) and infectious disease
spread models (SIR, SEIDR). Select model, configure parameters, and run simulations - dynamic bar and line charts will visualise the model's development over appropriate time periods. Model parameters 
range from degree of competition between species to disease infectious periods - you can follow the parameter suggestions or have a play around yourself, and observe how each parameter affects the simulation. Create an account to save interesting parameter presets for each model.

## App Composition:
- Frontend: Vue.js
- Backend: Flask RESTful API with MYSQL
- Python packages utilised to structure backend, separating logical components

## Features:
- CRUD database: create account, manage account and save/delete presets
- Salted password hashing using the Argon2i algorithm and protection against SQL injection attacks
- Vuex for application state management
- Chart.js for simulation visualisation
- Extensive user input validation

Matt Hayter