INPUT_FILE = 'web_clients_correct.csv'
OUTPUT_FILE = 'web_clients_description.txt'

GENDER_MAP = {
    'female': 'женского пола',
    'male': 'мужского пола'
}

VERB_MAP = {
    'female': 'совершила',
    'male': 'совершил'
}

DEVICE_ADJECTIVE_MAP = {
    'mobile': 'мобильного',
    'tablet': 'планшетного',
    'desktop': 'настольного',
    'laptop': 'портативного'
}


def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        return []


def parse_csv_line(line):
    result = []
    current_val = []
    in_quotes = False
    i = 0

    while i < len(line):
        char = line[i]

        if in_quotes:
            if char == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    current_val.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                current_val.append(char)
        else:
            if char == '"':
                in_quotes = True
            elif char == ',':
                result.append("".join(current_val))
                current_val = []
            else:
                current_val.append(char)
        i += 1

    result.append("".join(current_val))
    return result


def transform_data(raw_data):
    try:
        name = raw_data[0]
        device_key = raw_data[1]
        browser = raw_data[2]
        sex_key = raw_data[3]
        age = raw_data[4]
        bill = raw_data[5]
        region = raw_data[6]

        gender_text = GENDER_MAP.get(sex_key, sex_key)
        verb = VERB_MAP.get(sex_key, 'совершил(а)')
        device_text = DEVICE_ADJECTIVE_MAP.get(device_key, device_key)

        return {
            'name': name,
            'gender_text': gender_text,
            'verb': verb,
            'age': age,
            'bill': bill,
            'device_text': device_text,
            'browser': browser,
            'region': region
        }
    except IndexError:
        return None


def generate_description(client_dict):
    template = (
        "Пользователь {name} {gender_text}, {age} лет "
        "{verb} покупку на {bill} у.е. с {device_text} браузера {browser}. "
        "Регион, из которого совершалась покупка: {region}."
    )
    return template.format(**client_dict)


def save_to_file(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def main():
    raw_lines = read_file(INPUT_FILE)

    if not raw_lines:
        return

    data_lines = raw_lines[1:]
    processed_descriptions = []

    for line in data_lines:
        parsed_fields = parse_csv_line(line)

        if len(parsed_fields) < 7:
            continue

        client_data = transform_data(parsed_fields)

        if client_data:
            description = generate_description(client_data)
            processed_descriptions.append(description)

    save_to_file(OUTPUT_FILE, processed_descriptions)


if name == "main":
    main()