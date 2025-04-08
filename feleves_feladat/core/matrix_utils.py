from copy import deepcopy

class MatrixUtils:
    @staticmethod
    def transpose(mat):
        return list(map(list, zip(*mat)))

    @staticmethod
    def matmul(A, B):
        return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]

    @staticmethod
    def invert_matrix(matrix):
        size = len(matrix)
        I = [[float(i == j) for i in range(size)] for j in range(size)]
        M = deepcopy(matrix)

        for i in range(size):
            diag = M[i][i]
            if diag == 0:
                raise ValueError("Mátrix inverze nem létezik: nulla a diagonális elem")
            for j in range(size):
                M[i][j] /= diag
                I[i][j] /= diag
            for k in range(size):
                if k != i:
                    factor = M[k][i]
                    for j in range(size):
                        M[k][j] -= factor * M[i][j]
                        I[k][j] -= factor * I[i][j]
        return I

    @staticmethod
    def pseudo_inverse(B):
        BT = MatrixUtils.transpose(B)
        BTB = MatrixUtils.matmul(BT, B)
        try:
            BTB_inv = MatrixUtils.invert_matrix(BTB)
        except ValueError as e:
            print(f"Hiba a mátrix inverzénél: {e}")
            return None
        return MatrixUtils.matmul(BTB_inv, BT)
