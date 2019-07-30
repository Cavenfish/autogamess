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

    tmp=ag.read_file(a)
    tmp[0] = '! AutoGAMESS TEST\n'
    f=open(a,'w')
    f.writelines(tmp)
    f.close()

    if not fc.cmp(a,b):
        assert 0

    return

def test_bond_length_and_angle():
    a1 = ag.make_xzy([0,0,0])
    a2 = ag.make_xzy([1,0,0])
    assert distance.euclidean(a1, a2) == 1
    a1 = ag.make_xzy([0,1,0])
    assert ag.angle_between(a1, a2) == (np.pi/2)

    return

def test_get_data():
    optfile = './correct/GDtest/AG-test_H2O_B3LYP_CCD_opt.log'
    hesfile = './correct/GDtest/AG-test_H2O_B3LYP_CCD_hes.log'
    ramfile = './correct/GDtest/AG-test_H2O_B3LYP_CCD_raman.log'

    optdata = ag.get_data(optfile)
    hesdata = ag.get_data(hesfile)
    ramdata = ag.get_data(ramfile)

    bl = {'O-O Bond Length': '0.0', 'O-H Bond Length': '0.9689082029181745',
          'O-2H Bond Length': '0.9689082029181745',
          'H-O Bond Length': '0.9689082029181745', 'H-H Bond Length': '0.0',
          'H-2H Bond Length': '1.513601111',
          '2H-O Bond Length': '0.9689082029181745',
          '2H-H Bond Length': '1.513601111', '2H-2H Bond Length': '0.0'}

    ba = {'O-O Bond Angle': '0.0', 'O-H Bond Angle': '2.2351823705521188',
          'O-2H Bond Angle': '2.2351823705521188',
          'H-O Bond Angle': '2.2351823705521188', 'H-H Bond Angle': '0.0',
          'H-2H Bond Angle': '1.8128205660753491',
          '2H-O Bond Angle': '2.2351823705521188',
          '2H-H Bond Angle': '1.8128205660753491', '2H-2H Bond Angle': '0.0'}

    vf = {'A1': ['1658.10', '3748.38'], 'B2': ['3849.75']}
    ir = {'A1': ['1.31680', '0.06712'], 'B2': ['0.46621']}
    ra = {'A1': ['6.244', '73.030'], 'B2': ['33.310']}

    assert optdata.bond_lengths == bl
    assert optdata.bond_angles  == ba
    assert hesdata.vib_freq     == vf
    assert hesdata.ir_inten     == ir
    assert ramdata.raman        == ra

    return
