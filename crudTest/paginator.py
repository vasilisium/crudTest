from flask import request


class Paginator():

    _limitKey = 'limit'
    _skipKey = 'skip'

    def __init__(self, recordsCount, limit=10, skip=0, request=None):
        self.recordsCount = recordsCount
        self.request = request

        if request is not None:
            newLimit, newSkip = self._parseRequest(request)
        
        if newLimit:
            self.limit = newLimit
        else:
            self.limit = limit

        if newSkip:
            self.skip = newSkip
        else:
            self.skip = skip
        
    def _getOverSkip(self, skip, limit=0):
        if skip is None:
            return 0
        
        if (limit is None) and (self.limit) :
            limit = self.limit

        newSkip = skip

        if limit == 0:
            return newSkip

        if newSkip >= self.recordsCount:
            newSkip = self._getOverSkip(newSkip - limit)

        if newSkip < 0:
            return 0
        return newSkip

    def _generateUrl(self, skip=None, limit=None):
        if limit is None:
            limit = self.limit
        if skip is None:
            skip = self.skip

        result = f'?{self._limitKey}={str(limit)}'

        if skip > 0:
            result += f'&{self._skipKey}={str(skip)}'
        restArgs = self._getQueryParams()
        for key in restArgs.keys():
            if key != 'id':
                result += f'&{key}={restArgs[key]}' 
        return result

    def urlCurrent(self):
        return self._generateUrl()

    def urlFirst(self):
        return self._generateUrl(0)

    def urlNext(self):
        skip = self._getOverSkip(self.skip+self.limit)
        return self._generateUrl(skip)
    
    def urlLast(self):
        if self.limit == 0:
            return self.urlNext()
        return self._generateUrl(self._getOverSkip(self.recordsCount-self.limit))
    
    def urlPrev(self):
        asd = self._getOverSkip(self.skip-self.limit)
        return self._generateUrl(asd)

    def _parseRequest(self, request):
        limit = None
        skip = None

        try:
            limit = int(self._getRequestedLimit(request))
        except Exception:
            pass

        try:
            skip = int(self._getRequestedSkip(request))
        except Exception:
            pass

        skip = self._getOverSkip(skip, limit=limit)
        return limit, skip

    def _getRequestedLimit(self, request):
        limit = None
        if self._limitKey in request.cookies:
            limit = request.cookies[self._limitKey]
        if self._limitKey in request.args:
            limit = request.args[self._limitKey]
        return limit

    def _getRequestedSkip(self, request):
        skip = None
        if self._skipKey in request.args:
            skip = request.args[self._skipKey]
        return skip        

    def _getQueryParams(self):
        data = self.request.args.copy()
        if len(data) > 0:
            if 'limit' in data:
                del data['limit']
            if 'skip' in data:
                del data['skip']
        return data