import math
import matplotlib.pyplot as plt

def lancer_hamecon(v0, theta, x0, y0, g=9.81, vd=1):
    """
    Simule le lancer d'un hameçon et affiche la trajectoire avec Matplotlib.

    Args:
        v0: Vitesse initiale.
        theta: Angle de lancement (en degrés).
        x0: Position initiale en x.
        y0: Position initiale en y.
        g: Accélération due à la gravité.
        vd: Vitesse de descente dans l'eau.
    """

    theta_rad = math.radians(theta)  # Conversion en radians
    t = 0
    dt = 0.1  # Pas de temps

    x_values = []
    y_values = []

    while True:
        x = x0 + v0 * math.cos(theta_rad) * t
        y = y0 + v0 * math.sin(theta_rad) * t - 0.5 * g * t**2

        x_values.append(x)
        y_values.append(y)

        if y <= 0:  # L'hameçon touche l'eau
            print("L'hameçon a touché l'eau !")
            x_eau = x #on enregistre la position x au moment ou l'hamecon touche l'eau
            while y >= -10:  # La profondeur de la descente
                y = y - vd * dt
                x = x_eau # x ne change pas car la ligne tombe verticalement
                x_values.append(x)
                y_values.append(y)
            break

        t += dt

    # Visualisation avec Matplotlib
    plt.plot(x_values, y_values)
    plt.xlabel("Position en X")
    plt.ylabel("Position en Y")
    plt.title("Trajectoire de l'hameçon")
    plt.grid(True)
    plt.show()

# Exemple d'utilisation
lancer_hamecon(10, 45, 0, 5)