import tkinter
from tkinter import PhotoImage, END
from cryptography.fernet import Fernet
from tkinter import messagebox
from tkinter import filedialog
import base64


def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def save_and_encrypt_notes():
    title = title_entry.get()
    message = secret_text.get("1.0", END)
    master_secret = key_entry.get()

    if len(title) == 0 or len(message) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="Error", message="Please enter all info.")
    else:
        #encryption
        message_encrypted = encode(master_secret, message)
        try:
            with open("mysecret.txt", "a") as data_file:
                data_file.write(f"\n{title}\n{message_encrypted}")
        except FileNotFoundError:
            with open("mysecret.txt", "w") as data_file:
                data_file.write(f"\n{title}\n{message_encrypted}")
        finally:
            title_entry.delete(0, END)
            secret_text.delete("1.0", END)
            key_entry.delete(0, END)

def decrypt_notes():
    message_encrypted = secret_text.get("1.0", END)
    master_secret = key_entry.get()

    if len(message_encrypted) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="Error!", message="Please enter all info.")
    else:
        try:
            decrypted_message = decode(master_secret, message_encrypted)
            secret_text.delete("1.0", END)
            secret_text.insert("1.0", decrypted_message)
        except:
            messagebox.showinfo(title="Error!", message="Please Enter Encrypted text!")


#UI
window = tkinter.Tk()
window.title("Secret Notes - Encrypter / Decrypter")

photo = PhotoImage(file = "icon.png")
photo_label = tkinter.Label(image=photo)
photo_label.pack()


title_label = tkinter.Label(text="Enter Your Title:", pady=10,font=("Arial", 10, "bold"), fg="dark red")
title_label.pack()

title_entry = tkinter.Entry(width=30)
title_entry.pack()

secret_label = tkinter.Label(text="Enter Your Secret:", pady=10,font=("Arial", 10, "bold"), fg="dark red")
secret_label.pack()

secret_text = tkinter.Text(width=40, height=15)
secret_text.pack()

key_label = tkinter.Label(text="Enter Master Key:", pady=10,font=("Arial", 10, "bold"), fg="dark red")
key_label.pack()

key_entry = tkinter.Entry(width=30)
key_entry.pack()

title_label_exept = tkinter.Label(text="")
title_label_exept.pack()

save_button = tkinter.Button(text="Save & Encrypt", pady=7, padx=10, background="light blue", fg="dark red", command=save_and_encrypt_notes)
save_button.pack()

decrypt_button = tkinter.Button(text="Decrypt", pady=7, padx=10, background="light blue", fg="dark red", command=decrypt_notes)
decrypt_button.pack()


title_label_exept = tkinter.Label(text="", pady=7)
title_label_exept.pack()





window.mainloop()