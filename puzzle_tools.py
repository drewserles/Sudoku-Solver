"""
Some functions for working with puzzles
"""
# from sudoku_puzzle import SudokuPuzzle <- delete when done
from puzzle import Puzzle
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# you may uncomment the next lines on a unix system such as CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None
    """
    # seen puzzle configurations.
    # Credit to Brian Law on the forums for the tip on implementing this as
    # a set. https://piazza.com/class/ijagzkkg1y5r0?cid=1197
    seen = {puzzle.__str__()}
    for n in puzzle.extensions():
        # call helper function to perform recursion.
        rtrn = dfs_helper(n, seen)
        if rtrn is not None:
            return PuzzleNode(puzzle, [rtrn])


def dfs_helper(n_puzzle, lst):
    """
    Helper function called by depth_first_solve. This helper handles the
    recursion on the extensions so depth_first_solve can track seen puzzles.
    @type n_puzzle: Puzzle
    @type lst: set[Puzzle]
    @rtype: PuzzleNode | None
    """
    if n_puzzle is None:
        return None
    elif n_puzzle.__str__() in lst:
        return None
    elif n_puzzle.fail_fast():
        lst.add(n_puzzle.__str__())
        return None
    elif n_puzzle.is_solved():
        # return the linked list node
        return PuzzleNode(n_puzzle)
    else:
        # n_puzzle hasn't been seen before so add it
        lst.add(n_puzzle.__str__())
        for n in n_puzzle.extensions():
            rtrn = dfs_helper(n, lst)
            if rtrn is not None:
                # Create new PuzzleNode with rtrn as child
                return PuzzleNode(n_puzzle, [rtrn])
        return None


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None
    """
    # set of seen puzzles, list of extensions, root as PuzzleNode
    seen = {puzzle.__str__()}
    ext_list = []
    pp = PuzzleNode(puzzle)
    if puzzle.is_solved():
        return pp
    else:
        for item in puzzle.extensions():
            child = PuzzleNode(item, None, pp)
            # add extensions as children of pp PuzzleNode
            pp.children.append(child)
            ext_list.append(child)
        rtrn = bfs_helper(ext_list, seen)
        if rtrn is not None:
            return PuzzleNode(puzzle, [rtrn])


def bfs_helper(puzzle_extensions, seen_puzzles):
    """
    Helper function called by breadth_first_solve. This helper handles the
    recursion on the extensions so breadth_first_solve can track seen puzzles.
    @type puzzle_extensions: list[PuzzleNode]
    @type seen_puzzles: set[Puzzle]
    @rtype: PuzzleNode | None
    """
    next_level = []
    for puzz in puzzle_extensions:
        if puzz.puzzle.is_solved():
            return puzz
        if ((puzz.puzzle.__str__() not in seen_puzzles) and
                (not puzz.puzzle.fail_fast()) and (puzz is not None)):
            seen_puzzles.add(puzz.puzzle.__str__())
            # If puzzle isn't solved, make PuzzleNodes out of the extensions
            # and append them to puzzle's children
            for np in puzz.puzzle.extensions():
                child = PuzzleNode(np, None, puzz)
                puzz.children.append(child)
                next_level.append(child)
    if len(next_level) > 0:
        rtrn = bfs_helper(next_level, seen_puzzles)
    # If solution is found, update the child link so a single path is returned
        if rtrn is not None:
            path_parent = rtrn.parent
            path_parent.children = [rtrn]
            return path_parent
    # else:
    return None


class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode] | None
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))


def gather_lists(list_):
    """
    Return the concatenation of the sublists of list_.

    @param list[PuzzleNode] list_: list of sublists
    @rtype: list

    [1, 2, 3, 4]
    """
    # this is a case where list comprehension gets a bit unreadable
    new_list = []
    for sub in list_:
        for element in sub:
            new_list.append(element)
    return new_list


