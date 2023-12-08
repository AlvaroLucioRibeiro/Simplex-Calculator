# simplex-calculator
Simplex Calculator using Python

![image](https://github.com/Isaquehg/simplex-calculator/assets/77072103/e852f34f-da56-4a36-a0df-a9c65bc71491)


## Table of Contents
- [About](#about)
- [Setup](#setup)
- [Simplex](#simplex)
  - [Create Tableau](#create_tableau)
  - [Pivot Column](#pivot_column)
  - [Pivot Row](#pivot_row)
  - [Start Simplex](#start_simplex)
  - [Get Results](#get_results)
- [Web Implementation](#web-implementation)

## About
This project was created for the Optimization I course (M210), with the primary goal of addressing optimization challenges using the Simplex method. The project focuses on effectively solving problems by considering the Objective Function, Constraints, and the Right Side of the equations.

## Setup
1. Setup the virtual environment:
  ```
  cd your-project-directory
  python3 -m venv venv
  ```
2. Run Flask server
   ```
   python3 app.py
   ```

## Simplex
The Simplex class is built by the following function:

### create_tableau
This method starts the tableau creation. The first row stands the table header, with the variables and stack variables.

### pivot_column
The method pivot_column finds the pivot column gathering the smallest negative value.

### pivot_row
The pivot row is found given the pivot column and the ratios between the pivot column and the constraints right side.

### start_simplex
Start_simplex method is the entry point for the Simplex method iteration. While the objetive function's coefficients are less than zero, the loop will keep alive.

### get_results
Function responsible for optimal solution and shadow price extraction.

## Web Implementation
The web implementation was built using the Flask framework, rendering the results from the Simplex class into the HTML templates.
