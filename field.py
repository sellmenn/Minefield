from random import randint

class Field:
    def __init__(self, length = 10, mines = 20, start = (0, 0), goal = (9, 9))-> None:
        self.length = length
        self.num_mines = mines
        self.start, self.goal = start, goal
        self.map, self.mines = self.create_field()

    # Return a map of the minefield as a str object
    def __repr__(self):
        field = self.map
        field_str = str()
        length = self.length
        for i in range(length):
            for j in range(length):
                if (i,j) != self.start and (i,j) != self.goal:
                    field_str += f" {str(field[i][j])} "
                elif (i,j) == self.start:
                    field_str += " S "
                else:
                    field_str += " G "
            field_str += "\n"
        return field_str

    # Create and return a tuple of a map of the minefield, with randomly planted mines, as a list, and a list of coordinates of planted mines
    def create_field(self) -> list:
        field = []
        length = self.length
        for i in range(length):
            field.append(list())
            for j in range(length):
                field[i].append(0)
        mines = []
        mine_count = 0
        while mine_count != self.num_mines:
            x, y = randint(0, length - 1), randint(0, length - 1)
            if (x, y) not in mines and (x,y) != self.start and (x,y) not in self.goal:
                field[x][y] = "X"
                mines.append((x, y))
            mine_count += 1
        return field, mines
    
    # Reset field
    def reset(self):
        for i in range(self.length):
            for j in range(self.length):
                self.unmark_field((i,j))

    # Mark a position on the field with int as an argument
    def mark_field(self, coordinate, marker) -> None:
        x, y = coordinate
        self.map[x][y] = marker

    # Unmark a position on the field
    def unmark_field(self, coordinate) -> None:
        if coordinate != self.start and coordinate != self.goal and coordinate not in self.mines:
            x, y = coordinate
            self.map[x][y] = 0

    # Returns the number of a given marker on the field
    def count_marker(self, marker):
        count = 0
        for i in range(self.length):
            for j in range(self.length):
                if self.map[i][j] == marker:
                    count += 1
        return count
