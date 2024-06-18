
import fnmatch, os
import importlib

__all__ = []
base_dir = os.path.dirname(__file__)
for(dirpath, dirnames, filenames) in os.walk(base_dir):
    curr_dir = dirpath.replace(base_dir,'')

    for filename in fnmatch.filter(filenames, "[!_]*.py"):
        module_name = os.path.splitext(os.path.basename(filename))[0]
        full_name = (curr_dir + '.'+module_name).replace(os.path.sep, '.')

        module = importlib.import_module(full_name, package= __package__)
        class_name = ''.join([x.title() for x in module_name.split('_')]).strip()
        globals()[class_name] = getattr(module, class_name)
        __all__.append(class_name)