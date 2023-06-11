import tkinter as tk

# TODO: Deathcount missing
# TODO: UI Structure help:https://realpython.com/python-gui-tkinter/
# TODO: Dienstag?: Icons je nach Wetter oder Nachricht
# TODO: Jahr und Temperatur gleichzeitig aktuallisieren -> funktioniert net wirklich
# TODO: Code aufhübschen ฅ^•ﻌ•^ฅ
# TODO: Dienstag: UI aufhübschen ฅ^•ﻌ•^ฅ
def read_and_get_first_line(filepath):
    with open(filepath, "r+") as file:
        #Reads the first line and removes spaces and line breaks
        first_line = file.readline().strip()  
        #Reads the remaining contents of the file after the first line
        remaining_content = file.read()  
        #Sets the file pointer to the beginning of the file
        file.seek(0)  
        #Writes the remaining content back to the file
        file.write(remaining_content)  
        #Shortens the file to the current position
        file.truncate()  
    return first_line

def read_and_get_second_line(filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                second_line = lines[1]
                return second_line
            else:
                second_line = ""
                return second_line 

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

#Deletes the second line
def delete_second_line(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    with open(filepath, "w") as file:
        file.writelines(lines[:1] + lines[2:])
#For GUI, searches for keywords to assign to labels
def update_labels():
    first_line = read_and_get_first_line(filepath)
    #second_line = read_and_get_second_line(filepath)
    """ Bedinung für das gleichzeitige Auslesen von der ersten und zweiten Zeile -> funktioniert nur nicht
    if first_line.startswith("/year/") and second_line.startswith("/temperature/"):
        year = first_line.lstrip("/year/")
        year_label.config(text=f"{year}")
        temperature = second_line.lstrip("/temperature/")
        temperature = float(temperature)
        temperature_label.config(text=f"{temperature}")
        delete_second_line(filepath)
    """
    if is_file_empty(filepath):
        year_label.config(text="Game Over")
        temperature_label.config(text="")
    else:
        if first_line.startswith("/year/"):
            year = first_line.lstrip("/year/")
            year_label.config(text=f"{year}")
        elif first_line.startswith("/temperature/"):
            temperature = first_line.lstrip("/temperature/")
            temperature = float(temperature)
            temperature_label.config(text=f"{temperature:.2f} °C")  
        elif first_line.startswith("/catastrophe/"):
            catastrophe = first_line.lstrip("/catastrophe/")
            #inserting in Array, not label
            #catastrophe_label.config(text=f"{catastrophe}")
            headlines.insert(0, catastrophe)
        elif first_line.startswith("/headline/"):
            headline = first_line.lstrip("/headline/")
            #headline_label.config(text=f"{headline}")
            headlines.insert(0, headline)
        else:
            first_line = ""
        delete_first_line(filepath)

        headlines_to_display = headlines[:15]
        headlines_text = "\n".join(headlines_to_display)
        headline_list_label.config(text=headlines_text)
    #updatet Labels
    window.after(500, update_labels)

filepath = 'news.txt'

window = tk.Tk()

#Label for all textfile variables
year_label = tk.Label(window, text="2025", bg="white", font=("Arial", 18))
year_label.pack(fill=tk.X)

temperature_label = tk.Label(window, text="1.00 °C", bg="white", font=("Arial", 12))
temperature_label.pack(fill=tk.Y, side=tk.RIGHT)

deathcount_label = tk.Label(window, text="Deathcount", bg="white", font=("Arial", 12))
deathcount_label.pack(fill=tk.X)

#Label for the list of headlines
headline_list_label = tk.Label(window, bg="white", font=("Arial", 12))
headline_list_label.pack(fill=tk.X)
#Initialize the headlines array
headlines = []

update_labels()
window.mainloop()