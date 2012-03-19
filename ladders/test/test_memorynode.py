import unittest

from ladders.test import memorynode


class TestMemoryNode(unittest.TestCase):
    def test_access(self):
        n = memorynode.MemoryNode(1)
        self.assertFalse(n.readFrom)
        n.children
        self.assertTrue(n.readFrom)


    def test_access_reset(self):
        n = memorynode.MemoryNode(1)
        n.children
        n.reset()
        self.assertFalse(n.readFrom)        


    def test_mutation(self):
        n = memorynode.MemoryNode(1)
        self.assertFalse(n.readFrom)
        n.children.add(memorynode.MemoryNode(2))
        self.assertTrue(n.readFrom)


    def test_mutation_reset(self):
        n = memorynode.MemoryNode(1)
        n.children.add(memorynode.MemoryNode(2))
        n.reset()
        self.assertFalse(n.readFrom)


    def test_assignment(self):
        n = memorynode.MemoryNode(1)
        self.assertFalse(n.writtenTo)
        n.children = set()
        self.assertTrue(n.writtenTo)


    def test_assignment_reset(self):
        n = memorynode.MemoryNode(1)
        n.children = set()
        n.reset()
        self.assertFalse(n.writtenTo)
