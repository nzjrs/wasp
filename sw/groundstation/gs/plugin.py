import sys
import os.path
import logging

LOG = logging.getLogger('plugin')

class PluginNotSupported(Exception):
    pass

class Plugin(object):
    PLUGIN_NAME     = ""
    PLUGIN_VERSION  = "0.1"
    
    def plugin_name(self):
        return self.PLUGIN_NAME or self.__class__.__name__

    def plugin_version(self):
        return self.PLUGIN_VERSION

class PluginManager:
    def __init__(self, *plugin_dirs):
        self._plugins = []
        self._plugins_failed = []

        #default plugin dir is ./plugins/
        if not plugin_dirs:
            plugin_dirs = [os.path.join(
                            os.path.dirname(os.path.realpath(__file__)),
                            "plugins")]

        for d in plugin_dirs:
            LOG.debug("Searching for plugins in %s" % d)
            plugin_files = [x[:-3] for x in os.listdir(d) if x.endswith(".py")]
            sys.path.insert(0, d)
            for plugin in plugin_files:
                LOG.debug("Importing %s" % plugin)
                try:
                    __import__(plugin)
                except PluginNotSupported, e:
                    self._plugins_failed.append((plugin, str(e)))
                except Exception, e:
                    LOG.warn("Error loading plugin: %s" % plugin, exc_info=True)
                    self._plugins_failed.append((plugin, str(e)))

    def initialize_plugins(self, *args, **kwargs):
        for klass in Plugin.__subclasses__():
            try:
                self._plugins.append(klass(*args, **kwargs))
            except PluginNotSupported, e:
                self._plugins_failed.append((klass.PLUGIN_NAME or klass.__name__, str(e)))
            except Exception, e:
                LOG.warn("Error instantiating plugin class: %s" % klass, exc_info=True)
                self._plugins_failed.append((klass.PLUGIN_NAME or klass.__name__, str(e)))

    def get_plugins_implementing_interface(self, interface):
        return [p for p in self._plugins if isinstance(p, interface)]

    def get_plugin_summary(self):
        return  [(p.plugin_name(), p.plugin_version()) for p in self._plugins], self._plugins_failed

