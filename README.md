# Stochastic-Models-of-Evolution
Build using `make`

## Luo Model
Executable: ./Luo\ Implementation/main
Usage: 
- ./Luo\ Implementation \[output path\]
- ./Luo\ Implementation \[output path\] \[m\] \[n\] \[r\] \[s\] \[full output: 1 or 0\]

## Game Theory Model
Executable: ./GameTheory\ +\ Luo\ Implementation/main
Usage: 
- ./GameTheory\ +\ Luo\ Implementation/main [output path]
- ./GameTheory\ +\ Luo\ Implementation/main [output path] [m] [n] [lambda] [w_i] [w_g] [full output: 1 or 0]

## run_sims
Program to run multiple simulations in parallel
Modify code to needs (arguments for exectuables)
Change `ENABLE_FORK_LIMIT` if needed
Usage: ./run_simulations [number of simulations per set of variables] [output directory] [executable] [0: Luo Model, 1: Game Theory Model] [full output: 1 or 0]

## Visualization
Requires:
- numpy
- matplotlib
Modify code to needs (uncomment desired visualization)
Usage: python3 ./Visualization/main.py [file_path or directory to data] [1: Game Theory model, 0: Luo model]
