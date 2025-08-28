import tkinter as tk
import subprocess

MIN_TEMP = 3500
MAX_TEMP = 15000
NEUTRAL_TEMP = 5500
SLIDER_MIN = 20
SLIDER_MAX = 80
# Define your temperature presets
presets = {
    "Much Cooler": "10000",
    "Cooler": "8000",
    "Neutral": "5500",
    "Warmer": "4500",
    "Much Warmer": "3500",
}


updating_slider = False

def set_temp(temp):
    global updating_slider
    
    if temp == "5500":
        updating_slider = True
        subprocess.run(["gammastep", "-x"], check=True)
        #subprocess.run(["gammastep", "-x"], check=True)
        
        try: 
            slider.set(50)  # Reset slider to middle
        finally:
            updating_slider = False
        return
    
    
    else:
        try:
            subprocess.run(["gammastep", "-O", temp], check=True)
        
            updating_slider = True
            #slider_value =
            #map_temp_to_slider(int(temp))
            try:
                slider.set(map_temp_to_slider(int(temp)))
            finally:
                updating_slider = False
        except subprocess.CalledProcessError:
            print(f"Failed to set temperature ")
    
    """  else:
        t = clamp(int(temp), MIN_TEMP, MAX_TEMP)
        subprocess.run(["gammastep", "-O", str(t)], check=True)
        # then guarded slider.set(map_temp_to_slider(t)) """
  

def slider_to_temp(val):
    
    if updating_slider:
        return
    val = int(val)
    # Linear mapping from slider value to temperature
    temp = map_slider_to_temp(float(val))
    set_temp(str(int(round(temp))))

def map_temp_to_slider(t):
    t = clamp(t, MIN_TEMP, MAX_TEMP)
    return SLIDER_MIN + (t - MIN_TEMP) * (SLIDER_MAX - SLIDER_MIN) / (MAX_TEMP - MIN_TEMP)

def map_slider_to_temp(v):
    v = clamp(v, SLIDER_MIN, SLIDER_MAX)
    return MIN_TEMP + (v - SLIDER_MIN) * (MAX_TEMP - MIN_TEMP) / (SLIDER_MAX - SLIDER_MIN)

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

root = tk.Tk()
root.title("GammaStep Temperature Control")


for label, temp in presets.items():
    btn = tk.Button(root, text=label, command=lambda t=temp: set_temp(t), width=25)
    btn.pack(padx=15, pady=5)
    
slider = tk.Scale(root, from_=20, to=80, orient=tk.HORIZONTAL, command=slider_to_temp, length=300)
slider.pack(padx=20, pady=20)
slider.set(50)  # Set default value to 50
    


root.mainloop()
