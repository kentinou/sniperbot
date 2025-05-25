
import pandas as pd

def afficher_winrate():
    try:
        df = pd.read_csv("performance_log.csv")
    except FileNotFoundError:
        print("Aucun fichier de journal trouvé.")
        return

    completed = df[df['result'].isin(["win", "loss"])]
    total = len(completed)
    wins = len(completed[completed['result'] == "win"])
    losses = len(completed[completed['result'] == "loss"])
    winrate = (wins / total * 100) if total > 0 else 0

    print(f"📊 Total trades terminés : {total}")
    print(f"✅ Gagnés : {wins}")
    print(f"❌ Perdus : {losses}")
    print(f"🎯 Winrate : {winrate:.2f}%")

if __name__ == "__main__":
    afficher_winrate()
