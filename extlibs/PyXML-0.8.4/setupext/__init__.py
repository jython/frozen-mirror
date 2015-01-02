"Package providing extensions to the standard distutils"

from install_data import Data_Files, install_Data_Files

from distutils.command.bdist_wininst import bdist_wininst

# When building a windows installer, put some more text into
# the long description
class wininst_request_delete(bdist_wininst):
    add_text = "\nIf you have installed earlier versions of this package, please remove them through 'Add/Remove Programs' before installing this release."

    def get_inidata(self):
        m = self.distribution.metadata
        m.long_description = m.long_description + self.add_text
        return bdist_wininst.get_inidata(self)
