import json
import time

times = []
with open("my own bot\puns.json", "r") as file:
    bans = json.load(file)

for pun in bans["pun-times"]:
    times.append(pun["time"])
min_time = min(times)
# max_time = max(times)


while True:

    for ban in bans["pun-times"]:
        print(ban)
        
        if ban["time"] <= 0:
            ban["time"] = 0
        if ban["time"] > 0:
            ban["time"] -= 10

    with open("my own bot\puns.json", "w") as file:
        json.dump(bans, file)
    time.sleep(10)
