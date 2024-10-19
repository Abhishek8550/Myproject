from tkinter import *
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk, UnidentifiedImageError  
import os
from stegano import lsb  

root = Tk()
root.title("Steganography - Hide a Secret Text Message in an Image")
root.geometry("700x500+150+180")
root.resizable(False, False)
root.configure(bg="#25cf85")

try:
    icon_image = Image.open(r"C:\Users\user\OneDrive\Documents\Steganography folder\qwe2.png")
    icon_image = ImageTk.PhotoImage(icon_image)  
    root.iconphoto(False, icon_image)
except Exception as e:
    print(f"Error loading icon: {e}")

header_frame = Frame(root, bg="#25cf85")
header_frame.pack(pady=10)  

try:
    logo_image = Image.open(r"C:\Users\user\OneDrive\Documents\Steganography folder\logo.png")
    logo_image = ImageTk.PhotoImage(logo_image) 

    image_label = Label(header_frame, image=logo_image,width=75, height=65)
    image_label.pack(side="left", padx=0, pady=0) 
    image_label.image = logo_image
except Exception as e:
    print(f"Error loading logo: {e}")

title_label = Label(header_frame, text="ABHISHEK STEGANOGRAPHY", bg="#25cf85", fg="purple", font="Audiowide 30 bold")
title_label.pack(side="left")  

f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)

lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

frame2 = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
frame2.place(x=350, y=80)

text1 = Text(frame2, font="Calibri 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

frame3 = Frame(root, bd=3, bg="#25cf85", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

Button(frame3, text="Open Image", width=10, height=2, font="Calibri 14 bold", command=lambda: showimage()).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="Calibri 14 bold", command=lambda: save()).place(x=180, y=30)
Label(frame3, text="For save & open Picture & Image File", bg="#25cf85", fg="purple").place(x=20, y=5)

frame4 = Frame(root, bd=3, bg="#25cf85", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

Button(frame4, text="Hide Data", width=10, height=2, font="Calibri 14 bold", command=lambda: Hide()).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="Calibri 14 bold", command=lambda: Show()).place(x=180, y=30)
Label(frame4, text="For Hide and Show Text", bg="#25cf85", fg="purple").place(x=20, y=5)

filename = None
secret = None

def showimage():
    global filename
    filename = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title='Select Image File',
        filetypes=(("PNG file", "*.png"), ("JPG File", "*.jpg"), ("All files", "*.*"))
    )
    if filename:
        try:
            img = Image.open(filename)
            img = ImageTk.PhotoImage(img)
            lbl.configure(image=img, width=250, height=250)
            lbl.image = img  
        except (UnidentifiedImageError, FileNotFoundError) as e:
            messagebox.showerror("Error", f"Unable to open image: {e}")


def Hide():
    global secret
    if filename:
        message = text1.get(1.0, END).strip()
        if message:
            try:
                secret = lsb.hide(filename, message)
                messagebox.showinfo("Success", "Message hidden successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to hide message: {e}")
        else:
            messagebox.showwarning("Warning", "Enter a message to hide.")
    else:
        messagebox.showwarning("Warning", "Please select an image first.")


def Show():
    if filename:
        try:
            clear_message = lsb.reveal(filename)
            if clear_message:
                text1.delete(1.0, END)
                text1.insert(END, clear_message)
            else:
                messagebox.showinfo("Info", "No hidden message found in the image.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reveal message: {e}")
    else:
        messagebox.showwarning("Warning", "Please select an image first.")


def save():
    if secret:
        try:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                secret.save(save_path)
                messagebox.showinfo("Success", f"Image saved at {save_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")
    else:
        messagebox.showwarning("Warning", "No secret message to save.")


root.mainloop()