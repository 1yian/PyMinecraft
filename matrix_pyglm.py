import copy

class MatrixGLM4D:
    def __init__(self, matrix):
        self.matrix = copy.deepcopy(matrix)
    
    def alter(self, matrix):
        self.matrix = copy.deepcopy(matrix)

    def getGLMMatrix(self):
        return copy.copy(self.matrix)
    
    def getPyMatrix(self):
        ret = [[0.0 for x in range(4)] for x in range(4)]
        tempMat = copy.copy(self.matrix)
        ret[0][0] = tempMat[0][0]
        ret[0][1] = tempMat[0][1]
        ret[0][2] = tempMat[0][2]
        ret[0][3] = tempMat[0][3]

        ret[1][0] = tempMat[1][0]
        ret[1][1] = tempMat[1][1]
        ret[1][2] = tempMat[1][2]
        ret[1][3] = tempMat[1][3]

        ret[2][0] = tempMat[2][0]
        ret[2][1] = tempMat[2][1]
        ret[2][2] = tempMat[2][2]
        ret[2][3] = tempMat[2][3]

        ret[3][0] = tempMat[3][0]
        ret[3][1] = tempMat[3][1]
        ret[3][2] = tempMat[3][2]
        ret[3][3] = tempMat[3][3]
        return ret
