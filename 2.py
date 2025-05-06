import tkinter as tk
import requests

api_key = "rGEMHfyM6umWotsL0TLadOMuHDhVA14mg9Phv5M9QjuM0v4Hz4rz3H5K1Tw8iXXRL5wKdfQnvTbh2wJyIHwzRlfAz7fWXvHmVuFzCHtBOqWI3XgaykfiV84LNHZepSSP"
url = f"https://api.themoviedb.org/3/movie/550?api_key={api_key}"

response = requests.get(url)
data = response.json()
print(f"Фильм: {data['title']}, Рейтинг: {data['vote_average']}")
def fetch_launches():
    try:
        response = requests.get('https://api.spacexdata.com/v4/launches')
        response.raise_for_status()
        launches = response.json()
        return launches
    except requests.RequestException as e:
        return f'Error fetching data: {e}'


def display_launches():
    launches = fetch_launches()
    if isinstance(launches, str):
        output_label.config(text=launches)
    else:
        output_label.config(text=f'Fetched {len(launches)} launches!')


root = tk.Tk()
root.title('SpaceX Launches')


fetch_button = tk.Button(root, text='Fetch SpaceX Launches', command=display_launches)
fetch_button.pack(pady=10)


output_label = tk.Label(root, text='Press the button to fetch launches.')
output_label.pack(pady=10)


root.mainloop()
