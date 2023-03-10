# Biological Models Visualiser - Web Application

## Description
Visualiser for population models (predator-prey, competing species) and infectious disease
spread models (SIR, SEIDR). Select model, configure parameters, and run simulations - dynamic bar and line charts will visualise the model's development over appropriate time periods. Model parameters 
range from degree of competition between species to disease infectious periods - have a play around
and see how each affects the result. Create an account to save intereseting parameter presets for each model.

## App Composition:
- Frontend: Vue.js
- Backend: Flask RESTful API with MYSQL
- Python packages utilised to structure backend, separating logical components

## Features:
- CRUD database: create account, save presets and manage account
- Salted password hashing using the Argon2i algorithm and protection against SQL injection attacks
- Vuex for application state management
- Chart.js for simulation visualisation
- Extensive user input validation

Matt Hayter