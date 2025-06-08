import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.image as mpimg
from itertools import permutations

class WeightedGraph:
    def __init__(self):
        self.listkota = {}

    def tambahkanKota(self, kota):
        if kota not in self.listkota:
            self.listkota[kota] = {}

    def tambahkanJalan(self, kota1, kota2, jarak):
        if kota1 in self.listkota and kota2 in self.listkota:
            self.listkota[kota1][kota2] = jarak
            self.listkota[kota2][kota1] = jarak

    def djikstra(self, source):
        distances = {kota: float('inf') for kota in self.listkota}
        distances[source] = 0
        previous_nodes = {kota: None for kota in self.listkota}
        unvisited = list(self.listkota.keys())

        while unvisited:
            current = min(unvisited, key=lambda kota: distances[kota])
            unvisited.remove(current)
            for neighbor, weight in self.listkota[current].items():
                new_distance = distances[current] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current

        result = {}
        for kota in self.listkota:
            path = []
            current = kota
            while current:
                path.insert(0, current)
                current = previous_nodes[current]
            result[kota] = {"distance": distances[kota], "path": path}
        return result

    def tsp(self, start):
        kota_lain = list(self.listkota.keys())
        kota_lain.remove(start)

        min_path = None
        min_distance = float('inf')

        for perm in permutations(kota_lain):
            path = [start] + list(perm) + [start]
            total = 0
            valid = True
            for i in range(len(path) - 1):
                kota1, kota2 = path[i], path[i + 1]
                if kota2 in self.listkota[kota1]:
                    total += self.listkota[kota1][kota2]
                else:
                    valid = False
                    break
            if valid and total < min_distance:
                min_distance = total
                min_path = path

        return min_path, min_distance
    
    def display_ascii_map(self):
            print("\n=== ASCII Map of the Graph ===\n")
            printed_edges = set()
            for city in self.listkota:
                for neighbor, distance in self.listkota[city].items():
                    edge = tuple(sorted((city, neighbor)))
                    if edge in printed_edges:
                        continue
                    printed_edges.add(edge)
                    print(f"{edge[0]:<12} -- {distance:>3} --> {edge[1]}")
            print("\nNote: The graph is undirected, so each connection is only shown once.\n")

    def print_dijkstra_ascii_table(WeightedGraph, source: str):
        result = WeightedGraph.djikstra(source)
        
        # Header
        print("\nInterpreting the Results")
        print(f"\nFrom city: {source}")
        print("\n" + "-" * 50)
        print(f"{'Vertex':<12} {'Known?':<8} {'Distance(Km)':<6} {'Path':<10}")
        print("-" * 50)

        for city in sorted(WeightedGraph.listkota.keys()):
            cost = result[city]["distance"]
            path = result[city]["path"]

            # Determine previous node in path
            if len(path) <= 1:
                prev = "-"
            else:
                prev = path[-2]

            known = "Y" if cost != float('inf') else "N"
            cost_str = str(cost) if cost != float('inf') else "∞"

            print(f"{city:<12} {known:<8} {(cost_str):<12} {prev:<10}")
        print("-" * 50)


    def tampilkan_tsp(self, positions, start, background_image='./peta_jatim.jpg'):
        path, total_distance = self.tsp(start)

        G = nx.Graph()
        for kota, tetangga in self.listkota.items():
            for tujuan, jarak in tetangga.items():
                G.add_edge(kota, tujuan, weight=jarak)

        img = mpimg.imread(background_image)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(img, extent=[0, 700, 0, 400])

        node_colors = ["orange" if kota in path else "skyblue" for kota in G.nodes]
        edge_colors = []
        edge_widths = []
        tsp_edges = list(zip(path, path[1:]))

        for u, v in G.edges:
            if (u, v) in tsp_edges or (v, u) in tsp_edges:
                edge_colors.append("darkorange")
                edge_widths.append(3.5)
            else:
                edge_colors.append("#bbbbbb")
                edge_widths.append(1.5)

        nx.draw(
            G,
            pos=positions,
            ax=ax,
            with_labels=True,
            node_color=node_colors,
            node_size=1200,
            font_size=9,
            font_weight='bold',
            edge_color=edge_colors,
            width=edge_widths
        )

        nx.draw_networkx_edge_labels(
            G,
            pos=positions,
            edge_labels=nx.get_edge_attributes(G, 'weight'),
            ax=ax,
            font_size=7,
            font_color="#555",
            label_pos=0.5,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.6)
        )

        plt.title(f"Rute TSP dari {start} (Kembali ke {start})", fontsize=13, fontweight='bold', color='darkblue')
        plt.figtext(0.5, 0.01, f"Total Distance Travel: {total_distance} km", ha='center', fontsize=11, color='darkred')
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    def tampilkan_graf_dengan_jalur(self, positions, source, target, background_image='./peta_jatim.jpg'):
        hasil = self.djikstra(source)
        path = hasil[target]["path"]

        G = nx.Graph()
        for kota, neighbors in self.listkota.items():
            for neighbor, jarak in neighbors.items():
                G.add_edge(kota, neighbor, weight=jarak)

        img = mpimg.imread(background_image)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(img, extent=[0, 700, 0, 400])

        node_colors = [
            "green" if kota == source else
            "red" if kota == target else
            ("orange" if kota in path else "skyblue")
            for kota in G.nodes
        ]

        edge_colors = []
        edge_widths = []
        path_edges = list(zip(path, path[1:]))

        for u, v in G.edges:
            if (u, v) in path_edges or (v, u) in path_edges:
                edge_colors.append("orange")
                edge_widths.append(3)
            else:
                edge_colors.append("gray")
                edge_widths.append(1.2)

        nx.draw(
            G,
            pos=positions,
            ax=ax,
            with_labels=True,
            node_color=node_colors,
            node_size=1300,
            font_size=9,
            font_weight='bold',
            edge_color=edge_colors,
            width=edge_widths
        )

        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=edge_labels, ax=ax, font_size=7)

        total_distance = hasil[target]["distance"]
        plt.title(f"Jalur dari {source} ke {target}", fontsize=13, fontweight='bold', color='darkblue')
        plt.figtext(0.5, 0.01, f"Total Distance: {total_distance} km", ha='center', fontsize=11, color='darkred')
        plt.axis("off")
        plt.tight_layout()
        plt.show()

positions = {
    "Surabaya": (365, 240), "Tulungagung": (225, 116), "Malang": (343, 135),
    "Banyuwangi": (654, 97.5), "Mojokerto": (309, 207), "Gresik": (300, 280),
    "Ngawi": (130, 216), "Kediri": (236, 151), "Tuban": (238, 290), "Madura": (487, 266),
}

jalur = [
    ("Surabaya", "Madura", 20), ("Surabaya", "Tuban", 30), ("Surabaya", "Gresik", 25),
    ("Tulungagung", "Mojokerto", 85), ("Tulungagung", "Kediri", 70), ("Malang", "Surabaya", 60),
    ("Banyuwangi", "Malang", 55), ("Kediri", "Ngawi", 35), ("Tuban", "Ngawi", 15),
    ("Madura", "Banyuwangi", 65), ("Malang", "Tulungagung", 95), ("Kediri", "Malang", 10),
    ("Gresik", "Mojokerto", 45), ("Ngawi", "Madura", 85), ("Ngawi", "Mojokerto", 60),
    ("Madura", "Malang", 80), ("Banyuwangi", "Tuban", 120), ("Banyuwangi", "Ngawi", 100),
    ("Kediri", "Madura", 50), ("Kediri", "Gresik", 40), ("Gresik", "Tulungagung", 90),
    ("Mojokerto", "Malang", 55), ("Tuban", "Gresik", 35), ("Tuban", "Mojokerto", 60),
    ("Madura", "Gresik", 75), ("Tulungagung", "Tuban", 80), ("Banyuwangi", "Mojokerto", 110),
    ("Malang", "Ngawi", 70), ("Kediri", "Tuban", 45), ("Madura", "Tulungagung", 95),
]

petajawa = WeightedGraph()
for kota in positions:
    petajawa.tambahkanKota(kota)

for kota1, kota2, jarak in jalur:
    petajawa.tambahkanJalan(kota1, kota2, jarak)
petajawa.display_ascii_map()

def jalankan_visualisasi():
    kota_awal = combo_awal.get()
    kota_tujuan = combo_tujuan.get()
    if kota_awal == kota_tujuan:
        tk.messagebox.showerror("Error", "Kota awal dan tujuan tidak boleh sama!")
    else:
        petajawa.tampilkan_graf_dengan_jalur(positions, kota_awal, kota_tujuan)

petajawa.print_dijkstra_ascii_table("Surabaya")
petajawa.tampilkan_tsp(positions, "Surabaya")

root = tk.Tk()
root.title("Visualisasi Jalur Kota Jawa Timur")
root.geometry("400x230")

label1 = tk.Label(root, text="Pilih Kota Awal:")
label1.pack(pady=(15, 5))
combo_awal = ttk.Combobox(root, values=sorted(positions.keys()))
combo_awal.set("Surabaya")
combo_awal.pack()

label2 = tk.Label(root, text="Pilih Kota Tujuan:")
label2.pack(pady=(10, 5))
combo_tujuan = ttk.Combobox(root, values=sorted(positions.keys()))
combo_tujuan.set("Tulungagung")
combo_tujuan.pack()

btn = tk.Button(root, text="Tampilkan Jalur", command=jalankan_visualisasi)
btn.pack(pady=20)

root.mainloop()
