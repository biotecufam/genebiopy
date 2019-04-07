
class Annotation():
    def __init__(self, featureID, accessionID="", contig="", strand="", start="", stop="",
                 function="", role="", subsystem="", subcategory="", category="No Category"):
        self.featureID = featureID
        self.accessionID = accessionID
        self.contig = contig
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
