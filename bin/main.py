import os
from os.path import join as path_join
from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Dict, List
from itertools import groupby

import pandas as pd
from docxtpl import DocxTemplate, RichText

from row import Row, FONT
from translator import translate

df = pd.read_excel('data.xlsx', "data")
df["id"] = range(1, len(df) + 1)

def process_data(data):
    rows = [Row(**row) for row in data.to_dict(orient="records")]
    return rows

def render_docx(template_name: str, save_path: str, context: dict, file_suffix=''):
    template_path = path_join("templates", f"{template_name}_template{file_suffix}.docx")
    doc = DocxTemplate(template_path)
    doc.render(context)
    doc.save(save_path)


def ardzanagrutyun(row: Row, additional_info={}, file_suffix=''):
    file_name = "ardzanagrutyun"

    if "grouped" in file_suffix:
        all_entalots_empty = all(
            not group["entalot"].strip()
            for group in additional_info["groups"]
        )

        if all_entalots_empty:
            file_suffix += "_without_entalot"

    save_path = f"{row.paymanagri_hamar}_{file_name}{file_suffix}.docx"
    if os.path.exists(save_path):
        return

    info = row.model_dump()
    info.update(additional_info)
    render_docx(file_name, save_path, info, file_suffix)


def paymanagir(row: Row, additional_info={}, file_suffix=''):
    file_name = "paymanagir"

    if "grouped" in file_suffix:
        all_entalots_empty = all(
            not group["entalot"].strip()
            for group in additional_info["groups"]
        )

        if all_entalots_empty:
            file_suffix += "_without_entalot"

    save_path = f"{row.paymanagri_hamar}_{file_name}{file_suffix}.docx"
    if os.path.exists(save_path):
        return

    info = row.model_dump()
    info.update(additional_info)
    render_docx(file_name, save_path, info, file_suffix)


# alignement problem
def vkayakan(data: list[Row]):
    file_name = "vkayakan"

    def render_vkayakan(i, contents):
        save_path = f"{file_name}_{i}.docx"
        if os.path.exists(save_path):
            return

        lot_info = [
            f"Խումբ {row.xumb} ԼՈՏ {row.lot} {f'ենթալոտ {row.entalot}' if row.entalot else ''} մեկնարկային գինը {row.meknarkayin_gin} ՀՀ դրամ,"
            for row in contents
        ]

        context = contents[0].model_dump()
        context.update({
            "id": RichText(i, font=FONT, size=12*2, bold=True, underline=True),
            "lot_info": RichText('\n\t'.join(lot_info), font=FONT, size=12*2, bold=False, underline=False),
        })

        render_docx(file_name, save_path, context)

    grouped_rows = {}
    for row in data:
        grouped_rows.setdefault(row.gnord, []).append(row)

    threads = []
    max_workers = max(1, os.cpu_count() // 2)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i, contents in enumerate(grouped_rows.values(), 1):
            threads.append((i, executor.submit(render_vkayakan, i, contents)))

    for i, thread in threads:
        try:
            thread.result()
        except Exception as e:
            print(f"\nvkayakan{i}: {e}")


def run_process(data: list[Row]):
    threads = []
    errors = []

    grouped: Dict[str, List[Row]] = {
        paymanagri_hamar: list(obj)
        for paymanagri_hamar, obj in groupby(data, lambda row: row.paymanagri_hamar)
    }

    max_workers = os.cpu_count() // 2
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        threads.append((-1, executor.submit(vkayakan, data)))

        for index, d in enumerate(grouped, 2):
            row = grouped[d][0]

            if len(grouped[d]) == 1:
                threads.append((index, executor.submit(ardzanagrutyun, row)))
                threads.append((index, executor.submit(paymanagir, row)))
            else:
                additional_info = {
                    "groups": [
                        {
                            "xumb": obj.xumb,
                            "lot": obj.lot,
                            "entalot": obj.entalot if obj.entalot else "",
                            "guyqi_anvanum": translate(obj.guyqi_anvanum),
                            "meknarkayin_gin": Row.gin_to_str(obj.meknarkayin_gin),
                            "guyqi_arjeq": Row.gin_to_str(obj.guyqi_arjeq),
                            "guyqayin_hamar": obj.guyqayin_hamar
                        }
                        for obj in grouped[d]
                    ]
                }
                guyqi_arjeq_sum = sum(map(lambda o: int(o['guyqi_arjeq'].replace('.', '')), additional_info["groups"]))
                meknarkayin_gin_sum = sum(map(lambda o: int(o['meknarkayin_gin'].replace('.', '')), additional_info["groups"]))
                additional_info['accumulated'] = {
                    'guyqi_arjeq': Row.gin_to_str(guyqi_arjeq_sum),
                    'meknarkayin_gin': Row.gin_to_str(meknarkayin_gin_sum)
                }
                threads.append((index, executor.submit(ardzanagrutyun, row, additional_info, "_grouped")))
                threads.append((index, executor.submit(paymanagir, row, additional_info, "_grouped")))

    for i, thread in threads:
        try:
            thread.result()
        except Exception as e:
            if str(i) not in errors:
                errors.append(f"\n{i}: {e}")

    if errors:
        print(f'Errors: {"".join(errors)}')


def main():
    parser = ArgumentParser()
    parser.add_argument('-n', '--numbers', required=False)
    args = parser.parse_args()
    numbers = []

    if args.numbers:
        numbers = list(map(int, args.numbers.split(',')))

    data = process_data(df)
    if numbers:
        data = data[data["id"].isin(numbers)]

    from time import time
    s = time()
    run_process(data) # ~44 s
    print(f"Time: {time() - s}")


if __name__ == "__main__":
    main()
