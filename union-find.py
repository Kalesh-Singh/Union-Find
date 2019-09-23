# ------------------ UnionFind / Disjoint Set Data Structure -------------------------

class UnionFind:
    def __init__(self, size):
        """ Initializes the data structure. """
        # The number of element in this union find
        self.size = size
        # Tracks the number of components in the union find
        self.num_components = size
        # Each component is initially of size 1
        self.comp_size = [1] * size
        # Each component is initially its own parent/root (self loop)
        self.id = [i for i in range(size)]

    def find(self, p):
        """ Finds which component/set 'p' belongs to in amortized constant time. """

        # Find the root of the component/set
        root = p
        while root != self.id[root]:
            root = self.id[root]

        # Compress the path leading back to the root
        # This operation is called "path compression" and is
        # waht gives the amortized constant time complexity.
        while p != root:
            next = self.id[p]
            self.id[p] = root
            p = next

        return root

    def connected(self, p, q):
        """ Returns whether or not the components 'p' and 'q'
        are in the same component/set. """
        return self.find(p) == self.find(q)

    def component_size(self, p):
        """ Returns the size of the component/set 'p' belongs to. """
        return self.comp_size[self.find(p)]

    def size(self):
        """ Returns the number of elements in the UnionFind/Disjoint set. """
        return self.size

    def components(self):
        """ Returns the number of remaining components/sets. """
        return self.num_components

    def unify(self, p, q):
        """ Unify the components/sets containing p/q. """
        root1, root2 = self.find(p), self.find(q)

        # If the elements are already in the same set
        if root1 == root2:
            return

        # Merge the smaller component/set into the larger one.
        if self.comp_size[root1] < self.comp_size[root2]:
            self.comp_size[root2] += self.comp_size[root1]
            self.id[root1] = root2
        else:
            self.comp_size[root1] += self.comp_size[root2]
            self.id[root2] = root1

        # Since the roots found were different, we know that the
        # number of components/sets has decreased by one.
        self.num_components -= 1

# -------------------------------------------------------------------------------

# --------------------------------- Tests ---------------------------------------
# This is an array based union find which is very efficient.
# However, we will need to create an arbitraty mapping
# between the n nodes and the set of number from 0 to n-1.

# These test can be run with pytest -v <filename>

def test_union_find():
    nodes = list('abcdefghijkl')

    map = {node:i for i, node in enumerate(nodes)}

    uf = UnionFind(len(nodes))

    uf.unify(map['c'], map['k'])
    assert uf.find(map['k']) == map['c']
    assert uf.find(map['c']) == map['c']

    uf.unify(map['f'], map['e'])
    assert uf.find(map['e']) == map['f']
    assert uf.find(map['f']) == map['f']

    uf.unify(map['a'], map['j'])
    assert uf.find(map['j']) == map['a']
    assert uf.find(map['a']) == map['a']

    uf.unify(map['a'], map['b'])
    assert uf.find(map['b']) == map['a']
    assert uf.find(map['a']) == map['a']

    uf.unify(map['c'], map['d'])
    assert uf.find(map['d']) == map['c']
    assert uf.find(map['c']) == map['c']

    uf.unify(map['d'], map['i'])
    assert uf.find(map['i']) == map['c']
    assert uf.find(map['d']) == map['c']

    uf.unify(map['l'], map['f'])
    assert uf.find(map['f']) == map['f']
    assert uf.find(map['l']) == map['f']

    uf.unify(map['c'], map['a'])
    assert uf.find(map['a']) == map['c']
    assert uf.find(map['c']) == map['c']

    uf.unify(map['a'], map['b'])
    assert uf.find(map['b']) == map['c']
    assert uf.find(map['a']) == map['c']

    uf.unify(map['h'], map['g'])
    assert uf.find(map['g']) == map['h']
    assert uf.find(map['h']) == map['h']

    uf.unify(map['h'], map['f'])
    assert uf.find(map['f']) == map['f']
    assert uf.find(map['h']) == map['f']

    uf.unify(map['h'], map['b'])
    assert uf.find(map['b']) == map['c']
    assert uf.find(map['h']) == map['c']

