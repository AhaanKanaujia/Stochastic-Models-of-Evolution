LUO_PATH = ./Luo\ Implementation
GAMETHEORY_PATH = ./GameTheory\ +\ Luo\ Implementation

run_sims: ./run_simulations.c $(LUO_PATH)/main $(GAMETHEORY_PATH)/main
	clang ./run_simulations.c -o run_sims -g

$(LUO_PATH)/main: $(LUO_PATH)/main.cpp
	clang++ $(LUO_PATH)/main.cpp -o $(LUO_PATH)/main

$(GAMETHEORY_PATH)/main: $(GAMETHEORY_PATH)/main.cpp
	clang++ $(GAMETHEORY_PATH)/main.cpp -o $(GAMETHEORY_PATH)/main

clean:
	rm run_sims
	rm $(LUO_PATH)/main
	rm $(GAMETHEORY_PATH)/main
