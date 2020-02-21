#!/usr/bin/env python3
from astropy.io import fits
import glob
import numpy as np
import matplotlib.pyplot as plt

'''
 Este script processa as imagens avg_###nm.fits geradas pelo process_fits.py,
 associadas aos respectivos comprimentos de onda ###nm, integra as contagens
 no CCD e calcula os fluxos dos fótons segundo o fotômetro e segundo o CCD,
 computando as eficiências quânticas em função do comprimento de onda.
 
 NECESSÁRIO SETAR OS PARÂMETROS DAS IMAGENS NOS CAMPOS ABAIXO.
 
 
 Autor: Daniel Bednarski
 Data: 2020-02-19
 
'''


folder = '.' # where are the avg_*.fits files
#phot_file="ocam_300_to_900.dat"
phot_file="ocam_320_to_400.dat" # the name (with path, if needed) of photometer output file
gain = 26.07/300 # e/ADU
pix_size=24e-6 # in meters
phot_size=0.011 # photometer side, in meters
texp = 0.01 # s


h = 6.62607004e-34 # J.s
c = 299792458      # m/s

print("WARNING: you need to set the correct parameters inside\n"+ \
        "QE_counts script!!! Otherwise, the data will be wrong!!!\n")

list_images = np.sort(glob.glob("{}/avg_*.fits".format(folder)))

#bias = fits.open("test_002/bias01.fits")[0].data
#bias = bias[130:170, 130:170]  # crop bias image

wavelengths = np.array([])
counts = np.array([])

for img in list_images:
    image = fits.open(img)[0].data
    image = image[130:170, 130:170]    # define HERE the CCD region over which to compute
                                       # the Quantum Efficiency

    counts = np.append(counts, [np.sum(image)])
    wl = img.split('/')[-1][4:7]    # pega o comprimento de onda dos nomes
#    print(wl)
    wavelengths = np.append(wavelengths, [float(wl)])
   
    
# Abaixo, plota a última imagem, se necessário.
#plt.imshow(image_proc, cmap='gray')


# No fotômetro:
# N_fotons = Wλ/hc
# F_fotons = N/(l_fotômetro^2) # em fótons/s/m^2

# 1e-9 surge porque os λ estão em nm
flux_phot = np.loadtxt(phot_file)*wavelengths*1e-9/(h*c*(phot_size**2))

# No CCD:
# N_elétrons = N_contagens * ganho
# 'F'_elétrons = N_elétrons / (l_seção_CCD * Texp)  o número de elétrons/s/m^2
flux_ccd = counts*gain/(((pix_size*(170-130))**2)*texp)

QE = flux_ccd/flux_phot

print("*"*40+"\nSUMMARY FROM {} TO {} nm, IN STEPS OF {} nm\n".format(wavelengths[0],wavelengths[-1],wavelengths[1]-wavelengths[0]))
print("Counts in CCD (ADU)")
print(counts)
print("\nFlux on CCD (electron/s/m^2)")
print(flux_ccd)
print("\nFlux on Photometer (photon/s/m^2)")
print(flux_phot)
print("\nQE (%)")
print(QE*100)
print("\n"+"*"*40)

plt.xticks(wavelengths)
plt.plot(wavelengths,QE*100, 'o-')
plt.minorticks_on()
plt.xlabel(r'$\lambda$ (nm)')
plt.ylabel(r'QE (%)')
plt.show()

