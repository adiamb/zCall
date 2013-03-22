#! /usr/bin/env python

"""Convenience script to generate HTML documentation

Use instead of command-line pydoc. Allows user to specify Python version 2.7, even if installation of pydoc is compiled with an earlier Python version.

Run with -h or --help for command-line help.
"""

import os, pydoc, re, sys
from importlib import import_module
from modulefinder import ModuleFinder
try: 
    import argparse    
except ImportError: 
    sys.stderr.write("ERROR: Requires Python 2.7 to run; exiting.\n")
    sys.exit(1)

def main():

    description="Convenience script to generate HTML documentation using pydoc"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--out', required=True,  metavar="PATH", 
                        help="Directory in which to write HTML output files.")
    parser.add_argument('--recursive', action='store_true', default=False,
                        help="Recursively import documentation for dependencies. If not recursive, zcall documents will contain broken links to standard modules.")
    parser.add_argument('--verbose', action='store_true', default=False,
                        help="Write pydoc information to stdout.")
    args = vars(parser.parse_args())
    recursive = args['recursive']
    verbose = args['verbose']
    if not verbose: # suppress stdout chatter from pydoc.writedoc
        sys.stdout = open('/dev/null', 'w')

    localDir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.abspath(localDir+"/..")) # import from zcall dir
    zcallDir = os.path.abspath(localDir+"/../zcall")
    outDir = os.path.abspath(args['out'])
    if not (os.access(outDir, os.W_OK) and os.path.isdir(outDir)):
        msg = "ERROR: Output path "+outDir+" is not a writable directory.\n"
        sys.stderr.write(msg)
        sys.exit(1)
    os.chdir(outDir)
    import zcall
    pydoc.writedoc(zcall)
    modules = set()
    zcall = set()
    scripts = []
    mf = ModuleFinder()
    for script in os.listdir(zcallDir):
        if re.search("\.py$", script) and script!="__init__.py":
            words = re.split("\.", script)
            words.pop()
            scriptName = (".".join(words)) # name without .py suffix
            modules.add("zcall."+scriptName)
            zcall.add(scriptName)
            scripts.append(script)
    if recursive:
        for script in scripts:
            mf.run_script(os.path.join(zcallDir, script))
            for name, mod in mf.modules.iteritems(): 
                if name not in zcall: modules.add(name)
    for module in modules:
        pydoc.writedoc(import_module(module))

# NB findThresholds and findMeanSD files can only be run as scripts, not imported.  Omitting the .py extension from these files prevents pydoc from creating broken links in the main zcall page.


if __name__ == "__main__":
    main()
