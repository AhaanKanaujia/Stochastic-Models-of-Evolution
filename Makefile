default:
	clang ./run_simulations.c -o run_sims
.PHONY : default

clean:
	rm run_sims
