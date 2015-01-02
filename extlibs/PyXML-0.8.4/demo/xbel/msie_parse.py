#!/usr/bin/env python

"""
Small utility to convert MSIE favourites to an object structure.

Originally written by Fredrik Lundh.
Modified by Lars Marius Garshol
2-17-2002 tbp Now closes folder when its traverse is done.  Also works
    with current IE shortcut format, which can differ from the format
    that was assumed here.
"""

import bookmark,os,string

DIR = "Favoritter" # Norwegian version

#USRDIR = os.environ["USERPROFILE"] # NT version
USRDIR = r"c:\windows" # 95 version

class MSIE:
    # internet explorer

    def __init__(self,bookmarks, path):
        self.bms=bookmarks
        self.root = None
        self.path = path

        self.__walk()



    def __walk(self, subpath=[]):
        # traverse favourites folder
        path = os.path.join(self.path, string.join(subpath, os.sep))
        for file in os.listdir(path):
            fullname = os.path.join(path, file)
            if os.path.isdir(fullname):
                self.bms.add_folder(file,None)
                self.__walk(subpath + [file])
                self.bms.leave_folder()
            else:
                url = self.__geturl(fullname)
                if url:
                    self.bms.add_bookmark(os.path.splitext(file)[0],None,
                                          None,None,url)

    def __geturl(self, file):
        try:
            fp = open(file)
            #if fp.readline() != "[InternetShortcut]\n":
            #    return None
            while 1:
                line=fp.readline()
                if not line:
                    return None
                if line=="[InternetShortcut]\n":
                    s = fp.readline()
                    if not s:
                        break
                    if s[:4] == "URL=":
                        fp.close()
                        return s[4:-1]
                elif line=="[DEFAULT]\n":
                    s = fp.readline()
                    if not s:
                        break
                    if s[:8] == "BASEURL=":
                        fp.close()
                        return s[8:-1]
        except IOError:
            return ''
        fp.close()
        return ''

# --- Testprogram

if __name__ == '__main__':
    import sys
    if len(sys.argv)>1:
        path = sys.argv[1]
    else:
        try:
            import win32api, win32con
        except ImportError:
            print "The win32api module is not available on this system"
            print "so we can't automatically find your favorites folder."
            print "Please re-run this program specifiying the location of your"
            print "favorites folder on the command line."
            sys.exit(1)
        keyname = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        hkey = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, keyname)
        path, pathtype = win32api.RegQueryValueEx(hkey, "Favorites")
        assert pathtype == win32con.REG_SZ

    msie=MSIE(bookmark.Bookmarks(), path)
    msie.bms.dump_xbel()


