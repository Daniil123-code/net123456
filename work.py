INPUT_FILE = 'web_clients_correct.csv'
OUTPUT_FILE = 'web_clients_description.txt'

GENDER_MAP = {'female': 'женского пола', 'male': 'мужского пола'}
VERB_MAP = {'female': 'совершила', 'male': 'совершил'}
DEVICE_MAP = {
    'mobile': 'мобильного',
    'tablet': 'планшетного',
    'desktop': 'настольного',
    'laptop': 'портативного'
}


def parse_csv_line(line):
    fields = []
    current = []
    in_quotes = False
    i = 0
    while i < len(line):
        char = line[i]
        if char == '"':
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                current.append('"')
                i += 1
            else:
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            fields.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        i += 1
    fields.append("".join(current).strip())
    return fields


def process_data():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return

    if not lines:
        return

    results = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        f = parse_csv_line(line)
        if len(f) >= 6:
            name = f[0]
            dev = f[1]
            bro = f[2]
            sex = f[3]
            age = f[4]
            bill = f[5]
            reg = f[6] if len(f) > 6 and f[6] != '-' else "неизвестный регион"

            g_txt = GENDER_MAP.get(sex, sex)
            v_txt = VERB_MAP.get(sex, "совершил(а)")
            d_txt = DEVICE_MAP.get(dev, dev)

            res = (f"Пользователь {name} {g_txt}, {age} лет {v_txt} покупку на {bill} у.е. "
                   f"с {d_txt} браузера {bro}. Регион, из которого совершалась покупка: {reg}.")
            results.append(res)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        out.write("\n".join(results))


process_data()