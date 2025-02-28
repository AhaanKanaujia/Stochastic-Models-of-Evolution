# Stochastic-Models-of-Evolution
Build using `make`

## Interface
Usage: `python3 ./interface`

## Luo Model
Executable: `./Luo\ Implementation/main`

Usage: 
- `./Luo\ Implementation [output path]`
- `./Luo\ Implementation [output path] [m] [n] [r] [s] [full output: 1 or 0]`

## Game Theory Model
Executable: `./GameTheory\ +\ Luo\ Implementation/main`

Usage: 
- `./GameTheory\ +\ Luo\ Implementation/main [output path]`
- `./GameTheory\ +\ Luo\ Implementation/main [output path] [m] [n] [R] [S] [T] [P] [lambda] [w_i] [w_g] [full output: 1 or 0]`

## run_sims
Executable: `./run_sims`

Program to run multiple simulations in parallel

Modify code to needs (arguments for exectuables)

Comment out `ENABLE_FORK_LIMIT` if needed

Usage: ./run_simulations [0: Luo Model, 1: Game Theory Model] [number of simulations] [output directory] [executable] [m_start] [m_end] [m_increment] [n_start] [n_end] [n_increment] [args]...
- Luo Model: ./run_simulations 0 [number of simulations] [executable] [output directory] [m_start] [m_end] [m_increment] [n_start] [n_end] [n_increment] [r] [s] [full_output]
- Game Theory Model: ./run_simulations 1 [number of simulations] [executable] [output directory] [m_start] [m_end] [m_increment] [n_start] [n_end] [n_increment] [R] [S] [T] [P] [lambda] [w_i] [w_g] [full_output]

## Visualization
Requires:
- numpy
- matplotlib

Modify code to needs (uncomment desired visualization)

Usage: `python3 ./Visualization/visualization.py [file_path or directory to data] [1: Game Theory model, 0: Luo model]`
