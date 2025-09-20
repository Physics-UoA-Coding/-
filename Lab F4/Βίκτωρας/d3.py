import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat
from uncertainties import unumpy as unp

# Σταθερές κυκλώματος
R = 12.9 # Ω
C = 0.46e-6  # F
L = 2.13e-3  # H
VS = 0.5  # V

f0_exp = 5080 # Hz
f0_th = 1/(2*np.pi*np.sqrt(L*C))

# Πειραματικά δεδομένα
f_exp = np.array([4300, 4430, 4544, 4784, 4880, 4945, 5080, 5212, 5377, 5577, 5700, 5820, 5970])
I_mA = np.array([19.2, 22.18, 24.9, 32.6, 35.31, 37.04, 38, 37.39, 32.37, 27.5, 24.62, 22.3, 19.69])
VL = np.array([1.106, 1.316, 1.516, 2.085, 2.3, 2.446, 2.56, 2.596, 2.331, 2.041, 1.867, 1.725, 1.557])
VC = np.array([1.546, 1.735, 1.9, 2.36, 2.5, 2.591, 2.59, 2.476, 2.067, 1.7, 1.487, 1.32, 1.132])
VR = np.array([0.192, 0.222, 0.255, 0.326, 0.353, 0.37, 0.385, 0.372, 0.322, 0.273, 0.245, 0.221, 0.195])

# Μετατροπή μονάδων
I_exp = I_mA / 1000  # A


# --- Υπολογισμός γωνιακής συχνότητας ---
omega = 2 * np.pi * f_exp

# --- Υπολογισμός R και C για κάθε μέτρηση ---
R_exp = VR / I_exp
C_exp = I_exp / (omega * VC)

# --- Υπολογισμός μέσων όρων και σφαλμάτων μέσω διασποράς ---
def mean_with_std_error(values):
    mean = np.mean(values)
    std_err = np.std(values, ddof=1) / np.sqrt(len(values))
    return ufloat(mean, std_err)


VS_array = np.full_like(I_exp, 0.5)  # array με 0.5 για κάθε σημείο
R_avg = mean_with_std_error(R_exp)
C_avg = mean_with_std_error(C_exp)
L_exp = 1 /((2*np.pi*f0_exp)**2 * C_avg)
RL_exp = []

for i in range(len(VS_array)):
    term1 = (VS_array[i]**2) / (I_exp[i]**2)
    reactive = (omega[i] * L_exp - 1 / (omega[i] * C_avg))**2
    RL = unp.sqrt(term1 - reactive) - R_avg
    RL_exp.append(RL)

# Υπολογισμός μέσου όρου και σφάλματος
def mean_with_std_error_ufloat(uf_array):
    nom = np.array([x.nominal_value for x in uf_array])
    stds = np.array([x.std_dev for x in uf_array])
    mean = np.mean(nom)
    std_err = np.sqrt(np.sum(stds**2)) / len(uf_array)
    return ufloat(mean, std_err)

RL_avg = mean_with_std_error_ufloat(RL_exp)
R_full = unp.uarray(R_exp, np.zeros_like(R_exp)) + RL_avg
R_full_avg = mean_with_std_error_ufloat(R_full)

print(f"Πειραματικά: R = {R_avg:.3uP} Ω")
print(f"Πειραματικά: C = {C_avg:.3uP} F")
print(f"Πειραματικά: L = {L_exp:.3uP} H")
print(f"Πειραματικά: RL = {RL_avg:.3uP} Ω")
print(f"Η ολική αντίσταση πειραματικά είναι {R_full_avg:.3uP} Ω")

phi_exp = np.arccos((VS**2 + VR**2 + VC**2 - VL**2)/(2*VS*np.sqrt(VR**2 + VC**2))) - np.arccos(VR/np.sqrt(VR**2 + VC**2))
Z_exp = VS/I_exp
P_exp = VS*I_exp*np.cos(phi_exp)

# Πυκνό πλέγμα συχνοτήτων για θεωρητικές καμπύλες
f_theo = np.linspace(min(f_exp), max(f_exp), 1000)
omega_theo = 2 * np.pi * f_theo

# Θεωρητικές συναρτήσεις
Z_theo = np.sqrt(R**2 + (omega_theo * L - 1 / (omega_theo * C))**2)
I_theo = VS / Z_theo
phi_theo = np.arctan((omega_theo * L - 1 / (omega_theo * C)) / R)
P_theo = I_theo**2 * R

print(f"Η θεωρητική τιμή της συχνότητας συντονισμού είναι {f0_th} Hz")
print(f"Σχετική απόκλιση με την πειραματική: {100*abs((f0_exp - f0_th)/f0_th)}% \n")

# Εύρος Ζώνης
omega1 = (-R*C + np.sqrt(R**2*C**2 + 4*L*C))/(2*L*C)
omega2 = (R*C + np.sqrt(R**2*C**2 + 4*L*C))/(2*L*C)
bandwidth = omega2 - omega1
print(f"Το εύρος ζώνης είναι {bandwidth/(2*np.pi)} Hz")

# Συντελεστής ποιότητας
Q = 2*np.pi*f0_exp*L/R
print(f"Ο συντελεστής ποιότητας είναι {Q} \n")

# Διαγράμματα
plt.figure(figsize=(12, 10))

# 1. Ρεύμα vs Συχνότητα
plt.subplot(2, 2, 1)
plt.plot(f_theo, I_theo * 1000, 'b-', label='Θεωρητικό I(ω)')
plt.plot(f_exp, I_mA, 'ro', label='Πειραματικό I')
plt.xlabel('f (Hz)')
plt.ylabel('I (mA)')
plt.title('Ρεύμα vs Συχνότητα')
plt.legend()
plt.grid(True)

# 2. Φάση vs Συχνότητα
plt.subplot(2, 2, 2)
plt.plot(f_theo, phi_theo, 'b-', label='Θεωρητικό φ(ω)')
plt.plot(f_exp, phi_exp, 'ro', label='Πειραματικό φ')
plt.xlabel('f (Hz)')
plt.ylabel('φ (rad)')
plt.title('Φάση vs Συχνότητα')
plt.legend()
plt.grid(True)

# 3. Εμπέδηση vs Συχνότητα
plt.subplot(2, 2, 3)
plt.plot(f_theo, Z_theo, 'b-', label='Θεωρητικό Z(ω)')
plt.plot(f_exp, Z_exp, 'ro', label='Πειραματικό Z')
plt.xlabel('f (Hz)')
plt.ylabel('Z (Ω)')
plt.title('Εμπέδηση vs Συχνότητα')
plt.legend()
plt.grid(True)

# 4. Ισχύς vs Συχνότητα
plt.subplot(2, 2, 4)
plt.plot(f_theo, P_theo, 'b-', label='Θεωρητικό <P>(ω)')
plt.plot(f_exp, P_exp, 'ro', label='Πειραματικό <P>')
plt.xlabel('f (Hz)')
plt.ylabel('<P> (W)')
plt.title('Ισχύς vs Συχνότητα')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Υπολογισμός θεωρητικών τιμών στα πειραματικά σημεία
omega_exp = 2 * np.pi * f_exp
Z_theo_exp = np.sqrt(R**2 + (omega_exp * L - 1 / (omega_exp * C))**2)
I_theo_exp = VS / Z_theo_exp
phi_theo_exp = np.arctan((omega_exp * L - 1 / (omega_exp * C)) / R)
P_theo_exp = I_theo_exp**2 * R

# Υπολογισμός σχετικής απόκλισης (%)
rel_error_I = np.abs((I_exp - I_theo_exp) / I_theo_exp) * 100
rel_error_phi = np.abs((phi_exp - phi_theo_exp) / phi_theo_exp) * 100
rel_error_Z = np.abs((Z_exp - Z_theo_exp) / Z_theo_exp) * 100
rel_error_P = np.abs((P_exp - P_theo_exp) / P_theo_exp) * 100

# Διάγραμμα σχετικών αποκλίσεων
plt.figure(figsize=(10, 6))
plt.plot(f_exp, rel_error_I, 'r-o', label='Ρεύμα')
#plt.plot(f_exp, rel_error_phi, 'g-o', label='Φάση')
plt.plot(f_exp, rel_error_Z, 'b-o', label='Εμπέδηση')
plt.plot(f_exp, rel_error_P, 'm-o', label='Ισχύς')

plt.xlabel('Συχνότητα (Hz)')
plt.ylabel('Σχετική Απόκλιση (%)')
plt.title('Σχετική Απόκλιση Πειραματικών Τιμών από Θεωρία')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()