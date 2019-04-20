from scrapy.dupefilters import RFPDupeFilter
import os
from datetime import datetime as dt

class SeenURLFilter(RFPDupeFilter):
    """A dupe filter that considers the URL"""
    path = os.path.join(os.curdir, 'cache')

    #def __init__(self, path=None, debug=False):
    #    RFPDupeFilter.__init__(self, self.path, debug=False)
    

    def week_of_month(self):
        """ Returns the week of the month for the specified date.
        """
        day_of_month = dt.today().day
        return str((day_of_month - 1) // 7 + 1)

    def open(self):
        file_name =  '_'.join(['seen', dt.today().strftime('%Y%m'), "w", self.week_of_month()])
        self.file = open(os.path.join(self.path, file_name), 'a+')
        self.file.seek(0)
        self.fingerprints.update(x.rstrip() for x in self.file)

        
    
    def request_seen(self, request):
        if request.url in self.fingerprints:
            return True
        if not (request.url.endswith('_BestSellers_YES')):
            return False
        self.fingerprints.add(request.url)
        if self.file:
            self.file.write(request.url + os.linesep)