#from landlab import Component, FieldError
import numpy as np
from olm.calcite import concCaEqFromPCO2, palmerRate, calc_K_H
from olm.general import CtoK

secs_per_year = 365.*24.*60.*60.
mm_per_cm = 10.
cm_per_m = 100.
mw_Calcite = 100.09
L_per_m3 = 1000.

def calcite_diss_palmer_transfer(Ca=None,
                        PCO2=None,
                        hydraulic__diameter=None,
                        conduit__discharge=None,
                        length = None,
                        T_C=15., rho=2.6, impure=True):
    #print('PCO2=',PCO2)
#    if np.size(PCO2)==1:
#        PCO2 = PCO2[0]#Convert to float, otherwise Eq calc crashes
#    eqCas = concCaEqFromPCO2(PCO2,T_C=T_C)
#    Sat_Ratios = Ca/eqCas
    rates = np.zeros(np.size(Ca))
    for i, this_Ca in enumerate(Ca):
        eqCa = concCaEqFromPCO2(PCO2[i], T_C=T_C)
        ratio = this_Ca/eqCa
        rates[i] = palmerRate(T_C, PCO2[i], ratio, rho=rho, impure=True)
    #Convert rate to mol/s/m^2
    rates = (rho*rates/secs_per_year/mm_per_cm/mw_Calcite)*cm_per_m**2
    #for now assume circular conduit
    diss_flux = np.pi*length*hydraulic__diameter*rates# mol/s
    input_Ca_flux = Ca*L_per_m3*conduit__discharge
    output_Ca_flux = input_Ca_flux + diss_flux
    conc_Ca_out = output_Ca_flux/(conduit__discharge*L_per_m3)#mol/L
    #Calculate mol/L of carbonic acid + aqueous CO2
    K_H = calc_K_H(CtoK(T_C))
    conc_CO2 = PCO2*K_H
    input_CO2_flux = conc_CO2*L_per_m3*conduit__discharge
    output_CO2_flux = input_CO2_flux - diss_flux #mol of H2CO3s lost for every mol of Ca added
    conc_CO2_out = output_CO2_flux/(conduit__discharge*L_per_m3)
    PCO2_out = conc_CO2_out/K_H
    return {'solutes':{'Ca':conc_Ca_out, 'PCO2':PCO2_out},'new_link_values':{'diss__rates':rates}}
