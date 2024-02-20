import tkinter as tk
from tkinter import messagebox
import requests

CHAOS_IN_DIVINE = 0


def print_http_status(code):
    """
    Prints the meaning of the given HTTP status code.
    :param code: The HTTP status code.
    """
    status_codes = {
        200: "Server connected",
        301: "Server redirecting to a different endpoint.",
        400: "Bad request: incorrect data sent.",
        401: "Not authenticated: missing or incorrect credentials.",
        403: "Forbidden: insufficient permissions.",
        404: "Resource not found on the server.",
        503: "Server not ready to handle the request."
    }

    if code in status_codes:
        return status_codes[code]
    else:
        return "Unknown status code: " + str(code)


def calc(chaos_price):
    """
    returns the chaos_price in terms of divine and chaos
    :param chaos_price: total value of transaction in chaos
    :return: how many divs and chaos
    """
    number_of_divines = chaos_price // CHAOS_IN_DIVINE
    chaos_leftover = int(chaos_price) - (number_of_divines * CHAOS_IN_DIVINE)
    return f"{round(number_of_divines)} divines, {round(chaos_leftover)} chaos"


def update_divine_value():
    global CHAOS_IN_DIVINE
    response = requests.get("https://poe.ninja/api/data/currencyoverview?league=Affliction&type=Currency")
    http_status = print_http_status(response.status_code)
    if response.status_code == 200:
        data = response.json()
        for line in data["lines"]:
            if line["currencyTypeName"] == "Divine Orb":
                CHAOS_IN_DIVINE = line["chaosEquivalent"]
                divine_value_label.config(text=f"1 Divine Orb is worth: {CHAOS_IN_DIVINE} Chaos Orbs.")
        if CHAOS_IN_DIVINE == 0:
            messagebox.showerror("Error", "Divine Orb data not found.")
    else:
        messagebox.showerror("Error", http_status)


def calculate_conversion(event=None):
    try:
        chaos_price = int(chaos_price_entry.get())
        result = calc(chaos_price)
        result_label.config(text=result)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for Chaos Price.")


# GUI setup
root = tk.Tk()
root.title("PoE Currency Converter")

divine_value_label = tk.Label(root, text="")
divine_value_label.pack()

update_divine_button = tk.Button(root, text="Update Divine Value", command=update_divine_value)
update_divine_button.pack()

chaos_price_label = tk.Label(root, text="Total chaos to convert:")
chaos_price_label.pack()

chaos_price_entry = tk.Entry(root)
chaos_price_entry.pack()
chaos_price_entry.bind('<Return>', calculate_conversion)

calculate_button = tk.Button(root, text="Calculate", command=calculate_conversion)
calculate_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

update_divine_value()

root.mainloop()
