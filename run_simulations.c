#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/errno.h>

// enable to limit number of forks
#define ENABLE_FORK_LIMIT
#define LUO_MODEL 0
#define GAME_THEORY_MODEL 1
#define ARGV_OFFSET 3

int main(int argc, char** argv) {
    if (argc != 14 && argc != 19) {
        printf("Usage: ./run_simulations [0: Luo Model, 1: Game Theory Model] [number of simulations] [output directory] [executable] [m_start] [m_end] [m_increment] [n_start] [n_end] [n_increment] [argument 1] [argument 2] ...\n");
        printf("Luo Model: \t\t./run_simulations 0 [number of simulations] [executable] [output directory] [m_start] [m_end] [m_increment] [n_start] [n_end] [n_increment] [r] [s] [full_output]\n");
        printf("Game Theory Model: \t./run_simulations 1 [number of simulations] [executable] [output directory] [m_start] [m_end] [m_increment] [n_start] [n_end] [n_increment] [R] [S] [T] [P] [lambda] [w_i] [w_g] [full_output]\n");
        return 1;
    }

    long max_num_fork = sysconf(_SC_CHILD_MAX);
    size_t sim_count = atoi(argv[2]);

#ifdef ENABLE_FORK_LIMIT
    if (sim_count > 100) {
        printf("prevent 100+ forks, change limit and rebuild\n");
        exit(1);
    }
#endif
    if (sim_count > sysconf(_SC_CHILD_MAX)) {
        printf("number of processes(%zu) > _SC_CHILD_MAX(%zu), terminating (reduce number of simulations)", sim_count, max_num_fork);
        exit(1);
    }
    
    struct stat st = {0};
    if (mkdir(argv[4], 0777)) {
        if (errno != EEXIST) {
            printf("Could not find or create directory %s", argv[4]);
            return 1;
        }
    }
    int model = atoi(argv[1]);

    int m_start = atoi(argv[ARGV_OFFSET+2]);
    int m_end = atoi(argv[ARGV_OFFSET+3]); // (inclusive)
    int m_inc = atoi(argv[ARGV_OFFSET+4]);

    int n_start = atoi(argv[ARGV_OFFSET+5]);
    int n_end = atoi(argv[ARGV_OFFSET+6]); // (inclusive)
    int n_inc = atoi(argv[ARGV_OFFSET+7]);

    char* program_name = argv[ARGV_OFFSET];

    char output_filepath[200];
    strcpy(output_filepath, argv[ARGV_OFFSET+1]);
    size_t initial_len = strlen(output_filepath);

    char m_str[10];
    char n_str[10];

    // separate args array for each proccess (prevent heap corruption)
    char** args[sim_count];
    for (size_t i = 0; i < sim_count; ++i) {
        if (model == LUO_MODEL) {
            args[i][0] = program_name;                 // program name
            args[i][1] = output_filepath;              // output file
            args[i][2] = m_str;                        // m
            args[i][3] = n_str;                        // n
            args[i][4] = argv[ARGV_OFFSET+8];          // r
            args[i][5] = argv[ARGV_OFFSET+9];          // s
            args[i][6] = argv[ARGV_OFFSET+10];         // full output
            args[i][7] = NULL;
        } else if (model == GAME_THEORY_MODEL) {
            args[i][0] = argv[ARGV_OFFSET];            // program name
            args[i][1] = output_filepath;              // output file
            args[i][2] = m_str;                        // m
            args[i][3] = n_str;                        // n
            args[i][4] = argv[ARGV_OFFSET+8];          // R
            args[i][5] = argv[ARGV_OFFSET+9];          // S
            args[i][6] = argv[ARGV_OFFSET+10];         // T
            args[i][7] = argv[ARGV_OFFSET+11];         // P
            args[i][8] = argv[ARGV_OFFSET+12];         // lambda
            args[i][9] = argv[ARGV_OFFSET+13];         // w_i
            args[i][10] = argv[ARGV_OFFSET+14];        // w_g
            args[i][11] = argv[ARGV_OFFSET+15];        // full output
            args[i][12] = NULL;
        }
    }

    for (int m = m_start; m <= m_end; m += m_inc) {
        for (int n = n_start; n <= n_end; n += n_inc) {
            printf("running");
            for (int j = 0; args[j] != NULL; ++j) {
                if (j == 1) {
                    printf(" [output path]");
                } else {
                    printf(" %s", args[j]);
                }
            }
            printf("\n");
            pid_t processes[sim_count];
            for (int i = 0; i < sim_count; ++i) {
                sprintf(output_filepath+initial_len, "/o%d_%d_%d.csv", m, n, i);
                snprintf(args[i][2], 9, "%d", m);
                snprintf(args[i][3], 9, "%d", n);

                // fork process
                pid_t child_pid = fork();
                if (child_pid < 0) {
                    printf("Fork failed!\n");
                    exit(1);
                }
                if (!child_pid) {
                    execv(args[i][0], args[i]);
                    // only runs if exec failed
                    printf("Exec failed!\n");
                    exit(1);
                }
                processes[i] = child_pid;
            }
            int pid_status;

            // wait child processes
            for (int i = 0; i < sim_count; ++i) {
                waitpid(processes[i], &pid_status, 0);
            }
        }
    }

    return 0;
}
