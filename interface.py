import subprocess

LUO_MODEL = 0
GAMETHEORY_MODEL = 1

RUN_SIMS_EXECUTABLE = "./run_sims"
LUO_EXECUTABLE = "./Luo Implementation/main"
GAMETHEORY_EXECUTABLE = "./GameTheory + Luo Implementation/main"

def main():
    # Setup shared arguments
    model = GAMETHEORY_MODEL
    simulation_count_per_m_n = 3
    output_directory = "./temp2"

    args = [RUN_SIMS_EXECUTABLE, str(model), str(simulation_count_per_m_n)]
    # Setup model specific arguments
    if model == LUO_MODEL:
        executable  = LUO_EXECUTABLE
        output_dir  = output_directory
        m_start     = 5
        m_end       = 10
        m_inc       = 1
        n_start     = 5
        n_end       = 10
        n_inc       = 1
        r           = 0.1
        s           = 0.05
        full_output = 1
        args = args+[executable, output_dir, str(m_start), str(m_end), str(m_inc), str(n_start), str(n_end), str(n_inc), str(r), str(s), str(full_output)]
    elif model == GAMETHEORY_MODEL:
        executable  = GAMETHEORY_EXECUTABLE
        output_dir  = output_directory
        m_start     = 5
        m_end       = 10
        m_inc       = 1
        n_start     = 5
        n_end       = 10
        n_inc       = 1
        reward      = 10
        sucker      = -5
        temptation  = 5
        punishment  = 0
        lambda_     = 2
        w_i         = 0.1
        w_g         = 0.1
        full_output = 1
        args = args+[executable, output_dir, str(m_start), str(m_end), str(m_inc), str(n_start), str(n_end), str(n_inc), str(reward), str(sucker), str(temptation), str(punishment), str(lambda_), str(w_i), str(w_g), str(full_output)]
        print(args)
    else:
        print(f"{model} is not a valid model number")
        exit(1)
    
    popen = subprocess.Popen(args)
    popen.wait()
    return

main()
