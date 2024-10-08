import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.stats import norm

matplotlib.use('TkAgg')

'''
# TODO plotar gráficos baseado em dados de um arquivo csv usando a matplotlib
#*   Graficos de dispersão:  (Se ficar pontos demais pode filtrar os 10 com mais gols de cada time
#*       NP-xG/90 x Goals/90;
#*       Hdrs A x % Headers Won;

#*   Graficos radar/aranha: 
#*       Goals/90, xG/90, xG Overperformance, % Shots on Target, Dribbles/90 do jogador com mais gols de cada time

#*   Histograma:
#*       Gls (gols totais do jogador) de todos os jogadores de todos os times com linha de distribuição normal
'''

HEADERS ={
   "Name": 0,
   "Initial Apps": 1,
   "Bench Apps": 2,
   "Total Apps": 3,
   "Mins": 4,
   "Mins/App": 5,
   "Gls": 6,
   "Goals/90": 7,
   "xG": 8,
   "xG Overperformance": 9,
   "NP-xG": 10,
   "NP xG/90": 11,
   "Shots": 12,
   "ShT": 13,
   "% Shots on Target": 14,
   "Hdrs A": 15,
   "Hdrs": 16,
   "% Headers Won": 17,
   "Drb": 18,
   "Dribbles/90": 19,
   "Pens": 20,
   "Pens S": 21,
   "% Penalties Scored": 22
}

def sanitize_row (row, debug=False):    
    _row = row.copy()
   
    for index, item in enumerate(_row):
        if(index in [6, 7, 9, 11, 14, 15, 17, 19]):
            if item == "NaN" or item == "nan":
                _row[index] = 0.00
            else:
                _row[index] = round(float(item), 2)
    
    if(debug):
        for i in range(len(_row) - 1):
            if(row[i] != _row[i]):
                print(f"Changed {row[i]} to {_row[i]} type: {type(_row[i])}")

    return _row

def import_csv (file_path, debug=False):
    BASE_PATH = "input_files"
    BASE_EXT = ".csv"
    data = []
    
    with open(f"{BASE_PATH}/{file_path}{BASE_EXT}", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            if(row[0] != "Name"):
                data.append(sanitize_row(row, debug))
    
    return data

def get_goals (teams_data):
    goals = []

    for team in teams_data:
        goals += [row[HEADERS["Gls"]] for row in team]
        
    return goals

def get_radar_values (data):
    goals_list = [row[HEADERS["Goals/90"]] for row in data]
    best_player_index = goals_list.index(max(goals_list))
    best_player_stats = data[best_player_index]

    goals = best_player_stats[HEADERS["Goals/90"]]
    xg = best_player_stats[HEADERS["NP xG/90"]]
    header_won = best_player_stats[HEADERS["% Headers Won"]]/100
    shots_on_target = best_player_stats[HEADERS["% Shots on Target"]]/100
    dribbles = best_player_stats[HEADERS["Dribbles/90"]]

    return [goals, xg, header_won, shots_on_target, dribbles]

def plot_scatter_goals (team_name, data):
    title = "Gols esperados em 90min X Gols em 90min - " + team_name
    x_label = "NP xG/90"
    y_label = "Goals/90"
    
    plot_scatter(x_label, y_label, title, data)

def plot_scatter_headers (team_name, data):
    title = "% de Cabeçadas Ganhas X Cabeçadas Disputadas - " + team_name
    x_label = "Hdrs A"
    y_label = "% Headers Won"
   
    plot_scatter(x_label, y_label, title, data)

def plot_scatter(x_label, y_label, title, data):
    x = HEADERS[x_label]
    y = HEADERS[y_label]

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    x_data = [row[x] for row in data]
    y_data = [row[y] for row in data]

    plt.scatter(x_data, y_data)

    for i in range(len(data)):
        plt.annotate(data[i][0], (data[i][x], data[i][y]))
    
    plt.show()

def plot_radar (data):
    labels = ['Goals/90', 'NP xG/90', '% Headers Won', '% Shots on Target', 'Dribbles/90']
    num_vars = len(labels)
    
    colors = ['blue', 'red', 'green']
    team_names = ["Grêmio", "Internacional", "Juventude"]

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for i in range(len(data)):
        values = data[i]
        values += values[:1] 
        ax.fill(angles, values, color=colors[i], alpha=0.25)
        ax.plot(angles, values, color=colors[i], linewidth=2, label=team_names[i])

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.title('Radar de performance \n(melhor jogador por time)', size=20, weight='bold', ha='center')
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    plt.show()

def plot_histogram (data):
    plt.figure(figsize=(8, 6))
    count, bins, ignored = plt.hist(data, bins=30, density=False, color='green', alpha=0.6, edgecolor='black')
    
    mu, std = norm.fit(data)
    
    bin_width = bins[1] - bins[0]
    scale_factor = len(data) * bin_width
    
    xmin, xmax = int(np.floor(bins[0])), int(np.ceil(bins[-1]))  
    x = np.arange(xmin, xmax + 1, 1) 
    p = norm.pdf(x, mu, std) * scale_factor
    
    plt.plot(x, p, 'r', linewidth=2)
    
    plt.xticks(np.arange(xmin, xmax + 1, 1))
    
    title = "Historiograma de número de gols:\n média: %.2f  desvio padrão: %.2f" % (mu, std)
    plt.title(title)
    plt.xlabel('Quantidade de Gols')
    plt.ylabel('Quantidade de Jogadores')
    
    plt.show()

def __main__ ():
    teams = ["gremio", "inter", "juventude"]
    team_names = {"gremio": "Grêmio", "inter": "Internacional", "juventude": "Juventude"}

    radar_data = []
    teams_data = []
    for team in teams:
        name = team_names[team]
        
        data = import_csv(team)
        teams_data.append(data)
        radar_data.append(get_radar_values(data))

        plot_scatter_goals(name, data)
        plot_scatter_headers(name, data)
    
    goals = get_goals(teams_data)
    plot_histogram(goals)
    
    plot_radar(radar_data)

if __name__ == "__main__":
    __main__()
