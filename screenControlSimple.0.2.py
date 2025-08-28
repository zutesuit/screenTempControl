import tkinter as tk
import subprocess

# Define your temperature presets
presets = {
    "Much Cooler": "10000",
    "Cooler": "8000",
    "Neutral": "5500",
    "Warmer": "4500",
    "Much Warmer": "3500",
}

def set_temp(temp):
    
    temp_limits = (1000, 15000)
    if temp == "5500":
        subprocess.run(["gammastep", "-x"], check=True)
        slider.set(50)  # Reset slider to middle
    elif int(temp) < temp_limits[0] or int(temp) > temp_limits[1]:
        print(f"Temperature {temp} out of range {temp_limits}")
    else:
        try:
            subprocess.run(["gammastep", "-O", temp], check=True)
            temp_int = int(temp)
            slider_val = int(20 + (temp_int - 1000) * (80 - 20) / (15000 - 3500))
            slider.set(slider_val)
        except subprocess.CalledProcessError:
            print(f"Failed to set temperature {temp_limits}")

def slider_to_temp(val):
    temp_limits = (3500, 10000)
    val = int(val)
    # Linear mapping from slider value to temperature
    temp = int(3500 + (val - 20) * (10000 - 3500) / (80 - 20))
    if temp < temp_limits[0] or temp > temp_limits[1]:
        print(f"Temperature {temp} out of range {temp_limits}")
    else:
        set_temp(str(temp))

root = tk.Tk()
root.title("GammaStep Temperature Control")


for label, temp in presets.items():
    btn = tk.Button(root, text=label, command=lambda t=temp: set_temp(t), width=25)
    btn.pack(padx=15, pady=5)
    
slider = tk.Scale(root, from_=20, to=80, orient=tk.HORIZONTAL, command=slider_to_temp, length=300)
slider.pack(padx=20, pady=20)
slider.set(50)  # Set default value to 50
    


root.mainloop()
