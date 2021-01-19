class Helper(obect):
    @staticmethod
    def writeBinaryToFile(filePath, data):
        f = open(filePath, "wb")
        f.write(data)
        f.close()

    @staticmethod
    def readBinaryFromFile(filePath):
        f = open(filePath, "rb")
        data = f.read()
        f.close()
        return data
