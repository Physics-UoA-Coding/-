import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

mu_0_th = 4*np.pi*1e-7   # Διαπερατότητα κενού (H/m)

# ΜΕΡΟΣ Α

# Πείραμα Α4

a1 = 0.03 # m

# Μονάδες: B (mT), I (A)
B = np.array([0, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.09, 0.1, 0.12, 0.14])
I = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
B_T = np.array([1e-3*x for x in B])

# Μέθοδος ελαχίστων τετραγώνων
slope, intercept, r_value, p_value, std_err = linregress(I, B_T)

# Υπολογισμός μαγνητικής διαπερατότητας
mu_0 = 2 * slope * a1
mu_0_err = 2 * std_err * a1

# Εκτύπωση αποτελεσμάτων
print(f"Μαγνητική διαπερατότητα του κενού μ₀ = {mu_0:.6e} ± {mu_0_err:.6e} H/m")
rel_error = abs(mu_0 - mu_0_th) / mu_0_th * 100
print(f"Σχετική απόκλιση από τη θεωρητική τιμή: {rel_error:.2f} %")

# Γράφημα
plt.figure(figsize=(8, 6))
plt.plot(I, B_T, 'bo', label='Μετρήσεις')  # μπλε σημεία
plt.plot(I, slope * I + intercept, 'r-', label='Ευθεία ελαχίστων τετραγώνων')  # κόκκινη ευθεία
plt.xlabel("I(A)")
plt.ylabel("B(T)")
plt.title("B(I) και ευθεία ελαχίστων τετραγώνων")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Πείραμα Α5

a2 = 0.06 # m

N1 = [0, 1, 2, 3]
B2 = [0, 0.04, 0.09, 0.13]  # σε mT
B2_T = [1e-3 * x for x in B2]  # σε T

# Γραμμική παλινδρόμηση B = k·N + b
slope2, intercept2, r_value2, p_value2, std_err2 = linregress(N1, B2_T)

# Υπολογισμός μ0 από τη σχέση μ₀ = 2Βα / (5Ν) ⇒ η κλίση είναι η B/N, άρα:
mu_0_2 = 2 * slope2 * a2 / 5
mu_0_2_err = 2 * std_err2 * a2 / 5

# Εκτύπωση αποτελεσμάτων
print("\n=== Υπολογισμός μαγνητικής διαπερατότητας από B–N ===")
print(f"Μαγνητική διαπερατότητα του κενού μ₀ = {mu_0_2:.6e} ± {mu_0_2_err:.6e} H/m")

# Σχετική απόκλιση από θεωρητική τιμή
rel_error2 = abs(mu_0_2 - mu_0_th) / mu_0_th * 100
print(f"Σχετική απόκλιση από τη θεωρητική τιμή: {rel_error2:.2f} %")

# Γράφημα B(N)
N_np = np.array(N1)
plt.figure(figsize=(8, 6))
plt.plot(N1, B2_T, 'bo', label='Μετρήσεις')  # μπλε σημεία
plt.plot(N_np, slope2 * N_np + intercept2, 'r-', label='Ευθεία ελαχ. τετρ.')
plt.xlabel("Αριθμός σπειρών N")
plt.ylabel("Μαγνητικό πεδίο B (T)")
plt.title("B(N) και ευθεία ελαχίστων τετραγώνων")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ΜΕΡΟΣ Β - ΠΗΝΙΟ

N2 = [0, 75, 150, 300]
L = 0.16 # m
n2 = np.array([x/L for x in N2])
B3 = [0, 0.47, 1.05, 2.34]  # σε mT
B3_T = [1e-3 * x for x in B3]  # σε T

# Γραμμική παλινδρόμηση: B = slope * n + intercept
slope3, intercept3, r_value3, p_value3, std_err3 = linregress(n2, B3_T)

# Υπολογισμός μαγνητικής διαπερατότητας
mu_0_3 = slope3
mu_0_3_err = std_err3

# Εκτύπωση
print("\n=== Υπολογισμός μαγνητικής διαπερατότητας από B–n ===")
print(f"Μαγνητική διαπερατότητα του κενού μ₀ = {mu_0_3:.6e} ± {mu_0_3_err:.6e} H/m")

# Σχετική απόκλιση από θεωρητική τιμή
rel_error3 = abs(mu_0_3 - mu_0_th) / mu_0_th * 100
print(f"Σχετική απόκλιση από τη θεωρητική τιμή: {rel_error3:.2f} %")

# Γράφημα
plt.figure(figsize=(8, 6))
plt.plot(n2, B3_T, 'bo', label='Μετρήσεις')  # μπλε σημεία
plt.plot(n2, slope3 * n2 + intercept3, 'r-', label='Ευθεία ελαχ. τετρ.')  # κόκκινη ευθεία
plt.xlabel("n (αριθμός στροφών)")
plt.ylabel("Μαγνητικό πεδίο B (T)")
plt.title("B(n) και ευθεία ελαχίστων τετραγώνων")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#ΠΕΙΡΑΜΑ Β3 & Β4

d1 = 0.026  # διάμετρος πηνίου σε m
d2 = 0.041
I = 1  # Ρεύμα σε A

# Δεδομένα για τα δύο πηνία
coils = [
    {"N": 75, "R": d1/2, "label": "Πηνίο N=75", "x": [], "B_meas": []},
    {"N": 300, "R": d1/2, "label": "Πηνίο N=300", "x": [], "B_meas": []},
    {"N": 300, "R": d2/2, "label": "Πηνίο Διαμέτρου 33mm", "x": [], "B_meas": []}]

# ➤ Δώσε εδώ τις μετρήσεις σου για κάθε πηνίο:

X0 = [-8, -7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]
B0 = [0.17, 0.29, 0.4, 0.46, 0.51, 0.53, 0.55, 0.57, 0.57, 0.57, 0.58, 0.58, 0.59, 0.58, 0.58, 0.58, 0.58, 0.58, 0.59, 0.58, 0.57, 0.57, 0.57, 0.57, 0.56, 0.55, 0.54, 0.53, 0.51, 0.47, 0.46, 0.31, 0.2]

X1 = [-8, -7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]
B1 = [0.6, 1, 1.46, 1.83, 2.06, 2.2, 2.27, 2.39, 2.47, 2.55, 2.64, 2.68, 2.65, 2.59, 2.54, 2.51, 2.5, 2.36, 2.29, 2.21, 2.13, 1.97, 1.76, 1.7, 1.54, 1.35, 1.25, 1.16, 0.91, 0.8, 0.73, 0.57, 0.49]

X2 = [-8, -7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]
B2 = [0.67, 0.95, 1.22, 1.45, 1.71, 1.9, 2.04, 2.12, 2.18, 2.21, 2.25, 2.28, 2.3, 2.32, 2.34, 2.34, 2.34, 2.35, 2.34, 2.34, 2.33, 2.31, 2.27, 2.24, 2.19, 2.15, 2.07, 1.99, 1.81, 1.56, 1.31, 0.99, 0.72]

coils[0]["x"] = [i*1e-2 for i in X0]
coils[0]["B_meas"] = [i*1e-3 for i in B0]

coils[1]["x"] = [i*1e-2 for i in X1]
coils[1]["B_meas"] = [i*1e-3 for i in B1]

coils[2]["x"] = [i*1e-2 for i in X2]
coils[2]["B_meas"] = [i*1e-3 for i in B2]

# ➤ Loop για 3 πηνία
for coil in coils:
    N = coil["N"]
    R = coil["R"]
    x_vals = np.array(coil["x"])
    B_meas = np.array(coil["B_meas"])
    
    # Άκρα του πηνίου με το 0 στο κέντρο
    z1 = -L / 2
    z2 = L / 2

    # Θέσεις κατά μήκος του άξονα
    x = np.linspace(-0.1, 0.1, 1000)  # από -0.1m έως 0.1m

    # Υπολογισμός θεωρητικού B(x)
    B = (mu_0 * N * I) / (2 * L) * (
    (z2 - x) / np.sqrt(R**2 + (z2 - x)**2) +
    (x - z1) / np.sqrt(R**2 + (x - z1)**2)
    )

    # Σχεδίαση
    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, B_meas, 'bo', label='Μετρήσεις')
    plt.plot(x, B, 'r-', label='Θεωρητικό B(x)')
    plt.xlabel("x (m)")
    plt.ylabel("B (T)")
    plt.title(f"Κατανομή B(x) - {coil['label']}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    

# ΜΕΡΟΣ Γ - Μαγνητικό πεδίο μεταλλικών δύο παραλλήλων βρόχων (πηνία Helmholtz)

x_cm1 = [-40, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 40]        # αποστάσεις σε cm
B_mT1 = [0.05, -0.01, -0.05, 0.2, 0.36, 0.6, 0.89, 1.03, 0.87, 0.6, 0.35, 0.2, 0.11, 0.07, 0.03]  # μαγνητικό πεδίο σε mT

# --- Μετατροπή σε SI ---
x_m1 = [x / 100 for x in x_cm1]       # cm → m
B_T1= [B / 1000 for B in B_mT1]      # mT → T

# --- Σταθερές και παράμετροι ---
N = 130                            # Αριθμός σπειρών (όρισε τιμή)
R = 0.15                            # Ακτίνα κυκλικού αγωγού σε m (π.χ. 5 cm)
I = 2.0                             # Ρεύμα σε Ampere (όρισε τιμή)

# --- Θεωρητική συνάρτηση B στον άξονα κυκλικού αγωγού ---
def B_theory(x, N, R, I):
    return (mu_0_th * N * I * R**2) / (2 * (R**2 + x**2)**(3/2))

# --- Υπολογισμός θεωρητικών τιμών ---
x_vals = np.linspace(min(x_m1), max(x_m1), 500)
B_vals = B_theory(x_vals, N, R, I)

# --- Γράφημα ---
plt.figure(figsize=(8,5))
plt.plot(x_vals, B_vals, 'r-', label='Θεωρητική καμπύλη')
plt.scatter(x_m1, B_T1, color='blue', label='Μετρήσεις')
plt.xlabel('Απόσταση x (m)')
plt.ylabel('Μαγνητικό πεδίο B (T)')
plt.title('Μαγνητικό πεδίο στον άξονα κυκλικού αγωγού')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



x_cm2 = [-40, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 40]   # θέση ως προς το κέντρο των δύο πηνίων
B_mT2 = [0.09, 0.19, 0.29, 0.48, 0.73, 1.03, 1.14, 1.17, 1.15, 1, 0.73, 0.5, 0.32, 0.17, 0.06]

# --- Μετατροπή σε SI ---
x_m2 = [(x) / 100 for x in x_cm2] 
B_T2 = [B / 1000 for B in B_mT2]     # mT → T

# --- Θεωρητικό Β για πηνία Helmholtz ---
def B_helmholtz(x, N, R, I):
    term1 = 1 / ((R**2 + (x - R/2)**2)**(3/2))
    term2 = 1 / ((R**2 + (x + R/2)**2)**(3/2))
    return mu_0_th * N * I * R**2 * (term1 + term2) / 2

# --- Θεωρητική καμπύλη ---
x_vals = np.linspace(min(x_m2), max(x_m2), 500)
B_helm_vals = B_helmholtz(x_vals, N, R, I)

# --- Διάγραμμα μόνο για Helmholtz ---
plt.figure(figsize=(9,5))
plt.scatter(x_m2, B_T2, color='blue', label='Μετρήσεις')
plt.plot(x_vals, B_helm_vals, 'r-', label='Θεωρητική καμπύλη (Helmholtz)')
plt.xlabel('Απόσταση x (m)')
plt.ylabel('Μαγνητικό πεδίο B (T)')
plt.title('Μαγνητικό πεδίο στον άξονα - Πηνία Helmholtz')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()