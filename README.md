# Biological Models Visualizer - Web Application

## Description
This is a visualizer for population models (predator-prey, competing species) and infectious disease
spread models (SIR, SEIDR - COVID). Select model, configure parameters, and run simulations - dynamic bar and line charts will visualize the model's development over appropriate time periods. Model parameters range from degree of competition between species to disease infectious periods - you can follow the parameter suggestions or have a play around yourself, and observe how each parameter affects the simulation. Create an account to save interesting parameter presets for each model.

URL: https://www.biologicalmodelsvisualizer.com

## App Composition:
- Frontend: Vue.js with Bootstrap
- Backend: Flask RESTful API with MYSQL
- Python packages utilised to structure backend, separating logical components
- Deployed in the cloud with AWS

## Features:
- CRUD database: create account, manage account and save/delete presets
- Vuex for application state management
- Chart.js for simulation visualisation
- Salted password hashing using the argon2i algorithm and protection against SQL injection attacks
- Extensive user input validation (unique usernames, emails etc.)

## App Snapshots (using the SEIDR model view)

![app_SEIDR_home](https://user-images.githubusercontent.com/85962471/228538235-5d0951a7-ddbe-4367-a404-ffbbbe477e57.png)

Bar-chart race, mid simulation:

![app_SEIDR_bar](https://user-images.githubusercontent.com/85962471/228541002-a27d10ad-9390-476e-a3a1-705bad236c8c.png)

Line-chart race, mid simulation:

![app_SEIDR_line](https://user-images.githubusercontent.com/85962471/228541029-56e0fa71-8d27-4df2-b844-017b925cb4f0.png)


Matt Hayter
