#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This is a simple application to take a given set of at least two stock tickers
    and 1) chart the tickers' percentage performance over the past 5 years and 
    2) use the same 5-year period and set of tickers to perform a Monte Carlo
    simulation (6000 random weight trials) to find the optimal weight for the ticker 
    portfolio.  Once the simulation has completed and generated a binary pickle file 
    as output, the results can be a-charted, b-top 10 viewed as a table, c-export
    the results to an Excel file.

    The application uses the tkinter GUI, Python's implementation of the Tcl/Tk interface
"""

import mc_lib
import tkinter as tk
from tkinter import ttk
from pandastable import Table

root = tk.Tk()
root.title("Monte Carlo Simulation")

# window size
window_width = 600
window_height = 500

# get overall screen size and center window initially
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# window size and initial position
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# tk.Label(root, text='Classic Label').pack()
label = ttk.Label(
    root,
    text="Pick a minimum of 2 and a maximum of 10 securities \n sequentially down each entry box",
    font=("Helvetica", 12),
)
label.pack(ipadx=10, ipady=10)

# put tickers into a list to pass to functions
def get_input():
    sec_list = []
    val0 = security0.get("1.0", "end-1c")
    val1 = security1.get("1.0", "end-1c")
    val2 = security2.get("1.0", "end-1c")
    val3 = security3.get("1.0", "end-1c")
    val4 = security4.get("1.0", "end-1c")
    val5 = security5.get("1.0", "end-1c")
    val6 = security6.get("1.0", "end-1c")
    val7 = security7.get("1.0", "end-1c")
    val8 = security8.get("1.0", "end-1c")
    val9 = security9.get("1.0", "end-1c")
    sec_list.append(val0)
    sec_list.append(val1)
    sec_list.append(val2)
    sec_list.append(val3)
    sec_list.append(val4)
    sec_list.append(val5)
    sec_list.append(val6)
    sec_list.append(val7)
    sec_list.append(val8)
    sec_list.append(val9)
    return sec_list


# chart of stocks' performance
def perf_chrt():
    sec_list = get_input()
    # print(sec_list)

    if sec_list[0] == "":
        tk.messagebox.showerror(
            title="Missing Data", message="Security 1 must contain a ticker"
        )
    else:
        # run mc sim passing sec_list values
        mc_lib.chart_perf(sec_list)


# run monte carlo simulation for tickers
def mc_sim():
    sec_list = get_input()
    # print(sec_list)

    if (sec_list[0] == "") or (sec_list[1] == ""):
        tk.messagebox.showerror(
            title="Missing Data", message="Security 1 and 2 must contain tickers"
        )
    else:
        # run mc sim passing sec_list values
        mc_lib.mc_hammer(sec_list)
        # print(sec_list)


# view monte carlo sim results chart
def mc_view():
    mc_lib.view_mc()


# view top 10 weights in window
def tbl_view():
    frame = tk.Toplevel(root)
    table = Table(
        frame, dataframe=mc_lib.view_tbl(), showtoolbar=True, showstatusbar=True
    )
    table.show()


# Creating text box widgets and labels
security0 = tk.Text(root, height=1, width=7)
security0.place(x=90, y=80)
sec0 = tk.Label(root, text="Security1: ")
sec0.place(x=10, y=80)

security1 = tk.Text(root, height=1, width=7)
security1.place(x=90, y=100)
sec1 = tk.Label(root, text="Security2: ")
sec1.place(x=10, y=100)

security2 = tk.Text(root, height=1, width=7)
security2.place(x=90, y=120)
sec2 = tk.Label(root, text="Security3: ")
sec2.place(x=10, y=120)

security3 = tk.Text(root, height=1, width=7)
security3.place(x=90, y=140)
sec3 = tk.Label(root, text="Security4: ")
sec3.place(x=10, y=140)

security4 = tk.Text(root, height=1, width=7)
security4.place(x=90, y=160)
sec4 = tk.Label(root, text="Security5: ")
sec4.place(x=10, y=160)

security5 = tk.Text(root, height=1, width=7)
security5.place(x=90, y=180)
sec5 = tk.Label(root, text="Security6: ")
sec5.place(x=10, y=180)

security6 = tk.Text(root, height=1, width=7)
security6.place(x=90, y=200)
sec6 = tk.Label(root, text="Security7: ")
sec6.place(x=10, y=200)

security7 = tk.Text(root, height=1, width=7)
security7.place(x=90, y=220)
sec7 = tk.Label(root, text="Security8: ")
sec7.place(x=10, y=220)

security8 = tk.Text(root, height=1, width=7)
security8.place(x=90, y=240)
sec8 = tk.Label(root, text="Security9: ")
sec8.place(x=10, y=240)

security9 = tk.Text(root, height=1, width=7)
security9.place(x=90, y=260)
sec9 = tk.Label(root, text="Security10:")
sec9.place(x=10, y=260)

# Button to view stocks' performance
btn_perf = tk.Button(
    root,
    height=3,
    width=18,
    text="Chart of Performance",
    command=lambda: perf_chrt(),
)
btn_perf.place(x=200, y=160)

# Button to run Monte Carlo Simulation
btn_run = tk.Button(
    root, height=3, width=18, text="Run Simulation", command=lambda: mc_sim()
)
btn_run.place(x=400, y=160)

# Button to display Monte Carlo sim results
btn_view = tk.Button(
    root, height=1, width=18, text="View MC Results", command=lambda: mc_view()
)
btn_view.place(x=400, y=220)

# Button to view top 10 weights in popup window
btn_table = tk.Button(
    root,
    height=1,
    width=18,
    text="View Top 10 Weights",
    command=lambda: tbl_view(),
)
btn_table.place(x=400, y=245)

# Button to export top 10 weights to Excel
btn_excel = tk.Button(
    root,
    height=1,
    width=18,
    text="Excel Export Results",
    command=lambda: mc_lib.xls_export(),
)
btn_excel.place(x=400, y=270)

# launch window
root.mainloop()
