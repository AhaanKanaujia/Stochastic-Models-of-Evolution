#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/errno.h>

// enable to limit number of forks
#define ENABLE_FORK_LIMIT 0
#define LUO_MODEL 0
#define GAME_THEORY_MODEL 1

int main(int argc, char** argv) {
    if (argc != 5) {
        printf("Usage: ./run_simulations [number of simulations] [output directory] [executable] [0: Luo Model, 1: Game Theory Model]");
        return 1;
    }

    long max_num_fork = sysconf(_SC_CHILD_MAX);
    size_t count = atoi(argv[1]);

#if ENABLE_FORK_LIMIT
    if (count > 100) {
        printf("prevent 50+ forks, if you are sure change limit and rebuild\n");
        exit(1);
    }
#endif
    if (count > sysconf(_SC_CHILD_MAX)) {
        printf("number of processes(%zu) > _SC_CHILD_MAX(%zu), terminating (reduce number of simulations)", count, max_num_fork);
        exit(1);
    }
    
    struct stat st = {0};
    if (mkdir(argv[2], 0777)) {
        if (errno != EEXIST) {
            printf("Could not find or create directory %s", argv[2]);
            return 1;
        }
    }
    
    char output_filepath[200];
    strcpy(output_filepath, argv[2]);
    size_t initial_len = strlen(output_filepath);

    int full_output = 1;

    int model = atoi(argv[4]);
    
    int m_start = 100;
    int m_end = 100; // (inclusive)
    int m_inc = 20;

    int n_start = 100;
    int n_end = 100; // (inclusive)
    int n_inc = 20;

    // defaults
    int m = 50;
    int n = 50;
    double r = 0.2;
    double s = 0.2;
    double lambda = 0.1;
    double w_i = 0.01;
    double w_g = 0.01;

    char m_str[10];
    char n_str[10];
    char r_str[10];
    char s_str[10];
    char lambda_str[10];
    char w_i_str[10];
    char w_g_str[10];
    char full_output_str[10];

    for (m = m_start; m <= m_end; m+=m_inc) {
        for (n = n_start; n <= n_end; n+=n_inc) {
            if (model == LUO_MODEL) {
                printf("Running %zu simulations for %s with m=%d, n=%d, r=%f, s=%f\n", count, argv[3], m, n, r, s);
            } else if (model == GAME_THEORY_MODEL) {
                printf("Running %zu simulations for %s with m=%d, n=%d, lambda=%f, w_i=%f, w_g=%f\n", count, argv[3], m, n, lambda, w_i, w_g);
            }
            pid_t processes[count];
            for (int i = 0; i < count; ++i) {
                int count = sprintf(output_filepath+initial_len, "/o%d%d%d.csv", m, n, i);

                // fork process
                pid_t child_pid = fork();
                if (child_pid < 0) {
                    printf("Fork failed!\n");
                    exit(1);
                }
                if (!child_pid) {
                    // convert arguments to string for exec
                    sprintf(m_str, "%d", m);
                    sprintf(n_str, "%d", n);
                    sprintf(full_output_str, "%d", full_output);
                    if (model == LUO_MODEL) {
                        sprintf(r_str, "%f", r);
                        sprintf(s_str, "%f", s);
                        execl(argv[3], argv[3], output_filepath, m_str, n_str, r_str, s_str, full_output_str, NULL);
                    } else if (model == GAME_THEORY_MODEL) {
                        sprintf(lambda_str, "%f", lambda);
                        sprintf(w_i_str, "%f", w_i);
                        sprintf(w_g_str, "%f", w_g);
                        execl(argv[3], argv[3], output_filepath, m_str, n_str, lambda_str, w_i_str, w_g_str, full_output_str, NULL);
                    }
                    // only runs if exec failed
                    printf("Exec failed!\n");
                    exit(1);
                }
                processes[i] = child_pid;
            }
            int pid_status;

            // wait child processes
            for (int i = 0; i < count; ++i) {
                waitpid(processes[i], &pid_status, 0);
            }

        }
    }

    return 0;
}
