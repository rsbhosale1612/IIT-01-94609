import tkinter as tk
from tkinter import ttk, scrolledtext
from .api_client import get_current_weather, get_forecast, WeatherAPIError
from .formatter import format_current, format_simple_forecast

def start_gui():
    root = tk.Tk()
    root.title("Weather App")
    root.geometry("600x400")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    label = ttk.Label(frame, text="City:")
    label.grid(row=0, column=0, sticky="w")
    city_var = tk.StringVar()
    entry = ttk.Entry(frame, textvariable=city_var)
    entry.grid(row=0, column=1, sticky="ew")
    frame.columnconfigure(1, weight=1)

    output = scrolledtext.ScrolledText(frame, height=18)
    output.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def on_get():
        city = city_var.get().strip()
        if not city:
            return
        output.delete("1.0", tk.END)
        try:
            current = get_current_weather(city)
            out = format_current(current) + "\n\n"
            forecast = get_forecast(city)
            out += format_simple_forecast(forecast, entries=5)
            output.insert(tk.END, out)
        except WeatherAPIError as e:
            output.insert(tk.END, f"Error: {e}")

    btn = ttk.Button(frame, text="Get Weather", command=on_get)
    btn.grid(row=0, column=2, padx=6)

    root.mainloop()
