import sys

from crossword import *

from collections import deque


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        for variable in self.domains:
            
            remove_words = set()
            
            for word in self.domains[variable]:

                if variable.length != len(word):
                    remove_words.add(word)

            for word in remove_words:
                self.domains[variable].remove(word)
                    

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        overlap = self.crossword.overlaps[x,y]

        i = overlap[0]
        j = overlap[1]

        n = len(self.domains[x])

        # print(self.domains[x])

        for word1 in self.domains[x].copy():

            has = False

            for word2 in self.domains[y]:

                if word1[i] == word2[j]: 

                    has = True  
                    break

            if not has:
                    
                self.domains[x].remove(word1)

        if n > len(self.domains[x]):
            return True
        
        # print(self.domains[x])

        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        agenda = deque()

        if arcs == None:

            for var1 in self.domains:
                for var2 in self.domains:

                    if var1 == var2:
                        continue

                    if self.crossword.overlaps[var1,var2] is not None:

                        agenda.append((var1, var2))
                        agenda.append((var2, var1))
            
        else:
            agenda = deque(arcs) 

        while agenda:

            cur = agenda.popleft()

            x = cur[0]
            y = cur[1]

            if self.revise(x,y):
                 
                 if len(self.domain[x]) == 0:
                     
                     return False
                 
                 neighbors = self.crossword.neighbors(x)

                 for k in neighbors:
                     
                     if k != y:
                         
                        agenda.append((k,x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for var in assignment:
            if assignment[var] == None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for var in assignment:

            for word in assignment[var]:
                if var.length != len(word):
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        result = {}

        for word in self.domains[var]:

            count = 0

            neighbors = self.crossword.neighbors(var)

            for neighbor in neighbors:
                
                if neighbor not in assignment:
                    
                    overlap = self.crossword.overlaps[var,neighbor]

                    if not overlap:
                        continue

                    i,j = overlap

                    for neighbor_word in self.domains[neighbor]:
                        if word[i] != neighbor_word[j]:
                            count +=1
                
            result[word] = count

        return sorted(result, key=lambda word:result[word])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_dict_values = {}
        unassigned_dict_neighbors = {}

        for variable in self.domain:

            if variable not in assignment:

                #matches variable with len of num variables
                unassigned_dict_values[variable] = len(self.domains[variable])

                neighbors = self.crossword.neighbors[variable]

                #matches variable with num of neighbors
                unassigned_dict_neighbors[variable] = len(neighbors)
        

        min_value = min(unassigned_dict_values.values())

        vars_w_min_words = [key for key, value in unassigned_dict_values.items() if value == min_value]

        if len(vars_w_min_words) == 1:
            return vars_w_min_words[0]
        
        elif len(vars_w_min_words) > 1:
                
            max_value = max(unassigned_dict_neighbors.values())

            vars_w_max_neighbors = [key for key,value in unassigned_dict_neighbors.items() if value == max_value]

            return vars_w_max_neighbors[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
