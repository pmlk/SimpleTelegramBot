import urllib, urllib2, os, difflib
from pprint import pprint

class UrlNotifier(object):
    directory = os.path.dirname(__file__)
    tmpFileSuffix = "_tmp.html"

    def __init__(self, jsonObject):
        #print "init: "
        #print jsonObject
        self.url = jsonObject["URL"]
        self.name = jsonObject["name"]
        ignores = []
        for ign in jsonObject["diffIgnore"]:
            ignores.append(str(ign))

        self.diffIgnore = ignores

    def getFilename(self):
        return os.path.join(self.directory, self.name + ".html")

    def getTmpFilename(self):
        return os.path.join(self.directory, self.name + self.tmpFileSuffix)

    def getMessage(self):
        return self.message

    def createMessage(self):
        msg = "There are changes in " + self.name + "\nCheck out:\n" + self.url
        self.message = urllib.quote(msg)
        #self.message = "ThereWereChanges"

    def clearMessage(self):
        self.message = ""



    def sing(self):
        print "url: %s" % self.url
        print "name: %s" % self.name
        print "diffIgnore: %s" % self.diffIgnore

    def update(self):
        self.download()
        filteredDiffs = self.getFilteredDiffs()

        #diffs = self.getDiffs()
        #print "unfiltered diffs: "
        #pprint(diffs)

        if len(filteredDiffs) > 0:
            print "filtered diffs: "
            pprint(filteredDiffs)
            self.createMessage()
        else:
            self.clearMessage()

        self.swapTmp()


    def download(self):
        filename = self.getFilename()
        tmpFilename = self.getTmpFilename()
        if not os.path.isfile(filename):
            print filename + " does NOT exist"
            f = open(filename, "w+")
            f.write("new file\r\n")
            f.close()

        oldContent = open(filename, "r+").read()
        newContent = urllib2.urlopen(self.url).read()
        ftmp = open(tmpFilename, "w+")
        ftmp.write(newContent)
        ftmp.close()

    def swapTmp(self):
        os.remove(self.getFilename())
        os.rename(self.getTmpFilename(), self.getFilename())

    def getCleanContents(self, filename):
        return open(filename).read().replace('<', '\n<')

    def getLines(self, filename):
        return self.getCleanContents(filename).splitlines()

    def getDiffs(self):
        file1 = self.getFilename()
        file2 = self.getTmpFilename()
        f1_lines = self.getLines(file1)
        f2_lines = self.getLines(file2)

        d = difflib.Differ()
        result = list(d.compare(f1_lines, f2_lines))

        diff = []
        for res in result:
            if res[0] == "+" or res[0] == "-": # only care about changes (= lines starting with + or -)
                diff.append(res)
        return diff

    def getFilteredDiffs(self):
        unfilteredDiffs = self.getDiffs()
        diffs = []
        for diff in unfilteredDiffs:
            if not any(x in diff for x in self.diffIgnore):
                diffs.append(diff)
        return diffs
