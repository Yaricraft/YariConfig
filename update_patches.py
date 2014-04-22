import os
import sys
import fnmatch
import shlex
import difflib
import time
from optparse import OptionParser

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
    print "Creating patches"
    
    strConfigDir = os.path.dirname(os.path.abspath(__file__))
    parser = OptionParser()
    
    parser.add_option('-p', '--pack', action='store', dest='optPack', help='Pack to use.', default='scpb')
    parser.add_option('-c', '--config', action='store', dest='optConfig', help='Name of configs to compare to.', default='yari')
    
    options, _ = parser.parse_args()
    
    optPack = os.path.abspath(options.optPack)
    print "Using option "+optPack
    optConfig = os.path.abspath(options.optConfig)
    print "Using option "+optConfig

    diff = os.path.normpath(os.path.join(optPack, optConfig+'_patches'))
    print "Patches going to "+diff
    base = os.path.normpath(os.path.join(optPack, 'original'))
    print "Using base configs at "+base
    work = os.path.normpath(os.path.join(optPack, optConfig))
    print "Using edited configs at "+work
    
    for path, _, filelist in os.walk(work, followlinks=True):
        for cur_file in fnmatch.filter(filelist, '*.cfg'):
            file_base = os.path.normpath(os.path.join(base, path[len(work)+1:], cur_file)).replace(os.path.sep, '/')
            file_work = os.path.normpath(os.path.join(work, path[len(work)+1:], cur_file)).replace(os.path.sep, '/')
            
            fromlines = open(file_base, 'U').readlines()
            tolines = open(file_work, 'U').readlines()
            
            patch = ''.join(difflib.unified_diff(fromlines, tolines, '../' + file_base[len(strPackDir)+1:], '../' + file_work[len(strPackDir)+1:], '', '', n=3))
            patch_dir = os.path.join(diff, path[len(work)+1:])
            patch_file = os.path.join(patch_dir, cur_file + '.patch')
            print('%s', patch_dir)
            
            if len(patch) > 0:
                print patch_file[len(diff)+1:]
                patch = patch.replace('\r\n', '\n')
                
                if not os.path.exists(patch_dir):
                    os.makedirs(patch_dir)
                with open(patch_file, 'wb') as fh:
                    fh.write(patch)
            else:
                if os.path.isfile(patch_file):
                    print("Deleting empty patch: %s"%(patch_file))
                    os.remove(patch_file)
                    

    cleanDirs(diff)
    
if __name__ == '__main__':
    main()