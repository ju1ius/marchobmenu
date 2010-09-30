#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <inotifytools/inotifytools.h>
#include <inotifytools/inotify.h>

/*
 * Compile with: gcc -linotifytools mom-watch.c -o mom-watch
 */

void signal_handler(int signum);
void cleanup(void);
void it_error(void);


int main(int argc, char **argv)
{
  /* Our process ID and Session ID */
  pid_t pid, sid;

  struct inotify_event * event;
  int option, i, res;
  int daemonize = 0;
  char* exclude_pattern;
  char* command;

  /*****************************************
   * Process Command line args
   ****************************************/

  while((option = getopt(argc, argv, "c:de:")) != -1)
  {
    switch(option)
    {
      case 'c':
        command = optarg;
        break;
      case 'd':
        daemonize = 1;
        break;
      case 'e':
        exclude_pattern = optarg;
      case '?':
        if (optopt == 'c' || optopt == 'e')
        {
          fprintf (stderr, "Option -%c requires an argument.\n", optopt);
          exit(EXIT_FAILURE);
        }
        else if (isprint(optopt))
        {
          fprintf (stderr, "Unknown option 0\\x%x'.\n", optopt);
          exit(EXIT_FAILURE);
        }
      default:

        break;
    }
  }
  /******************************************
   * Daemonification steps
   *****************************************/
  if(daemonize)
  {
    /* Fork off the parent process */
    pid = fork();
    if (pid < 0) exit(EXIT_FAILURE);

    /* If we got a good PID, then we can exit the parent process. */
    if (pid > 0) exit(EXIT_SUCCESS);

    /* 
     * Change the file mode mask
     * Not needed here as we don't write to any file
     */
    /*umask(0);*/

    /* Create a new SID for the child process */
    sid = setsid();
    if (sid < 0) exit(EXIT_FAILURE);

    /* Change the current working directory */
    if ((chdir("/")) < 0) exit(EXIT_FAILURE);

    /*
     * Close out the standard file descriptors
     * We can't use this, as it will prevent the
     * build.py script to write to file descriptors
     * TODO: check why ?
     */
    /*close(STDIN_FILENO);*/
    /*close(STDOUT_FILENO);*/
    /*close(STDERR_FILENO);*/
  }

  /*****************************************
   *  Core Functionnalities
   ****************************************/

  /*
   * initialize and watch the entire directory tree from the current working
   * directory downwards for all events
   */
  if(!inotifytools_initialize()) it_error();
 
  /* set time format to 24 hour time, HH:MM:SS */
  inotifytools_set_printf_timefmt( "%T" );

  if (exclude_pattern)
  {
    inotifytools_ignore_events_by_regex(exclude_pattern, 0);  
  }
  /*
   * Loop on the remaining command-line args
   * Exit if a non-existent dir is given
   */
  for (i = optind; i < argc; i++)
  {
    res = inotifytools_watch_recursively(argv[i], IN_CREATE | IN_DELETE | IN_MODIFY); 
    if(!res) it_error();
  }
  /* Setup signal handling */
  signal(SIGHUP, signal_handler);
  signal(SIGINT, signal_handler);
  signal(SIGQUIT, signal_handler);
  signal(SIGTERM, signal_handler);

  /* Output all events as "<timestamp> <events> <path>" */
  event = inotifytools_next_event(-1);
  while (event)
  {
    inotifytools_fprintf(stdout, event, "%T %e %w%f\n");
    system(command);
    event = inotifytools_next_event(-1);
  }
  cleanup();
  return 0;
}

void cleanup(void)
{
  inotifytools_cleanup();
}

void signal_handler(int signum)
{
  (void) signum;
  cleanup();
  exit(0);
}

void it_error(void)
{
  fprintf(stderr, "%s\n", strerror(inotifytools_error()));
  exit(EXIT_FAILURE);
}
