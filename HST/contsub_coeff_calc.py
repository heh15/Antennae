import matplotlib.pyplot as plt
import numpy as np

def fit_proportional(x, y):
    '''
    Fit the linear relation forced through 0 point
    ------
    Parameters:
    x: np.1darray
        x of the data
    y: np.1darray
        y of the data
    ------
    return:
    a: float
        coefficient between x and y
    '''
    x = x[:,np.newaxis]
    a,_,_,_ = np.linalg.lstsq(x,y)

    return a


Dir = '/home/heh15/research/Antennae/'
picDir = Dir + 'pictures/'

flux_128N = np.array([3.1e2,1.226e1,3.53e1,7.82,6.57e2,1.44e2])
flux_J = np.array([1.13e4,4.121e2,1.093e3,2.67e2,2.174e4,4.459e3])

flux_128N_bkg = np.array([3.25,0.94,0.85,0.69,23,10.3])
flux_J_bkg = np.array([123,30.6,49.7,38.3,721,293])

flux_128N_corr = flux_128N - flux_128N_bkg
flux_J_corr = flux_J - flux_J_bkg 

a = fit_proportional(flux_J_corr, flux_128N_corr)
print(a[0])

fig = plt.figure()
plt.xlabel('F116W flux')
plt.ylabel('F128N flux')
plt.scatter(flux_J_corr, flux_128N_corr)
plt.plot(flux_J_corr, a*flux_J_corr, color='red', label='coeff=0.0296')
plt.legend()
plt.savefig(picDir+'contsub_compare.pdf', bbox_inches='tight',pad_inches=0.02)
