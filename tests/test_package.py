import pytest
import os
import filecmp as fc
import autogamess as ag
import numpy as np
from scipy.spatial import distance

csvfile = './input.csv'
title   = 'check/'

def test_new_project(tmpdir):
    ag.new_project(tmpdir.strpath, csvfile, title=title)

    a = fc.dircmp(tmpdir.strpath + title, './correct/NPtest/')
    assert a.left_only == []
    assert a.right_only == []

    return

def test_input_builder(tmpdir):
    ag.input_builder(csvfile, tmpdir.strpath+'/')

    a = tmpdir.strpath+'/' + os.listdir(tmpdir.strpath+'/')[0]
    b = './correct/IBtest/' + os.listdir('./correct/IBtest/')[0]
    if not fc.cmp(a,b):
        assert 0

    return

def test_bond_length_and_angle():
    a1 = ag.make_xzy([0,0,0])
    a2 = ag.make_xzy([1,0,0])
    assert distance.euclidean(a1, a2) == 1
    a1 = ag.make_xzy([0,1,0])
    assert ag.angle_between(a1, a2) == (np.pi/2)
