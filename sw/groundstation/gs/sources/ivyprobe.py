#!/usr/bin/env python
"""An ivyprobe script for ivy-python
"""
from ivy.std_api import *
import os, string, sys, time, getopt

try:
    import readline
except ImportError:
    pass


IVYAPPNAME = 'pyivyprobe'

def info(fmt, *arg):
    print fmt % arg

def usage(cmd):
    usage = '''Usage: %s [options] regexps
Options:
\t-b, --ivybus=bus  defines the Ivy bus to join; defaults to 127:2010
\t-h, --help        this message
\t-n, name          changes the name of the agent, defaults to %s
\t-V, --version     prints the ivy release number
\t-v, --verbose     verbose mode (twice makes it even more verbose)

Type '.help' in ivyprobe for a list of available commands.'''
    print usage % ( os.path.basename(cmd), IVYAPPNAME )

def on_connection_change(agent, event):
    if event == IvyApplicationDisconnected :
        info('Ivy application %r has disconnected', agent)
    else:
        info('Ivy application %r has connected', agent)
    info('Ivy applications currently on the bus: %s',
         ','.join(IvyGetApplicationList()))
    
def on_die(agent, id):
    info('Received the order to die from %r with id = %d', agent, id)
    IvyStop()    

def on_msg(agent, *arg):
    info('Received from %r: %s', agent, arg and str(arg) or '<no args>')

def on_direct_msg(agent, num_id, msg):
    info('%r sent a direct message, id=%s, message=%s',
         agent, num_id, msg)
    
def on_regexp_change(agent, event, regexp_id, regexp):
    from ivy.ivy import IvyRegexpAdded
    info('%r %s regexp id=%s: %s',
            agent, event==IvyRegexpAdded and 'added' or 'removed',
            regexp_id, regexp)

if __name__ == '__main__':
    from ivy.ivy import ivylogger
    import logging

    ivybus = ''
    readymsg = '[%s is ready]' % IVYAPPNAME
    verbose=0
    showbind=0;
    
    ivylogger.setLevel(logging.WARN)

    try:
        optlist, left_args = \
                 getopt.getopt(sys.argv[1:],
                               'hb:n:Vv',
                               ['help','ivybus=','name=','version','verbose'])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(2)
    for opt, arg in optlist:
        if opt in ('-h', '--help'):
            usage(sys.argv[0])
            sys.exit()
        elif opt in ('-b', '--ivybus'):
            ivybus = arg
        elif opt in ('-V', '--version'):
            import ivy
            info('ivyprobe supplied with ivy-python library version%s',
                   ivy.__version__)
        elif opt in ('-v', '--verbose'):
            if not verbose:
                ivylogger.setLevel(logging.INFO)
                verbose+=1
            elif verbose==1:
                ivylogger.setLevel(logging.DEBUG)
                verbose+=1
            else:
                if hasattr(logging, 'TRACE'):
                    ivylogger.setLevel(logging.TRACE)
        elif opt in ('-n', '--name'):
            IVYAPPNAME=arg

    info('Broadcasting on %s',
         ivybus or os.environ.get('IVYBUS') or 'ivydefault')

    # initialising the bus 
    IvyInit(IVYAPPNAME,            # application name for Ivy
            readymsg ,             # ready message
            0,                     # parameter ignored
            on_connection_change,  # handler called on connection/deconnection
            on_die                 # handler called when a die msg is received 
            )

    # starting the bus
    IvyStart(ivybus)

    # bind the supplied regexps
    for regexp in left_args:
        IvyBindMsg(on_msg, regexp)

    # direct msg
    IvyBindDirectMsg(on_direct_msg)

    # Ok, time to go
    time.sleep(0.5)
    info('Go ahead! (type .help for help on commands)')
    while 1:
        try:
            msg = raw_input('')
        except (EOFError, KeyboardInterrupt):
            msg = '.quit'

        if msg == '.help':
            info("""Available commands:
        .bind 'regexp'              - add a msg to receive. The displayed index
                                                     can be supplied to .remove
        .die appname                - send die msg to appname
        .dieall-yes-i-am-sure       - send die msg to all applications
        .direct appname id arg      - send direct msg to appname
        .help                       - print this message
        .error appname id err_msg   - send an error msg to an appname
        .quit                       - terminate this application
        .remove idx                 - remove a binding (see .bind, .regexps)
        .regexps                    - show current bindings
        .regexps appname            - show all bindings registered for appname
        .showbind                   - show/hide bindings (toggle)
    .   .where appname              - print the host for appname
        .who                        - display the names of all applications on
                                                                       the bus

Everything that is not a command is interpreted as a message and sent to the
appropriate applications on the bus.
""")

        elif msg[:5] == '.bind':
            regexp = msg[6:]
            if not regexp:
                print 'Error: missing argument'
            info('Bound regexp, id: %d', IvyBindMsg(on_msg, regexp))
            
        elif msg == '.die-all-yes-i-am-sure':
            app_names = IvyGetApplicationList()
            if not app_names:
                info('No application on the bus')
                continue
            
            for app_name in IvyGetApplicationList():
                app = IvyGetApplication(app_name)
                if not app:
                    info('No application %s'%app_name)
                else:
                    IvySendDieMsg(app)
        
        elif msg[:4] == '.die':
            app_name = msg[5:]
            app = IvyGetApplication(app_name)
            if app is None:
                info('No application named %s', app_name)
                continue
            IvySendDieMsg(app)
            
        elif msg[:7] == '.direct':
            try:
                app_name, num = msg[8:].split()[:2]
                arg = ' '.join(msg[8:].split()[2:])
                if not arg:
                    raise ValueError
            except ValueError:
                print 'Error: wrong number of parameters'
                continue

            app = IvyGetApplication(app_name)
            if app is None:
                info('No application named %s', app_name)
                continue

            IvySendDirectMsg(app, num, arg)

        elif msg[:6] == '.error':
            try:
                app_name, num = msg[7:].split()[:2]
                err_msg = ' '.join(msg[7:].split()[2:])
                if not err_msg:
                    raise ValueError
            except ValueError:
                print 'Error: wrong number of parameters'
                continue

            app = IvyGetApplication(app_name)
            if app is None:
                info('No application named %s', app_name)
                continue

            IvySendError(app, num, err_msg)

        elif msg[:7] == '.remove':
            try:
                regexp_id = int(msg[8:])
                info('Removed %d:%s', regexp_id, IvyUnBindMsg(regexp_id))
            except KeyError:
                info('No such binding')
            except ValueError:
                info('Error: expected an integer')
                
        elif msg[:8] == '.regexps':
            app_name = msg[9:]
            app = IvyGetApplication(app_name)
            if app is None:
                from ivy import std_api
                info('Our subscriptions: %s',
                       ', '.join(["%s:'%s'"%(id,regexp) for id,regexp in std_api._IvyServer.get_subscriptions()]))
            else:
                info('Subscriptions for %s: %s',
                       app_name, ', '.join(["%s:'%s'"%(id,regexp) for id,regexp in IvyGetApplicationMessages(app)]))
                
        elif msg[:9] == '.showbind':
            if not showbind:
                IvyBindRegexpChange(on_regexp_change)
                showbind=1
                info("Changes in applications' bindings are now shown")
            else:
                IvyBindRegexpChange(void_function)
                showbind=0
                info("Changes in applications' bindings are now hidden")
                
        elif msg == '.quit':
            IvyStop()
            break
        
        elif msg[:6] == '.where':
            app_name = msg[7:]
            app = IvyGetApplication(app_name)
            if app is None:
                info('No application named %s', app)
                continue
            info('Application %s on %s:%s',app_name, app.ip, app.port)
            
        elif msg == '.who':
            print IvyGetApplicationList()
            
        else:
            info('Sent to %s peers'%IvySendMsg(msg))
