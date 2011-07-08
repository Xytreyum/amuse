from amuse.test import amusetest

from amuse.support.exceptions import AmuseException
from amuse.support.units import units
from amuse.support.units import constants
from amuse.support.units import nbody_system
from amuse.support.data.core import Particles
from amuse.support.interface import InCodeComponentImplementation
from amuse.support.data import trees

import numpy
import time
import sys

class TestBinaryTree(amusetest.TestCase):
    
    def test1(self):
        particles = Particles(10)
        particles.mass = list(range(10)) | units.kg
        particles[0].child1 = particles[1]
        particles[0].child2 = particles[2]
        
        self.assertEquals(particles[0].mass, 0 | units.kg)
        self.assertEquals(particles[0].child1.mass, 1 | units.kg)
        self.assertEquals(particles[1].child1, None)
    
        children1 = particles.child1.select_array(lambda x  : x > 0, ['key',])
        children2 = particles.child2.select_array(lambda x  : x > 0, ['key',])
        children = children1 + children2
        roots = particles - children
    
        print len(roots)
        self.assertEquals(len(roots), 8)
        self.assertEquals(len(children), 2)
        
    def test2(self):
        n = 100000
        particles = Particles(n)
        particles.mass = list(range(n)) | units.kg
        particles[n-1].child1 = particles[0]
        particles[n-1].child2 = particles[1]
        
        self.assertEquals(particles[0].mass, 0 | units.kg)
        self.assertEquals(particles[n-1].child1.mass, 0 | units.kg)
        self.assertEquals(particles[n-1].child2.mass, 1 | units.kg)
    
        children1 = particles.child1.select_array(lambda x  : x > 0, ['key',])
        children2 = particles.child2.select_array(lambda x  : x > 0, ['key',])
        children = children1 + children2
        roots = particles - children
    
        self.assertEquals(len(roots), n - 2)
        self.assertEquals(len(children), 2)
    
        binaries = particles.select_array(lambda x  : x.key > 0, ['child1',])
        self.assertEquals(len(binaries), 1)
    def test3(self):
        n = 10
        particles = Particles(n)
        particles.mass = list(range(n)) | units.kg
        particles[0].child1 = particles[1]
        particles[0].child2 = particles[2]
        particles[1].child1 = particles[3]
        particles[1].child2 = particles[4]
        
        self.assertEquals(particles[0].child1.child1.mass, 3 | units.kg)
    
        binaries = particles.select_array(lambda x : x.key > 0, ["child1",])
    
        print len(binaries)
        self.assertEquals(len(binaries), 2)
    
        binaries_children1 = binaries.child1.select_array(lambda x : x > 0, ["key",]).select_array(lambda x : x.key > 0, ["child1",])
        binaries_children2 = binaries.child2.select_array(lambda x : x > 0, ["key",]).select_array(lambda x : x.key > 0, ["child1",])
        binaries_roots = binaries - (binaries_children1 + binaries_children2)
    
        self.assertEquals(len(binaries_roots), 1)

        self.assertEquals(binaries_roots[0].mass, 0 | units.kg)


    def test4(self):
        particles = Particles(10)
        particles.mass = list(range(10)) | units.kg
        particles[0].child1 = particles[1]
        particles[0].child2 = particles[2]
        particles[1].child1 = particles[3]
        particles[1].child2 = particles[4]
    
        x = trees.BinaryTreesOnAParticleSet(particles, "child1", "child2")
        roots = list(x.iter_roots())
    
        self.assertEquals(len(roots), 1)
        x = [x.mass.value_in(units.kg) for x in roots[0].iter_descendants()]
        self.assertEquals(x, [1,2,3,4])
        self.assertEquals(roots[0].get_descendants_subset().mass, [1,2,3,4] | units.kg)
