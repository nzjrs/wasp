#ifndef _NPS_UTILS_H_
#define _NPS_UTILS_H_

#include <unistd.h>
#include <sys/types.h>

pid_t   spawn_background_command(const char *cmd, int *infd, int *outfd, int *errfd);
void    spawn_sigchild_sighandler(int sig);

#endif
