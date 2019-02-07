class WebUtility:

    def getOp(self, pathinfo):
        return pathinfo.split('/')

    def gerarchyInterpreter(self, gerarchy, keys):
        result = {}
        for i in range(len(gerarchy)):
            result[keys[i]] = gerarchy[i]
        return result
