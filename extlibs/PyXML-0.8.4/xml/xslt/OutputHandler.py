import string
from xml.xslt import NullWriter, PlainTextWriter
from xml.xslt import HtmlWriter, XmlWriter

class OutputHandler(NullWriter.NullWriter):
    def __init__(self, outputParams, stream, notifyFunc):
        self._outputParams = outputParams
        self._stream = stream
        self._notify = notifyFunc
        self._stack = []

    def _finalize(self, writerClass):
        writer = writerClass(self._outputParams, self._stream)
        self._notify(writer)
        writer.startDocument()
        newline = 0
        for (cmd, args, kw) in self._stack:
            if newline:
                writer.text('\n')
            else:
                newline = 1
            apply(getattr(writer, cmd), args, kw)
        self._outputParams = None
        self._stream = None
        self._notify = None
        self._stack = []

    def getResult(self):
        return ''

    def startDocument(self):
        if self._outputParams.method == 'html':
            self._finalize(HtmlWriter.HtmlWriter)
        elif self._outputParams.method == 'xml':
            self._finalize(XmlWriter.XmlWriter)
        elif self._outputParams.method == 'text':
            self._finalize(PlainTextWriter.PlainTextWriter)

    def text(self, *args, **kw):
        self._stack.append(('text', args, kw))
        if string.strip(args[0]):
            self._finalize(XmlWriter.XmlWriter)

    def processingInstruction(self, *args, **kw):
        self._stack.append(('processingInstruction', args, kw))

    def comment(self, *args, **kw):
        self._stack.append(('comment', args, kw))

    def startElement(self, *args, **kw):
        self._stack.append(('startElement', args, kw))
        tagName = args[0]
        if string.upper(tagName) == 'HTML':
            self._finalize(HtmlWriter.HtmlWriter)
        else:
            self._finalize(XmlWriter.XmlWriter)
