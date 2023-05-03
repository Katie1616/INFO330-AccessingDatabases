import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

# Connection to database
conn = sqlite3.connect('pokemon.sqlite')
cursor = conn.cursor()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    # selects pokedex_number 
    cursor.execute('SELECT * FROM pokemon WHERE pokedex_number = ?', (pokemon_id,))
    line = cursor.fetchone()

    if line: 
        pokedex_number, name, type_1, type_2, total, hp, attack, defense, sp_attack, sp_defense, speed, generation, legendary = line
        types_str = (f"{type_1} {type_2}".strip())
        against = []
        for type_name in types:
            against_attr = (f"against_{type_name}")
            against_value = getattr(line, against_attr)
            if against_value > 1:
                against.append(type_name)
                print(f"{name} is strong against {type_name}")
            elif against_value < 1:
                print(f"but {name} is weak against {type_name}")
            else:
                pass

    print("Analyzing ", pokedex_number)
    print(f"{name} ({types_str}) is strong against {against} but weak against {[t for t in types if t not in against]}")
    # Analyze the pokemon whose pokedex_number is in "arg"

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

    