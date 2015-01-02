import os, cStringIO, string
from wxPython.wx import *
from xml.parsers.xmlproc import xmlval,xmlapp,xcatalog,catalog,errors, utils

# Todo:
# - bookmarks or something for sysid entry (make general bm and last-used?)
# - radio group for Output: None, Canonical XML, ESIS
# - tick box: namespace processing
# - File | About
# - File | Help

# --- Constants

XML_WILDCARD = "XML documents (*.xml)|*.xml|RDF documents (*.rdf)|*.rdf|XSL stylesheets (*.xsl)|*.xsl|All files|*.*"
CAT_WILDCARD = "SGML Open catalogs (*.soc)|*.soc|XCatalogs (*.xml)|*.xml|All files|*.*"

# --- Application

class Validator(wxApp):

    def OnInit(self):
        frame = MainWindow(NULL, -1, "wxValidator")
        frame.Show(true)
        self.SetTopWindow(frame)
        return true

# --- ErrorHandler

class ErrorRecorder(xmlapp.ErrorHandler):

    def __init__(self,locator,warnings=1):
        xmlapp.ErrorHandler.__init__(self,locator)
        self.show_warnings=warnings
        self.reset()

    def warning(self,msg):
        if self.show_warnings:
            self.__add_error(msg)

    def error(self,msg):
        self.__add_error(msg)

    def fatal(self,msg):
        self.__add_error(msg)

    def reset(self):
        self.errors=[]

    def __add_error(self,msg):
        self.errors.append((self.locator.get_current_sysid(),
                            self.locator.get_line(),
                            self.locator.get_column(),
                            msg))

# --- Output window

class OutputWindow(wxFrame):

    def __init__(self, parent, output):
        wxFrame.__init__(self, parent, -1, "Output")
        wxTextCtrl(self, -1, output, wxDefaultPosition, wxDefaultSize,
                   wxTE_READONLY | wxTE_MULTILINE)

# --- Main window

ID_DOCUMENT = NewId()
ID_CATALOG  = NewId()
ID_EXIT     = NewId()

class MainWindow(wxFrame):
    def __init__(self, parent, ID, title):
        wxFrame.__init__(self, parent, ID, title,
                         wxDefaultPosition, wxSize(550, 450))

        self.SetAutoLayout(true)
        self.CreateStatusBar(1)

        # --- Menu

        menu = wxMenu()
        menu.Append(ID_DOCUMENT, "&Find document",
                    "Find a document to validate")
        menu.Append(ID_CATALOG,  "Find &catalog",
                    "Find a catalog to resolve public identifiers with")
        menu.Append(ID_EXIT, "E&xit", "Terminate the program")

        menuBar = wxMenuBar()
        menuBar.Append(menu, "&File");

        self.SetMenuBar(menuBar)

        EVT_MENU(self, ID_DOCUMENT, self.FindDocument)
        EVT_MENU(self, ID_CATALOG,  self.FindCatalog)
        EVT_MENU(self, ID_EXIT,     self.TimeToQuit)

        # --- Field: XML document location

        loc=wxTextCtrl(self,-1,"")
        lc=wxLayoutConstraints()
        lc.top.SameAs(self, wxTop, 5)
        lc.height.AsIs()
        lc.left.SameAs(self, wxLeft, 5)
        lc.right.SameAs(self, wxRight, 5)
        loc.SetConstraints(lc)

        # --- Field: Catalog file location

        cat_loc=""
        if os.environ.has_key("XMLXCATALOG"):
            cat_loc=os.environ["XMLXCATALOG"]
        elif os.environ.has_key("XMLSOCATALOG"):
            cat_loc=os.environ["XMLSOCATALOG"]

        cat=wxTextCtrl(self,-1,cat_loc)
        lc=wxLayoutConstraints()
        lc.top.SameAs(loc, wxBottom, 5)
        lc.height.AsIs()
        lc.left.SameAs(self, wxLeft, 5)
        lc.right.SameAs(self, wxRight, 5)
        cat.SetConstraints(lc)

        # --- A containing panel for a row of controls

        panel=wxPanel(self,-1)
        lc=wxLayoutConstraints()
        lc.top.SameAs(cat, wxBottom)
        lc.height.AsIs()
        lc.left.SameAs(self, wxLeft)
        lc.right.SameAs(self, wxRight)
        panel.SetConstraints(lc)

        # --- Buttons

        parse_id=NewId()
        parse_btn=wxButton(panel,parse_id,"Parse")
        lc=wxLayoutConstraints()
        lc.top.SameAs(panel, wxTop, 5)
        lc.height.AsIs()
        lc.left.SameAs(panel, wxLeft, 5)
        lc.width.AsIs()
        parse_btn.SetConstraints(lc)
        EVT_BUTTON(self, parse_id, self.Parse)

        # --- Field: Language

        lang=wxComboBox(panel,-1)
        # FIXME: want to set style
        lc=wxLayoutConstraints()
        lc.top.SameAs(panel, wxTop, 5)
        lc.height.AsIs()
        lc.left.SameAs(parse_btn, wxRight, 5)
        lc.width.AsIs()
        lang.SetConstraints(lc)

        for lang_name in errors.get_language_list():
            lang.Append(lang_name)

        lang.SetSelection(0)

        # --- Field: Warnings

        warn=wxCheckBox(panel, -1, "Warnings")
        lc=wxLayoutConstraints()
        lc.top.SameAs(panel, wxTop, 5)
        lc.height.AsIs()
        lc.left.RightOf(lang, 5)
        lc.width.AsIs()
        warn.SetConstraints(lc)

        # --- Field: Output?

        output = wxCheckBox(panel, -1, "Show output")
        lc = wxLayoutConstraints()
        lc.top.SameAs(panel, wxTop, 5)
        lc.height.AsIs()
        lc.left.RightOf(warn, 5)
        lc.width.AsIs()
        output.SetConstraints(lc)

        # --- Error list

        list_id = NewId()
        list = wxListCtrl(self, list_id, wxDefaultPosition, wxDefaultSize,
                          wxLC_REPORT|wxSUNKEN_BORDER)
        list.InsertColumn(0,"System identifier")
        list.InsertColumn(1,"Line")
        list.InsertColumn(2,"Column")
        list.InsertColumn(3,"Message")
        lc=wxLayoutConstraints()
        lc.top.SameAs(panel, wxBottom, 5)
        lc.bottom.SameAs(self, wxBottom, 5)
        lc.left.SameAs(self, wxLeft, 5)
        lc.right.SameAs(self, wxRight, 5)
        list.SetConstraints(lc)

        # --- Global data

        self.loc=loc
        self.cat=cat
        self.list=list
        self.parser=xmlval.XMLValidator()
        self.errors=ErrorRecorder(self.parser)
        self.lang=lang
        self.warn=warn
        self.output = output

    def Parse(self, *args):
        sysid = string.strip(self.loc.GetValue())
        if sysid == "":
            self.SetStatusText("Nothing to parse")
            return

        self.parser.reset()
        self.errors.reset()
        self.errors.show_warnings = self.warn.GetValue()

        if self.cat.GetValue != "":
            self.SetStatusText("Parsing catalog...")
            pf=xcatalog.FancyParserFactory()
            cat=catalog.xmlproc_catalog(self.cat.GetValue(),pf,self.errors)
            self.parser.set_pubid_resolver(cat)

        self.SetStatusText("Parsing...")

        if self.output.GetValue():
            output = cStringIO.StringIO()
            self.parser.set_application(utils.DocGenerator(output))

        self.parser.set_error_handler(self.errors)
        self.parser.set_error_language(self.lang.GetValue())
        self.parser.parse_resource(sysid)

        self.list.DeleteAllItems()

        ix=0
        for (sysid,line,col,msg) in self.errors.errors:
            self.list.InsertStringItem(ix, sysid)
            self.list.SetStringItem(ix, 1, `line`)
            self.list.SetStringItem(ix, 2, `col`)
            self.list.SetStringItem(ix, 3, msg)
            ix=ix+1

        self.list.SetColumnWidth(0, wxLIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wxLIST_AUTOSIZE)
        self.list.SetColumnWidth(2, wxLIST_AUTOSIZE)
        self.list.SetColumnWidth(3, wxLIST_AUTOSIZE)

        if self.output.GetValue():
            self.CreateOutputWindow(output)
        self.SetStatusText("Parse completed (%s error(s))" % ix)

    def CreateOutputWindow(self, output):
        win = OutputWindow(self, output.getvalue())
        win.Show(true)

    def FindDocument(self, event):
        file = wxFileSelector("Find document", ".", "", "", XML_WILDCARD,
                              wxOPEN | wxHIDE_READONLY)
        if file: self.loc.SetValue(file)

    def FindCatalog(self, event):
        file = wxFileSelector("Find catalog", ".", "", "", CAT_WILDCARD,
                              wxOPEN | wxHIDE_READONLY)
        if file: self.cat.SetValue(file)

    def TimeToQuit(self, event):
        self.Close(true)

# --- Main program

app = Validator(0)
app.MainLoop()
