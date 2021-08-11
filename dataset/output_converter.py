import sys
import numpy as np

ITEM_IDS = None
FROM_IDX = 1
TO_IDX = 0


def get_file_names():
    target_folder = sys.argv[1]
    target_file_name = sys.argv[2]
    target_file_name = f"{target_folder}/{target_file_name}"
    output_file_name = f"{target_file_name.split('.raw')[0]}.json"

    tmp_file_name = "ml-latest-binary_ratio_u0_i0"
    item2id_file_name = f"{target_folder}/{tmp_file_name}.item2id"
    user2id_file_name = f"{target_folder}/{tmp_file_name}.user2id"

    return target_file_name, item2id_file_name, user2id_file_name, output_file_name


def init_lists():
    global ITEM_IDS
    ITEM_IDS = np.empty(shape=[0, 2])
    return


def id_from_file(file, origin_id):
    file.seek(0)
    for line in file:
        from_id = int(line.split(',')[FROM_IDX])
        if from_id == origin_id:
            return int(line.split(',')[TO_IDX])

    print(f"Convert USER id {origin_id} failed.")
    return -1


def item_id_from_list(origin_id):
    result = ITEM_IDS[np.where(ITEM_IDS[:, FROM_IDX] == origin_id)]
    if len(result) == 1:
        return result[0][TO_IDX]
    else:
        return -1


def convert_item_id(file, origin_id):
    from_list = item_id_from_list(origin_id)

    if from_list != -1:
        return from_list
    else:
        return id_from_file(file, origin_id)


def convert_all(origin_name, item_name, user_name, output_name):
    with open(output_name, 'w') as output_file, open(item_name, 'r') as item_file, open(user_name, 'r') as user_file, open(origin_name, 'r') as origin_file:
        output_file.write('{\n')

        for line in origin_file:
            origin_user_id = int(line.split(": ")[0])
            origin_movie_ids = [int(number) for number in (
                (line.split(": ")[1]).split(", "))]

            new_user_id = id_from_file(user_file, origin_user_id)
            new_movie_ids = [convert_item_id(
                item_file, origin_id) for origin_id in origin_movie_ids]

            new_line = f'"{new_user_id}": {new_movie_ids},\n'
            output_file.write(new_line)

        output_file.write('}')
    return


if __name__ == "__main__":
    target_file_name, item2id_file_name, user2id_file_name, output_file_name = get_file_names()
    print(f"Start to convert: {target_file_name}")
    print(f"           using: {item2id_file_name}")
    print(f"                  {user2id_file_name}")
    print(f"            into: {output_file_name}")

    init_lists()
    convert_all(target_file_name, item2id_file_name,
                user2id_file_name, output_file_name)
    print("Done!")
