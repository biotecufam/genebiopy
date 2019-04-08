

class Annotation():
    def __init__(self, featureID, accessionID="", contig="", frame="",
                 strand="", start="", stop="", function="", role="",
                 subsystem="", subcategory="", category="No Category"):
        self.featureID = featureID
        self.accessionID = accessionID
        self.contig = contig
        self.frame = frame
        self.strand = strand
        self.start = start
        self.stop = stop
        self.function = function
        self.role = role
        self.subsystem = subsystem
        self.subcategory = subcategory
        self.category = category

    def __str__(self):
        return "Anot {}".format(self.featureID)

    def getGffText(self):
        return "{}\tFIG\tCDS\t{}\t{}\t.\t{}\t{}\tID={};Name={}".format(
            self.contig, self.start, self.stop,self.strand,
            self.frame,self.featureID,self.function)
