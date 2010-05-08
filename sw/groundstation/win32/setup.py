#!/usr/bin/env python
# PiTiVi , Non-linear video editor
#
# Copyright (c) 2009, Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from distutils.core import setup
import py2exe
import os
import sys
import shutil
from optparse import OptionParser

class Deploy:

    app_exe = None
    app_name = None
    app_version = None
    app_description = None
    
    py2exe_windows_options = None
    py2exe_options = None
    
    curr_dir = None
    root_dir = None
    
    def __init__(self, gtk_path):
        self.gtk_dir = gtk_path
        
        self.check_current_dir()
        self.set_path_variables()
        self.create_deployment_folder()
        self.set_path()
        self.check_dependencies()
        self.deploy()
        self.deploy_gtk()
        self.set_py2exe_options()
        self.run_py2exe()
        self.close()
        
    def check_current_dir(self):
        """
        Derived objects must set and check self.curr_dir and
        self.root_dir if they wish to chain to this function
        """
        raise NotImplementedError
        
    def deploy(self):
        """
        Copy application specific files to deployment dirs
        """
        raise NotImplementedError
        
    def set_py2exe_options(self):
        raise NotImplementedError
        
    def check_dependencies(self):
        """
        Check application dependencies
        """
        raise NotImplementedError
        
    def close(self, message=None):
        if message is not None:
            print 'ERROR: %s' % message
            exit(1)
        else:
            exit(0)

    def set_path_variables(self):
        """
        Sets up dir paths for a unix like environment, like
        self.dist._{bin/share/lib/etc}
        """
        assert(self.curr_dir)
        assert(self.root_dir)
        assert(self.app_exe)
        self.dist_dir = os.path.join (self.root_dir, 'win32', 'dist')
        self.dist_bin_dir = os.path.join (self.dist_dir, 'bin')
        self.dist_etc_dir = os.path.join (self.dist_dir, 'etc')
        self.dist_etc_app_dir = os.path.join (self.dist_dir, 'etc', self.app_exe)
        self.dist_share_dir = os.path.join (self.dist_dir, 'share')
        self.dist_share_app_dir = os.path.join (self.dist_share_dir, self.app_exe)
        self.dist_lib_dir = os.path.join (self.dist_dir, 'lib')
        self.dist_lib_app_dir = os.path.join (self.dist_lib_dir, self.app_exe)


    def set_path(self):
        # Add root folder to the python path
        sys.path.insert(0, self.root_dir)
        # Add Gtk to the system path
        for folder in [self.gtk_dir]:
            os.environ['PATH'] = os.environ['PATH']+';'+os.path.join(folder, 'bin')
        os.environ['PATH'] = os.environ['PATH']+';'+self.dist_bin_dir
        
    def create_deployment_folder(self):
        # Create a Unix-like diretory tree to deploy
        print ('Create deployment directory')
        if os.path.exists(self.dist_dir):
            try:
                shutil.rmtree(self.dist_dir)
            except :
                self.close("Can't delete folder %s"%self.dist_dir)

        for path in [self.dist_dir, self.dist_bin_dir, self.dist_etc_dir, self.dist_etc_app_dir,
                self.dist_share_dir, self.dist_lib_app_dir, 
                self.dist_share_app_dir]:
                os.makedirs(path)

    def deploy_gtk(self):
        print ('Deploying Gtk dependencies')
        # Copy Gtk files to the dist folder
        for name in ['fonts', 'pango', 'gtk-2.0']:
            shutil.copytree(os.path.join(self.gtk_dir, 'etc', name),
                     os.path.join(self.dist_etc_dir, name))
        shutil.copytree(os.path.join(self.gtk_dir, 'lib', 'gtk-2.0'),
            os.path.join(self.dist_lib_dir, name))

    def run_py2exe(self):
        assert(self.app_name)
        assert(self.app_version)
        assert(self.app_description)
        assert(self.py2exe_windows_options != None)
        assert(self.py2exe_options != None)
        
        sys.argv.insert(1, 'py2exe')
        setup(
            name = self.app_name,
            description = self.app_description,
            version = self.app_version,
            windows = [ self.py2exe_windows_options ],
            options = self.py2exe_options,
            zipfile = None,
        )
         


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
                    'You can download the installers at:\n'
                    'http://www.pygtk.org/\n'
                    'http://www.gtk.org/')
        else:
            print ('Gtk... OK')        


    def deploy(self):
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
        

    
def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-k", "--gtk-path", action="store",
            default="c:\\gtk", type="string",
            help="GTK+ installation path")

    (options, args) = parser.parse_args()
    GroundStationDeploy(options.gtk_path)
    
if __name__ == "__main__":
    main()


