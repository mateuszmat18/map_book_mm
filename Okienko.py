import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkintermapview
import requests


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry('250x250')
        self.root.title('Okno logowania')

        self.frame_start = Frame(self.root)
        self.frame_start.grid(row=0, column=0, padx=10, pady=10)

        self.label_start = Label(self.frame_start, text='Logowanie')
        self.entry_password = Entry(self.frame_start, show='*')
        self.button_password = Button(self.frame_start, text='Sprawdź hasło', command=self.check_password)

        self.label_start.grid(row=0, column=0, columnspan=4)
        self.entry_password.grid(row=1, column=0, columnspan=2)
        self.button_password.grid(row=2, column=0, columnspan=2)

    def check_password(self):
        password = self.entry_password.get()
        if password == 'kot':
            self.open_park_manager()
        else:
            messagebox.showerror('Nieprawidłowe hasło', 'Podane hasło jest nieprawidłowe.')

    def open_park_manager(self):
        self.root.withdraw()
        park_manager_window = Toplevel(self.root)
        map_widget = tkintermapview.TkinterMapView(park_manager_window, width=700, height=400)
        park_manager = ParkManager(park_manager_window, map_widget)

    def start(self):
        self.root.mainloop()

class ParkManager:
    def __init__(self, root, map_widget):
        self.root = root
        self.root.geometry('800x700')
        self.root.title('Park Manager')

        self.parks = []
        self.map_widget = map_widget
        self.markers = {}

        self.frame_list = Frame(root)
        self.frame_details = Frame(root)
        self.frame_map = Frame(root)

        self.frame_list.grid(row=0, column=0, padx=10, pady=10)
        self.frame_details.grid(row=0, column=1, padx=10, pady=10)
        self.frame_map.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.setup_list_frame()
        self.setup_details_frame()
        self.setup_map_frame()
        self.selected_marker = None
        self.selected_park = None

    def setup_list_frame(self):
        self.label_list = Label(self.frame_list, text='Lista Parków:')
        self.listbox_parks = Listbox(self.frame_list, width=30)
        self.button_show_details = Button(self.frame_list, text='Pokaż szczegóły', command=self.show_park_details)
        self.button_add_park = Button(self.frame_list, text='Dodaj Park', command=self.add_park)
        self.button_remove_park = Button(self.frame_list, text='Usuń Park', command=self.remove_park)
        self.button_update_park = Button(self.frame_list, text='Edytuj Park', command=self.update_park)

        self.label_list.grid(row=0, column=0)
        self.listbox_parks.grid(row=1, column=0, columnspan=3)
        self.button_show_details.grid(row=2, column=0)
        self.button_add_park.grid(row=2, column=1)
        self.button_remove_park.grid(row=2, column=2)
        self.button_update_park.grid(row=3, column=0, columnspan=3)

        self.refresh_park_list()

    def setup_details_frame(self):
        self.label_details = Label(self.frame_details, text='Szczegóły Parku')
        self.label_name = Label(self.frame_details, text='Nazwa Parku:')
        self.entry_name = Entry(self.frame_details, width=30)
        self.label_guests = Label(self.frame_details, text='Goście:')
        self.listbox_guests = Listbox(self.frame_details, width=35)
        self.label_workers = Label(self.frame_details, text='Pracownicy:')
        self.listbox_workers = Listbox(self.frame_details, width=35)

        self.entry_guest_name = Entry(self.frame_details)
        self.entry_worker_name = Entry(self.frame_details)
        self.entry_guest_vehicle = Entry(self.frame_details)
        self.entry_worker_location = Entry(self.frame_details)
        self.entry_guest_location = Entry(self.frame_details)

        self.button_add_guest = Button(self.frame_details, text='Dodaj Gościa', command=self.add_guest)
        self.button_remove_guest = Button(self.frame_details, text='Usuń Gościa', command=self.remove_guest)
        self.button_update_guest = Button(self.frame_details, text='Edytuj Gościa', command=self.update_guest)
        self.button_update_vehicle = Button(self.frame_details, text='Edytuj Pojazd', command=self.update_vehicle)
        self.button_remove_vehicle = Button(self.frame_details, text='Usuń Pojazd', command=self.remove_vehicle)
        self.button_add_worker = Button(self.frame_details, text='Dodaj Pracownika', command=self.add_worker)
        self.button_remove_worker = Button(self.frame_details, text='Usuń Pracownika', command=self.remove_worker)
        self.button_update_worker = Button(self.frame_details, text='Edytuj Pracownika', command=self.update_worker)
        self.button_add_guest_location = Button(self.frame_details, text='Dodaj Lokację Gościa', command=self.add_guest_location)
        self.button_remove_guest_location = Button(self.frame_details, text='Usuń Lokację Gościa', command=self.remove_guest_location)
        self.button_add_worker_location = Button(self.frame_details, text='Dodaj Lokację Pracownika', command=self.add_worker_location)
        self.button_remove_worker_location = Button(self.frame_details, text='Usuń Lokację Pracownika', command=self.remove_worker_location)

        self.label_details.grid(row=0, column=0, columnspan=4)
        self.label_name.grid(row=1, column=0, sticky=W)
        self.entry_name.grid(row=1, column=1, sticky=W, columnspan=3)
        self.label_guests.grid(row=2, column=0, columnspan=2)
        self.label_workers.grid(row=2, column=2, columnspan=2)
        self.listbox_guests.grid(row=3, column=0, columnspan=2)
        self.listbox_workers.grid(row=3, column=2, columnspan=2)

        self.entry_guest_name.grid(row=4, column=0, columnspan=2)
        self.entry_worker_name.grid(row=4, column=2, columnspan=2)
        self.entry_guest_vehicle.grid(row=5, column=0, columnspan=2)
        self.entry_worker_location.grid(row=5, column=2, columnspan=2)
        self.entry_guest_location.grid(row=6, column=0, columnspan=2)

        self.button_add_guest.grid(row=7, column=0)
        self.button_remove_guest.grid(row=7, column=1)
        self.button_update_guest.grid(row=8, column=0, columnspan=2)
        self.button_update_vehicle.grid(row=9, column=0)
        self.button_remove_vehicle.grid(row=9, column=1)
        self.button_add_worker.grid(row=7, column=2)
        self.button_remove_worker.grid(row=7, column=3)
        self.button_update_worker.grid(row=8, column=2, columnspan=2)
        self.button_add_guest_location.grid(row=10, column=0)
        self.button_remove_guest_location.grid(row=10, column=1)
        self.button_add_worker_location.grid(row=9, column=2)
        self.button_remove_worker_location.grid(row=9, column=3)

    def setup_map_frame(self):
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=770, height=400)
        self.map_widget.grid(row=0, column=0, columnspan=8)
        self.map_widget.set_position(50.21, 21.0)
        self.map_widget.set_zoom(5)

    def refresh_park_list(self):
        self.listbox_parks.delete(0, END)
        for park in self.parks:
            self.listbox_parks.insert(END, park['name'])

    def show_park_details(self):
        selected_index = self.listbox_parks.curselection()
        if selected_index:
            self.selected_park = self.parks[selected_index[0]]
            self.entry_name.delete(0, END)
            self.entry_name.insert(0, self.selected_park['name'])
            self.refresh_guest_list()
            self.refresh_worker_list()
            self.update_map_marker()

    def refresh_guest_list(self):
        self.listbox_guests.delete(0, END)
        if self.selected_park:
            for guest in self.selected_park['guests']:
                vehicles = ", ".join(guest['vehicles']) if 'vehicles' in guest else "-"
                location = ", ".join(guest['location']) if 'location' in guest else "-"
                self.listbox_guests.insert(END, f"{guest['name']} - Pojazdy: {vehicles} - Lokacja: {location}")

    def refresh_worker_list(self):
        self.listbox_workers.delete(0, END)
        if self.selected_park:
            for worker in self.selected_park['workers']:
                location = ", ".join(worker['location']) if 'location' in worker else "-"
                self.listbox_workers.insert(END, f"{worker['name']} - Lokacja: {location}")

    def add_park(self):
        park_name = self.entry_name.get()
        if park_name:
            coordinates = self.pobierz_koordynaty(park_name)
            if coordinates:
                new_park = {"name": park_name, "guests": [], "workers": []}
                self.parks.append(new_park)
                self.refresh_park_list()
                self.entry_name.delete(0, END)

    def remove_park(self):
        selected_index = self.listbox_parks.curselection()
        if selected_index:
            del self.parks[selected_index[0]]
            self.refresh_park_list()
            self.entry_name.delete(0, END)
            self.listbox_guests.delete(0, END)
            self.listbox_workers.delete(0, END)
            self.update_map_marker()

    def update_park(self):
        selected_index = self.listbox_parks.curselection()
        if selected_index:
            new_name = self.entry_name.get()
            coordinates = self.pobierz_koordynaty(new_name)
            if coordinates:
                self.parks[selected_index[0]]['name'] = new_name
                self.refresh_park_list()

    def add_guest(self):
        if self.selected_park:
            guest_name = self.entry_guest_name.get()
            if guest_name:
                new_guest = {"name": guest_name, "vehicles": [], "location": []}
                self.selected_park['guests'].append(new_guest)
                self.refresh_guest_list()
                self.entry_guest_name.delete(0, END)
                self.update_map_marker()

    def remove_guest(self):
        selected_index = self.listbox_guests.curselection()
        if selected_index and self.selected_park:
            del self.selected_park['guests'][selected_index[0]]
            self.refresh_guest_list()
            self.update_map_marker()

    def update_guest(self):
        selected_index = self.listbox_guests.curselection()
        if selected_index and self.selected_park:
            guest = self.selected_park['guests'][selected_index[0]]
            guest['name'] = self.entry_guest_name.get()
            self.refresh_guest_list()
            self.update_map_marker()

    def add_worker(self):
        if self.selected_park:
            worker_name = self.entry_worker_name.get()
            if worker_name:
                new_worker = {"name": worker_name, "location": []}
                self.selected_park['workers'].append(new_worker)
                self.refresh_worker_list()
                self.entry_worker_name.delete(0, END)
                self.update_map_marker()

    def remove_worker(self):
        selected_index = self.listbox_workers.curselection()
        if selected_index and self.selected_park:
            del self.selected_park['workers'][selected_index[0]]
            self.refresh_worker_list()
            self.update_map_marker()

    def update_worker(self):
        selected_index = self.listbox_workers.curselection()
        if selected_index and self.selected_park:
            worker = self.selected_park['workers'][selected_index[0]]
            worker['name'] = self.entry_worker_name.get()
            self.refresh_worker_list()
            self.update_map_marker()

    def update_vehicle(self):
        selected_index = self.listbox_guests.curselection()
        if selected_index and self.selected_park:
            guest = self.selected_park['guests'][selected_index[0]]
            new_vehicle = self.entry_guest_vehicle.get()
            if new_vehicle:
                guest['vehicles'] = [new_vehicle]
                self.refresh_guest_list()
                self.entry_guest_vehicle.delete(0, END)

    def remove_vehicle(self):
        selected_index = self.listbox_guests.curselection()
        if selected_index and self.selected_park:
            guest = self.selected_park['guests'][selected_index[0]]
            vehicle_to_remove = self.entry_guest_vehicle.get()
            if vehicle_to_remove in guest.get('vehicles', []):
                guest['vehicles'].remove(vehicle_to_remove)
                self.refresh_guest_list()
                self.entry_guest_vehicle.delete(0, END)
                self.update_map_marker()
            else:
                messagebox.showerror('Nieprawidłowy pojazd', 'Podany pojazd nie istnieje dla wybranego gościa.')

    def add_guest_location(self):
        selected_index = self.listbox_guests.curselection()
        if selected_index and self.selected_park:
            guest = self.selected_park['guests'][selected_index[0]]
            new_location = self.entry_guest_location.get()
            if new_location:
                guest['location'] = [new_location]
                self.refresh_guest_list()
                self.entry_guest_location.delete(0, END)
                self.update_map_marker()

    def remove_guest_location(self):
        selected_index = self.listbox_guests.curselection()
        if selected_index and self.selected_park:
            guest = self.selected_park['guests'][selected_index[0]]
            location_to_remove = self.entry_guest_location.get()
            if location_to_remove in guest['location']:
                guest['location'].remove(location_to_remove)
                self.refresh_guest_list()
                self.entry_guest_location.delete(0, END)
                self.update_map_marker()  # Update the map after removing the location

    def add_worker_location(self):
        selected_index = self.listbox_workers.curselection()
        if selected_index and self.selected_park:
            worker = self.selected_park['workers'][selected_index[0]]
            new_location = self.entry_worker_location.get()
            if new_location:
                worker['location'] = [new_location]
                self.refresh_worker_list()
                self.entry_worker_location.delete(0, END)
                self.update_map_marker()

    def remove_worker_location(self):
        selected_index = self.listbox_workers.curselection()
        if selected_index and self.selected_park:
            worker = self.selected_park['workers'][selected_index[0]]
            location_to_remove = self.entry_worker_location.get()
            if location_to_remove in worker['location']:
                worker['location'].remove(location_to_remove)
                self.refresh_worker_list()
                self.entry_worker_location.delete(0, END)
                self.update_map_marker()  # Update the map after removing the locatio

    def update_map_marker(self):

        for marker in list(self.markers.values()):
            marker.delete()
        self.markers.clear()

        if self.selected_park:
            coordinates = self.pobierz_koordynaty(self.selected_park['name'])
            if coordinates:
                latitude, longitude = coordinates
                marker_text = self.selected_park['name']
                marker = self.map_widget.set_marker(latitude, longitude, text=marker_text)
                self.markers[self.selected_park['name']] = marker

            for guest in self.selected_park['guests']:
                for location in guest['location']:
                    coordinates = self.pobierz_koordynaty(location)
                    if coordinates:
                        latitude, longitude = coordinates
                        marker_text = f"{guest['name']} (Gość), Lokalizacja: {location}"
                        marker = self.map_widget.set_marker(latitude, longitude, text=marker_text)
                        self.markers[guest['name']] = marker

            for worker in self.selected_park['workers']:
                for location in worker['location']:
                    coordinates = self.pobierz_koordynaty(location)
                    if coordinates:
                        latitude, longitude = coordinates
                        marker_text = f"{worker['name']} (Pracownik), Lokalizacja: {location}"
                        marker = self.map_widget.set_marker(latitude, longitude, text=marker_text)
                        self.markers[worker['name']] = marker

    def pobierz_koordynaty(self, park_name):
        try:
            url = f'https://nominatim.openstreetmap.org/search?q={park_name}&format=json'
            response = requests.get(url)
            data = response.json()
            if data:
                latitude = float(data[0]['lat'])
                longitude = float(data[0]['lon'])
                return latitude, longitude
            return None
        except Exception as e:
            print("Błąd podczas pobierania koordynatów:", e)
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.start()
