import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
from swarm import Swarm

def wizualizuj_osobnika(osobnik: Swarm):
    liczba_roverow = len(osobnik.chromosome)
    colors = cm.get_cmap('tab10', liczba_roverow)  # Różne kolory dla każdego roverka

    plt.figure(figsize=(10, 8))
    
    for idx, rover in enumerate(osobnik.chromosome):
        # Startujemy od pozycji początkowej
        x = [osobnik.start_position.x]
        y = [osobnik.start_position.y]
        labels = ["START"]

        # Dodajemy wszystkie POI w kolejności z listy
        for poi in rover.pois_list:
            x.append(poi.position.x)
            y.append(poi.position.y)
            labels.append(f"POI {poi.poi_number}")

        # Rysujemy trasę rovera
        plt.plot(x, y, marker='o', linestyle='-', color=colors(idx), label=f'Rover {idx + 1}')

        # Opisujemy każdy punkt
        for i in range(len(x)):
            plt.text(x[i], y[i], labels[i], fontsize=9, ha='right')

    plt.title("Trasy wszystkich Roverów")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def wizualizuj_generacje(generacja: list[Swarm]):
    iteracje = list(range(len(generacja)))
    fitness_scores = [swarm.fitness for swarm in generacja]

    plt.figure(figsize=(10, 6))
    plt.plot(iteracje, fitness_scores, marker='o', linestyle='-', color='blue')
    plt.xlabel('Numer osobnika w generacji')
    plt.ylabel('Fitness score')
    plt.title('Fitness osobników w generacji')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def wizualizuj_timr_generacje(generacja: list[Swarm]):
    iteracje = list(range(len(generacja)))
    fitness_scores = [swarm.time for swarm in generacja]

    plt.figure(figsize=(10, 6))
    plt.plot(iteracje, fitness_scores, marker='o', linestyle='-', color='blue')
    plt.xlabel('Numer osobnika w generacji')
    plt.ylabel('time')
    plt.title('time osobników w generacji')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def wizualiacja_skippowania_poi(najlepsze_osobniki_z_kazdej_generacji: list[Swarm]):
    generacje = list(range(len(najlepsze_osobniki_z_kazdej_generacji)))
    skipniete_poi = []

    for swarm in najlepsze_osobniki_z_kazdej_generacji:
        suma_skipow = sum(rover.skipped for rover in swarm.chromosome)
        skipniete_poi.append(suma_skipow)

    plt.figure(figsize=(10, 6))
    plt.bar(generacje, skipniete_poi, color='orange')
    plt.xlabel('Numer generacji')
    plt.ylabel('Liczba skipniętych POI')
    plt.title('Skipnięte POI w kolejnych generacjach')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()



def visualize_swarm_paths(swarm):
    fig, ax = plt.subplots(figsize=(12, 8))

    rovers = swarm.chromosome
    num_rovers = len(rovers)
    colors = cm.tab20(np.linspace(0, 1, num_rovers))

    for idx, rover in enumerate(rovers):
        visited_pois = []
        current_pos = rover.start_position
        total_time = 0

        for poi in rover.pois_list:
            distance = math.sqrt(
                (current_pos.x - poi.position.x) ** 2 + 
                (current_pos.y - poi.position.y) ** 2
            )
            time_needed = distance + poi.time_of_task  # <-- TU BYŁA ZMIANA
            if total_time + time_needed <= rover.max_time:
                visited_pois.append(poi)
                total_time += time_needed
                current_pos = poi.position
            else:
                break

        path = [rover.start_position] + [poi.position for poi in visited_pois]
        x_vals = [p.x for p in path]
        y_vals = [p.y for p in path]
        ax.plot(x_vals, y_vals, linestyle='-', linewidth=2.0, color=colors[idx], label=f'Rover {idx+1}')

        for poi in visited_pois:
            ax.scatter(poi.position.x, poi.position.y, color=colors[idx], s=30, alpha=0.7)

    # Start position (zielona kropka)
    ax.scatter(rovers[0].start_position.x, rovers[0].start_position.y, color='green', s=100, label='Start')

    ax.set_title('Trasy wszystkich roverów w swarmie')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()