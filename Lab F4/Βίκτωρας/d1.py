from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np

e_theoretical_over_m = 1.758820e11  # C/kg
e_charge = 1.602176634e-19  # C
mu_0 = 1.25663706e-6   # Διαπερατότητα κενού (H/m)
N = 130  # Πλήθος σπειρών
R = 0.15  # Ακτίνα πηνίου (m)
c = 2.99792458e8  # m/s (ταχύτητα φωτός)
A = 0.715 * mu_0 * N / R

V_c = c**2/(8*e_theoretical_over_m)

datasets = {
    288.2: [(10.7, 1.14), (5.9, 1.83), (4.9, 1.94), (5.8, 1.63), (7.7, 1.42), (10.1, 1.2), (7.8, 1.51)],
    305.4: [(10.1, 1.14), (6.3, 1.83), (6.2, 1.93), (7.8, 1.63), (8.4, 1.42), (10.6, 1.2), (8.4, 1.51)],
    275.5: [(8.9, 1.14), (5.3, 1.83), (4.8, 1.92), (6.2, 1.63), (7.3, 1.42), (10.7, 1.2), (6.7, 1.51)],
    297.8: [(10.9, 1.14), (6.2, 1.83), (5.5, 1.92), (8.0, 1.63), (7.3, 1.42), (10.7, 1.2), (7.7, 1.51)],
}

for voltage, data in datasets.items():
    d_mm_inv = [2 / (d * 10) for d, _ in data]
    B = [A * I for _, I in data]
    
    point_plot = plt.plot(d_mm_inv, B, 'o', label=f'V = {voltage} V')
    color = point_plot[0].get_color()

    slope, intercept, r_value, p_value, std_err = linregress(d_mm_inv, B)
    x_fit = sorted(d_mm_inv)
    y_fit = [slope * x + intercept for x in x_fit]
    plt.plot(x_fit, y_fit, linestyle='--', color=color,
             label=f'Fit V={voltage}V (R²={r_value**2:.3f})')

    # Κλίση και σφάλμα σε SI μονάδες
    k_si = slope * 1e-3  # T·m
    delta_k_si = std_err * 1e-3

    # e/m και σφάλμα
    e_over_m = (2 * voltage) / (k_si ** 2)
    delta_e_over_m = abs((4 * voltage) / (k_si ** 3)) * delta_k_si

    # Μάζα και σφάλμα
    m_electron = e_charge / e_over_m
    delta_m = e_charge / (e_over_m ** 2) * delta_e_over_m

    # Ταχύτητα και σφάλμα
    v_electron = np.sqrt(2 * e_charge * voltage / m_electron)
    delta_v = (e_charge * voltage) / (v_electron * m_electron ** 2) * delta_m

    # γ και σφάλμα
    gamma = 1 / np.sqrt(1 - (v_electron / c) ** 2)
    delta_gamma = (v_electron / c**2) / (1 - (v_electron / c)**2)**(3/2) * delta_v

    # Εκτύπωση
    print(f"Τάση {voltage} V:")
    print(f"  Κλίση: k = ({k_si:.5e} ± {delta_k_si:.2e}) T·m")
    print(f"  e/m = ({e_over_m:.5e} ± {delta_e_over_m:.2e}) C/kg")
    print(f"  e/m θεωρ. = {e_theoretical_over_m:.5e} C/kg")
    print(f"  Σχετικό σφάλμα e/m: {abs(e_over_m - e_theoretical_over_m)/e_theoretical_over_m * 100:.2f}%")
    print(f"  Μάζα: m = ({m_electron:.5e} ± {delta_m:.2e}) kg")
    print(f"  Ταχύτητα: v = ({v_electron:.5e} ± {delta_v:.2e}) m/s")
    print(f"  Συντελεστής γ = ({gamma:.8f} ± {delta_gamma:.2e})\n")
print(f"Η τάση που πρέπει να εφαρμόσουμε ώστε η ταχύτητα των ηλεκτρονίων να γίνει η μισή της ταχύτητας του φωτός είναι {V_c} Volts")
# Διαμόρφωση γραφήματος
plt.xlabel('1 / r (mm⁻¹)')
plt.ylabel('B (Tesla)')
plt.title('Διάγραμμα B - (1/r) με ευθείες ελάχιστων τετραγώνων')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("d1.jpg")
plt.show()