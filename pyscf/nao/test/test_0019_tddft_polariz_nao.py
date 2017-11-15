from __future__ import print_function, division
import os,unittest,numpy as np
from pyscf.nao import tddft_iter

dname = os.path.dirname(os.path.abspath(__file__))
td = tddft_iter(label='water', cd=dname, jcutoff=7, iter_broadening=1e-2, xc_code='RPA')

class KnowValues(unittest.TestCase):

  def test_non_inter_polariz(self):
    """ This is non-interacting polarizability TDDFT with SIESTA starting point """
    omegas = np.linspace(0.0,2.0,500)+1j*td.eps
    pxx = -td.comp_polariz_nonin(omegas).imag
    #pxx = np.zeros_like(omegas)
    #vext = np.transpose(td.moms1)
    #for iomega,omega in enumerate(omegas): pxx[iomega] = -np.dot(td.apply_rf0(vext[0,:], omega), vext[0,:]).imag

    data = np.array([27.2114*omegas.real, pxx])
    data_ref = np.loadtxt(dname+'/water.tddft_iter.omega.pxx.txt-ref')
    self.assertTrue(np.allclose(data_ref,data.T, rtol=1.0, atol=1e-05))
    #np.savetxt('water.tddft_iter.omega.nonin.pxx.txt', data.T, fmt=['%f','%f'])

  def test_inter_polariz(self):
    """ This is interacting polarizability with SIESTA starting point """
    omegas = np.linspace(0.0,2.0,150)+1j*td.eps
    pxx = -td.comp_polariz_inter(omegas).imag
    data = np.array([omegas.real*27.2114, pxx])
    np.savetxt(dname+'/water.tddft_iter.omega.inter.pxx.txt', data.T, fmt=['%f','%f'])
    data_ref = np.loadtxt(dname+'/water.tddft_iter.omega.inter.pxx.txt-ref')
    #print('    td.rf0_ncalls ', td.rf0_ncalls)
    #print(' td.matvec_ncalls ', td.matvec_ncalls)
    self.assertTrue(np.allclose(data_ref,data.T, rtol=1.0, atol=1e-05))


if __name__ == "__main__": unittest.main()
