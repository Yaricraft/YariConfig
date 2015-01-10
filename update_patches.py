import os
import sys
import fnmatch
import shlex
import difflib
import time

from optparse import OptionParser

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def cmdsplit(args):
    if os.sep == '\\':
        args = args.replace('\\', '\\\\')
    return shlex.split(args)
                    
def cleanDirs(path):
    if not os.path.isdir(path):
        return
 
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                cleanDirs(fullpath)
 
    files = os.listdir(path)
    if len(files) == 0:
        os.rmdir(path)
        
def main():
    print 
    print "    ============================="
    print "              YariConfig"
    print "    ============================="
    print "   Minecraft configuration utility."
    print ""
    
    streamPacks = open("packs.yml", "r")
    dataPacks = load(streamPacks, Loader=Loader)
    
    defBase = dataPacks['packs']['scpb']['base']
    defWork = dataPacks['packs']['scpb']['work']
    
    # Get the path we are running the script in.
    strPathCurrent = os.path.dirname(os.path.abspath(__file__))
    
    # Collect options
    parser = OptionParser()
    parser.add_option('-b', '--base', action='store', dest='optBase', help='Path to base onfigs.', default=defBase)
    parser.add_option('-w', '--work', action='store', dest='optWork', help='Path to work onfigs.', default=defWork)
    options, _ = parser.parse_args()
    
    # Make sure the directories are valid.
    if options.optBase == '':
        strPathBase = os.path.abspath('base')
        print "No base config path specified, attempting to use "+strPathBase
    else:
        strPathBase = os.path.abspath(options.optBase)
    strNormBase = os.path.normpath(strPathBase)
    if os.path.isdir(strNormBase):
        print "Using base configs at "+strNormBase
    else:
        print "Base config directory was not found at "+strNormBase
        return
    
    if options.optWork == '':
        strPathWork = os.path.abspath('work')
        print "No work config path specified, attempting to use "+strPathWork
    else:
        strPathWork = os.path.abspath(options.optWork)
    strNormWork = os.path.normpath(strPathWork)
    if os.path.isdir(strNormWork):
        print "Using work configs at "+strNormWork
    else:
        print "Work config directory was not found at "+strNormWork
        return
    
    strShortBase = strPathBase.split(os.path.sep)[-1]
    strShortWork = strPathWork.split(os.path.sep)[-1]
    strNormPatches = os.path.normpath(os.path.join(strPathWork,".."))+os.path.sep+strShortBase+"to"+strShortWork+"patches"
    
    for path, _, filelist in os.walk(strNormWork, followlinks=True):
        for cur_file in fnmatch.filter(filelist, '*'):
            file_base = os.path.normpath(os.path.join(strNormBase, path[len(strNormWork)+1:], cur_file)).replace(os.path.sep, '/')
            file_work = os.path.normpath(os.path.join(strNormWork, path[len(strNormWork)+1:], cur_file)).replace(os.path.sep, '/')
            
            if not os.path.isfile(file_base):
                continue
            
            fromlines = open(file_base, 'U').readlines()
            tolines = open(file_work, 'U').readlines()
            
            patch = ''.join(difflib.unified_diff(fromlines, tolines, '../' + file_base[len(strPathCurrent)+1:], '../' + file_work[len(strPathCurrent)+1:], '', '', n=3))
            patch_dir = os.path.join(strNormPatches, path[len(strNormWork)+1:])
            patch_file = os.path.join(patch_dir, cur_file + '.patch')
            
            
            if len(patch) > 0:
                print patch_file[len(strNormPatches)+1:]
                patch = patch.replace('\r\n', '\n')
                
                if not os.path.exists(patch_dir):
                    os.makedirs(patch_dir)
                with open(patch_file, 'wb') as fh:
                    fh.write(patch)
            else:
                if os.path.isfile(patch_file):
                    print "Deleting empty patch: "+patch_file
                    os.remove(patch_file)
                    

    cleanDirs(strNormPatches)
    
if __name__ == '__main__':
    main()
