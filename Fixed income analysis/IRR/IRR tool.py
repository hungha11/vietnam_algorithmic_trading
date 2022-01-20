import tkinter as tk
import numpy as np

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 600, height = 300)
canvas1.pack()

label0 = tk.Label(root, text='Calculate IRR')
label0.config(font=('helvetica', 14))
canvas1.create_window(300, 40, window=label0)

entry1 = tk.Entry (root, width = 40)
canvas1.create_window(450, 100, window=entry1)

entry2 = tk.Entry (root, width = 40)
canvas1.create_window(450, 140, window=entry2)

entry3 = tk.Entry (root, width = 30)
canvas1.create_window(300, 250, window=entry3)

label1 = tk.Label(root, text=' Initial Investment (Absolute Value):')
label1.config(font=('helvetica', 10))
canvas1.create_window(130, 100, window=label1)

label2 = tk.Label(root, text='Cash Flow Each Year (Separated by Commas):')
label2.config(font=('helvetica', 10))
canvas1.create_window(168, 140, window=label2)

def calcIRR ():
    cf0 = entry1.get()
    cf0 = -1*float(cf0)
    cashflows = entry2.get().split(',') #Enter values Separated by Commas

    cf0_and_cashflows = [cf0] + cashflows
    irr = np.irr(cf0_and_cashflows)

    label3 = tk.Label(root, text= irr*100,font=('helvetica', 10, 'bold'),bg='white')
    canvas1.create_window(300, 250, window=label3)

button1 = tk.Button(text='Calculate IRR', command=calcIRR, bg='green', fg='white', font=('helvetica', 9, 'bold'), width = 25)
canvas1.create_window(300, 200, window=button1)

root.mainloop()