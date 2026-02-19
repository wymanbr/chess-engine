class Move:
    def __init__(self, from_row, from_col, to_row, to_col):
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col

    def __str__(self):
        output = f'Move [from_row={self.from_row}, from_col={self.from_col}'
        output += f', to_row={self.to_row}, to_col={self.to_col}]'
        return output	
