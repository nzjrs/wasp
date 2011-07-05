import os
import shutil

from deploy import Deploy

class GroundStationDeploy(Deploy):

    app_exe = "groundstation"
    app_name = "Wasp Groundstation"
    app_version = "0.1"
    app_description = "Wasp UAV Groundstation"


    def check_current_dir(self):
        self.curr_dir = os.getcwd()
        if not self.curr_dir.endswith('win32'):
            self.close("The script must be run from the win32 directory")
        self.root_dir = os.path.abspath(os.path.join(self.curr_dir,'..'))
        
    def check_dependencies(self):
        print ('Checking dependencies')
        try:
            import gtk
            import gtk.gdk
            import gobject
            import glib
        except ImportError:
                self.close('IMPORT_ERROR: Could not find the Gtk Python bindings.\n'
                    'You can download the installers at: http://www.pygtk.org/')
        else:
            print ('Gtk... OK')        


    def deploy_application(self):
        def copy_dir_contents(source_dir, dest_dir, filter_func):
            os.makedirs(dest_dir)
            for name in [x for x in os.listdir(source_dir) if filter_func(x)]:
                shutil.copy (os.path.join(source_dir, name),
                    os.path.join(dest_dir, name))
        
        print('Deploying GroundStation')
        
        # Copy plugins
        copy_dir_contents(
            os.path.join(self.root_dir, 'gs', 'plugins'),
            os.path.join(self.dist_lib_app_dir, "plugins"),
            lambda x: x.endswith('.ui') or x.endswith('.py')
        )
        
        # Copy icons
        copy_dir_contents(
            os.path.join(self.root_dir, 'data', 'icons'),
            os.path.join(self.dist_share_app_dir, "icons"),
            lambda x: x.endswith('.png')
        )

        # Copy ui
        copy_dir_contents(
            os.path.join(self.root_dir, 'data', 'ui'),
            os.path.join(self.dist_share_app_dir, "ui"),
            lambda x: x.endswith('.ui')
        )
        
        # Copy config xml
        copy_dir_contents(
            os.path.join(self.root_dir, '..', 'onboard', 'config'),
            os.path.join(self.dist_etc_app_dir, 'config'),
            lambda x: x.endswith('.xml')
        )        
        
    def set_py2exe_options(self):
        self.py2exe_windows_options = {
                'script': '../groundstation.py',
                'icon_resources': [(1, "rocket-48x48.ico")],
        }
        
        self.py2exe_options = {
                'py2exe': {
                      'packages': 'gs, wasp, libserial',
                      'includes': 'gtk, cairo, pango, atk, pangocairo, gobject, glib, gio',
                      'dist_dir' : self.dist_bin_dir
                }
        }
        
if __name__ == "__main__":
    GroundStationDeploy()


