import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

conn = sqlite3.connect("../pokemon.sqlite")
cursor = conn.cursor()

types = ["bug", "dark", "dragon", "electric", "fairy", "fight",
                "fire", "flying", "ghost", "grass", "ground", "ice", "normal",
                "poison", "psychic", "rock", "steel", "water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Analyze the pokemon whose pokedex_number is in "arg"
    for pokemon_id in sys.argv[1:]:

        pokemon_name = cursor.execute(
            "SELECT name FROM pokemon WHERE id=?", (pokemon_id,)).fetchone()
        name = pokemon_name[0]
        print("Analyzing ", pokemon_id)

        type1 = cursor.execute(
            "SELECT type1 FROM pokemon_types_view WHERE name=?",
                    (pokemon_name[0],)).fetchall()
        type2 = cursor.execute(
            "SELECT type2 FROM pokemon_types_view WHERE name=?", (pokemon_name[0],)).fetchall()   
        for i, type in enumerate(types):
            strengths = []
            weaknesses = []
            against = cursor.execute(
                "SELECT against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM pokemon_types_battle_view WHERE type1name=? AND type2name=?",
                (type1[0][0], type2[0][0])).fetchone()
            for j, val in enumerate(against):
                if val > 1:
                    strengths.append(types[j])
                elif val < 1:
                    weaknesses.append(types[j])
        print(name, "({} {})".format(type1[0][0], type2[0][0]).replace
              ("'", ""), "is strong against", strengths,
              "but weak against", weaknesses)


    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type

# Closing cursor and connection
cursor.close()
conn.close()

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")
