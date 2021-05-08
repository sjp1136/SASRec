import linecache

# Go through first 15 lines of mapping.txt
# For each line, use the user_id in Steam2.txt to find the reviews the user posted
# Use the line number location in Steam2.txt to find corresponding JSON review in steam_reviews.json


def main():
    results = {}
    total = 15
    count = 0
    with open('../mapping.txt', 'r') as reader:
        # [user_id, next_recommended_item_id]
        line = reader.readline()

        while count < total:
            print("mapping: " + line)
            user_id = line.split()[0]
            next_recommended_item_id = line.split()[1]

            with open('../data/Steam2.txt') as steam_reader:
                # [user_id, item_id, line number]
                steam_line = steam_reader.readline()
                # print("Steam2: " + steam_line)
                while steam_line != '':
                    steam_user_id = steam_line.split()[0]
                    if steam_user_id == user_id:
                        print("Steam2 match: " + steam_line)
                        line_number = int(steam_line.split()[2])
                        reviews_line = linecache.getline("../data/steam_reviews.json", line_number)
                        print(reviews_line)
                    steam_line = steam_reader.readline()

            line = reader.readline()
            count += 1


if __name__ == "__main__":
    main()
