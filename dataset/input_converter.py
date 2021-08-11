import sys
import pandas as pd
import numpy as np

INPUT_FILE_NAME = "./ml-latest.rating"
OUTPUT_FILE_NAME = "./ml-latest-binary.rating"
WATCHED = 1


def rate_score_to_binary():
    df = pd.DataFrame([(-1, -1, -1, -1)], columns=['U', 'I', 'R', 'T'])
    with open(INPUT_FILE_NAME, "r") as scores:
        print(f'opening {INPUT_FILE_NAME} done!')
        for line in scores:
            char_in_line = line.split(",")
            user_id = int(char_in_line[0])
            movie_id = int(char_in_line[1])
            rate = WATCHED
            timestamp = int(char_in_line[3])

            df = df.append({'U': user_id, 'I': movie_id, 'R': rate,
                            'T': timestamp}, ignore_index=True)

    print(f'making output csv as {OUTPUT_FILE_NAME}')
    df.to_csv(OUTPUT_FILE_NAME)


if __name__ == "__main__":
    rate_score_to_binary()
    print("all done!")
