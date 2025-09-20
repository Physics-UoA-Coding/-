import matplotlib.pyplot as plt
from scipy.stats import linregress

# Φυσικές σταθερές
c = 2.998*10**8  #m/s
e = 1.602e-19  # C
h_true = 6.626e-34  # J·s

# Δεδομένα
wavelengths = [578, 546, 436, 405, 366]  # nm

# Μετατροπή Δεδομένων (Από το μήκος κύματος σε συχνότητες)
frequencies_Hz = [c / (l * 10**(-9)) for l in wavelengths]
frequencies_THz = [f*10**(-12) for f in frequencies_Hz]

vsv_2mm = [0.676, 0.785, 1.311, 1.521, 1.92]
vsv_8mm = [0.692, 0.801, 1.333, 1.555, 1.945]

# Γραμμική παλινδρόμηση
slope_2mm, intercept_2mm, r_val_2mm, p_val_2mm, stderr_2mm = linregress(frequencies_Hz, vsv_2mm)
slope_8mm, intercept_8mm, r_val_8mm, p_val_8mm, stderr_8mm = linregress(frequencies_Hz, vsv_8mm)

r_squared_2mm = r_val_2mm**2
r_squared_8mm = r_val_8mm**2

x_intercept_2mm = -intercept_2mm / slope_2mm
x_intercept_8mm = -intercept_8mm / slope_8mm

# Υπολογισμός h
h_exp_2mm = slope_2mm * e
h_exp_8mm = slope_8mm * e

# Σφάλμα στο h
h_err_2mm = stderr_2mm * e
h_err_8mm = stderr_8mm * e

# Σχετική απόκλιση
rel_dev_2mm = abs((h_exp_2mm - h_true) / h_true) * 100
rel_dev_8mm = abs((h_exp_8mm - h_true) / h_true) * 100

# Εκτύπωση αποτελεσμάτων
print(f"[2mm]")
print(f"  Συσχέτιση: {r_squared_2mm:.4f}")
print(f"  Κλίση: {slope_2mm:.5e} V/Hz ± {stderr_2mm:.2e}")
print(f"  h (πειραματική): {h_exp_2mm:.3e} J·s ± {h_err_2mm:.2e}")
print(f"  Σχετικό σφάλμα: {(h_err_2mm / h_exp_2mm) * 100 :.2f}%")
print(f"  Σχετική απόκλιση: {rel_dev_2mm:.2f}%")
print(f"  Σημείο τομής με τον άξονα x: f = {x_intercept_2mm*1e-12:.2f} THz")
print(f"  Μήκος κύματος κατωφλίου: λ = {c*1e9/x_intercept_2mm} nm \n")

print(f"[8mm]")
print(f"  Συσχέτιση: {r_squared_8mm:.4f}")
print(f"  Κλίση: {slope_8mm:.5e} V/Hz ± {stderr_8mm:.2e}")
print(f"  h (πειραματική): {h_exp_8mm:.3e} J·s ± {h_err_8mm:.2e}")
print(f"  Σχετικό σφάλμα: {(h_err_8mm / h_exp_8mm) * 100 :.2f}%")
print(f"  Σχετική απόκλιση: {rel_dev_8mm:.2f}%")
print(f"  Σημείο τομής με τον άξονα x: f = {x_intercept_8mm*1e-12:.2f} THz")
print(f"  Μήκος κύματος κατωφλίου: λ = {c*1e9/x_intercept_8mm} nm \n")

# Διάγραμμα
plt.figure(figsize=(8, 5))
plt.scatter(frequencies_THz, vsv_2mm, color='blue', label='2mm', marker='o')
plt.scatter(frequencies_THz, vsv_8mm, color='red', label='8mm', marker='s')

plt.xlabel('Συχνότητα (THz)')
plt.ylabel('Τάση αποκοπής (V)')
plt.title('Σχέση Συχνότητας - Τάσης αποκοπής')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()