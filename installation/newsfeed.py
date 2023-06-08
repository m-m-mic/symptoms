import tkinter as tk

# TODO: Deathcount missing
# TODO: UI Structure help:https://realpython.com/python-gui-tkinter/
# TODO: Visibility of more Headlines
# TODO: More Headlines visible

def lese_und_loesche_first_line(filepath):
    with open(filepath, 'r+') as file:
        # Reads the first line and removes spaces and line breaks
        first_line = file.readline().strip()  
        # Reads the remaining contents of the file after the first line
        remaining_content = file.read()  
        # Sets the file pointer to the beginning of the file
        file.seek(0)  
        # Writes the remaining content back to the file
        file.write(remaining_content)  
        # Shortens the file to the current position
        file.truncate()  
    return first_line

#Checks if the text file is empty
def is_file_empty(filepath):
    with open(filepath, "r") as file:
        content = file.read()
        return not content.strip()

#Deletes the first line
def delete_first_line(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        file.writelines(lines[0:])

#For GUI, searches for keywords to assign to labels
def update_year_label():
    first_line = lese_und_loesche_first_line(filepath)

    if first_line.startswith("/year/"):
        year = first_line.lstrip("/year/")
        year_label.config(text=f"{year}")
    elif first_line.startswith("/temperature/"):
        temperature = first_line.lstrip("/temperature/")
        temperature = float(temperature)
        temperature_label.config(text=f"{temperature:.2f} °C")
    elif first_line.startswith("/catastrophe/"):
        catastrophe = first_line.lstrip("/catastrophe/")
        catastrophe_label.config(text=f"{catastrophe}")
    elif first_line.startswith("/headline/"):
        headline = first_line.lstrip("/headline/")
        headline_label.config(text=f"{headline}")
    else:
        first_line = ""
    delete_first_line(filepath)
    if not is_file_empty(filepath):
        window.after(1000, update_year_label)

filepath = 'news.txt'

window = tk.Tk()

#Labels für Jahr
year_label = tk.Label(window, text="Jahr", bg="white", font=("Arial", 18))
year_label.pack(fill=tk.X)
#Labels für Temperaturanstieg
temperature_label = tk.Label(window, text="°C", bg="white", font=("Arial", 12))
temperature_label.pack(fill=tk.Y, side=tk.RIGHT)
#Labels für Katastrophe
catastrophe_label = tk.Label(window, text="Katastrophe", bg="white", font=("Arial", 12))
catastrophe_label.pack(fill=tk.X)
#Labels für Katastrophe
headline_label = tk.Label(window, text="Headline", bg="white", font=("Arial", 12))
headline_label.pack(fill=tk.X)

update_year_label()
window.mainloop()