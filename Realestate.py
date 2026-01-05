import tkinter as tk
from tkinter import ttk, messagebox

#Default Rates
RATES = {
    "Residential": {"Chennai": 3500, "Delhi": 2000, "Hosur": 2200, "banglore": 5000, "Mumbai": 7500, "Uttarpradesh": 3000, "Remote": 500},
    "Commercial":  {"Chennai": 6000, "Delhi": 3500, "Hosur": 3700, "banglore": 6500, "Mumbai": 8500, "Uttarpradesh": 2500, "Remote": 1500},
    "Agriculture": {"Chennai": 800,  "Delhi": 600,  "Hosur": 650,  "banglore": 4000, "Mumbai": 5500, "Uttarpradesh": 2000, "Remote": 500},
    "Industrial":  {"Chennai": 2500, "Delhi": 1400, "Hosur": 1600, "banglore": 4500, "Mumbai": 6500, "Uttarpradesh": 2800, "Remote": 1200}, 
    "Recreational": {"Chennai": 1000, "Delhi": 1200, "Hosur": 1200, "banglore": 4000, "Mumbai": 7500, "Uttarpradesh": 3500, "Remote": 500},
    "Transportation": {"Chennai": 2000, "Delhi": 3000, "Hosur": 1200, "banglore": 6000, "Mumbai": 9500, "uttarpradesh":4000, "Remote": 600},
    "Institutional":{"Chennai": 2500, "Delhi": 2500, "Hosur": 1600, "banglore": 6500, "Mumbai": 8500, "uttarpradesh": 5000, "Remote": 800}
}


#GUI Class
class LandCalculatorApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Land Amount Calculator")
        self.window.geometry("500x550")
        self.window.resizable(False, False)

        title = tk.Label(window, text="Land Amount Calculator",
                         font=("Arial", 18, "bold"))
        title.pack(pady=15)

        frame = tk.Frame(window)
        frame.pack(pady=10)

        # Land Type
        tk.Label(frame, text="Select Land Type:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.land_type = ttk.Combobox(frame, values=list(RATES.keys()), state="readonly", width=20)
        self.land_type.grid(row=0, column=1, pady=5)
        self.land_type.bind("<<ComboboxSelected>>", self.update_locations)

        # Location
        tk.Label(frame, text="Select Location:", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        self.location = ttk.Combobox(frame, values=[], state="readonly", width=20)
        self.location.grid(row=1, column=1, pady=5)

        # Square Feet
        tk.Label(frame, text="Enter Square Feet:", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        self.sqft_entry = tk.Entry(frame, width=22)
        self.sqft_entry.grid(row=2, column=1, pady=5)

        # GST
        tk.Label(frame, text="GST % (0-18):", font=("Arial", 12)).grid(row=3, column=0, sticky="w")
        self.gst_entry = tk.Entry(frame, width=22)
        self.gst_entry.insert(0, "0")
        self.gst_entry.grid(row=3, column=1, pady=5)

        # Discount
        tk.Label(frame, text="Discount %:", font=("Arial", 12)).grid(row=4, column=0, sticky="w")
        self.discount_entry = tk.Entry(frame, width=22)
        self.discount_entry.insert(0, "0")
        self.discount_entry.grid(row=4, column=1, pady=5)

        # Calculate Button
        calc_btn = tk.Button(window, text="Calculate Amount",
                             command=self.calculate_amount,
                             font=("Arial", 13, "bold"), bg="#4CAF50", fg="white", width=20)
        calc_btn.pack(pady=10)

        # Result Box
        self.result_box = tk.Text(window, width=55, height=15, font=("Arial", 11))
        self.result_box.pack(pady=10)

    # Update location dropdown when land type changes
    def update_locations(self, event):
        land = self.land_type.get()
        locations = list(RATES[land].keys())
        self.location["values"] = locations
        if "Chennai" in locations:
            self.location.set("Chennai")
        else:
            self.location.set(locations[0])

    # Calculation Logic
    def calculate_amount(self):
        try:
            land = self.land_type.get()
            loc = self.location.get()
            sqft = float(self.sqft_entry.get())
            gst = float(self.gst_entry.get())
            discount = float(self.discount_entry.get())

            if sqft <= 0:
                messagebox.showerror("Error", "Square feet must be greater than 0.")
                return

            rate = RATES[land].get(loc, RATES[land]["Remote"])
            base_amount = sqft * rate

            # Discount
            discounted = base_amount - (base_amount * discount / 100)

            # GST
            final_amount = discounted + (discounted * gst / 100)

            # Display Output
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, f"Land Type: {land}\n")
            self.result_box.insert(tk.END, f"Location: {loc}\n")
            self.result_box.insert(tk.END, f"Rate per sqft: ₹{rate}\n")
            self.result_box.insert(tk.END, f"Area (sqft): {sqft}\n")
            self.result_box.insert(tk.END, f"\nBase Amount: ₹{base_amount:,.2f}\n")
            self.result_box.insert(tk.END, f"After Discount ({discount}%): ₹{discounted:,.2f}\n")
            self.result_box.insert(tk.END, f"After GST ({gst}%): ₹{final_amount:,.2f}\n")
            self.result_box.insert(tk.END, "\nFinal Amount Payable:\n")
            self.result_box.insert(tk.END, f"₹{final_amount:,.2f}")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")


#Run the App
window = tk.Tk()
app = LandCalculatorApp(window)
window.mainloop()

