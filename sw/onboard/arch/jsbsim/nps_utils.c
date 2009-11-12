#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>

#include "nps_utils.h"

/* closeall() - close all FDs >= a specified value */
static void closeall(int fd)
{
    int fdlimit = sysconf(_SC_OPEN_MAX);

    while (fd < fdlimit)
        close(fd++);
}

/* like system(), but executes the specified command as a background
 * job. 
 * If INFD, OUTFD or ERRFD are non-NULL, then a pipe will be opened and
 * a descriptor for the parent end of the relevent pipe stored there.
 * If any of these are NULL, they will be redirected to /dev/null in the
 * child.
 * Also closes all FDs > 2 in the child process (an oft-overlooked task)
 *
 * @returns: < 0 on error
 *
 * http://www.steve.org.uk/Reference/Unix/faq_8.html#SEC90
 */
pid_t spawn_background_command(const char *cmd,
                               int *infd, int *outfd, int *errfd)
{
    int nullfd = -1;
    int pipefds[3][2];
    int error = 0;

    if (!cmd)
        return errno = EINVAL, -1;

    pipefds[0][0] = pipefds[0][1] = -1;
    pipefds[1][0] = pipefds[1][1] = -1;
    pipefds[2][0] = pipefds[2][1] = -1;

    if (infd && pipe(pipefds[0]) < 0)
        error = errno;
    else if (outfd && pipe(pipefds[1]) < 0)
        error = errno;
    else if (errfd && pipe(pipefds[2]) < 0)
        error = errno;

    if (!error && !(infd && outfd && errfd))
    {
        nullfd = open("/dev/null",O_RDWR);
        if (nullfd < 0)
            error = errno;
    }

    if (!error)
    {
        pid_t pid = fork();
        switch (pid)
        {
            case -1: /* fork failure */
                error = errno;
                break;
                
            case 0: /* child proc */
                
                dup2(infd ? pipefds[0][0] : nullfd, 0);
                dup2(outfd ? pipefds[1][1] : nullfd, 1);
                dup2(errfd ? pipefds[2][1] : nullfd, 2);
                closeall(3);
                
                execl("/bin/sh","sh","-c",cmd,(char*)NULL);

                _exit(127);

            default: /* parent proc */

                close(nullfd);
                if (infd)
                    close(pipefds[0][0]), *infd = pipefds[0][1];
                if (outfd)
                    close(pipefds[1][1]), *outfd = pipefds[1][0];
                if (errfd)
                    close(pipefds[2][1]), *errfd = pipefds[2][0];

                return pid;
        }
    }

    /* only reached if error */
    {
        int i,j;
        for (i = 0; i < 3; ++i)
            for (j = 0; j < 2; ++j)
                if (pipefds[i][j] >= 0)
                    close(pipefds[i][j]);
    }
    
    if (nullfd >= 0)
        close(nullfd);

    return errno = error, (pid_t) -1;
}


void sigchild_sighandler(int sig) {
        /* wait() is the key to acknowledging the SIGCHLD */
        wait(0);
}
