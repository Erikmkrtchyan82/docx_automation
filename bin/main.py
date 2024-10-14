from docxtpl import DocxTemplate, RichText
import pandas as pd
import os
from os.path import join as path_join
from concurrent.futures import ProcessPoolExecutor
from argparse import ArgumentParser
from typing import Dict
from row import Row, FONT
from itertools import groupby
from translator import translate

excel = pd.read_excel('data.xlsx', None)
data = excel["data"].to_dict(orient="records")
users_list = excel["user"].to_dict(orient="records")
users = {}

def ardzanagrutyun(row: Row, additional_info={}, file_suffix=''):
    file_name = "ardzanagrutyun"

    doc = DocxTemplate(path_join("templates", f"{file_name}_template{file_suffix}.docx"))

    save_path = f"{row.paymanagri_hamar}_{file_name}{file_suffix}.docx"
    if os.path.exists(save_path):
        return

    info = row.model_dump()
    info.update(additional_info)
    doc.render(info)
    doc.save(save_path)


def paymanagir(row: Row, additional_info={}, file_suffix=''):
    file_name = "paymanagir"

    doc = DocxTemplate(path_join("templates", f"{file_name}_template{file_suffix}.docx"))

    save_path = f"{row.paymanagri_hamar}_{file_name}{file_suffix}.docx"
    if os.path.exists(save_path):
        return

    info = row.model_dump()
    info.update(additional_info)
    doc.render(info)
    doc.save(save_path)


# alignement problem
def vkayakan():
    file_name = "vkayakan"
    doc = DocxTemplate(path_join("templates", f"{file_name}_template.docx"))

    info: Dict[int, Row] = {}
    for i in users.keys():
        for row in data:
            if row["gnord"] != i:
                continue
            if i not in info:
                info[i] = []
            info[i].append(Row(**row))


    for raw_row in data:
        row = Row(**raw_row)
        id_ = row.gnord
        if id_ not in info:
            info[id_] = []
        info[id_].append(row)


    i = 0
    for id_, contents in info.items():
        i += 1

        lot_info = []
        for row in contents:
            lot_info.append(
                (
                    row.xumb,
                    row.lot,
                    row.entalot,
                    row.meknarkayin_gin
                )
            )

        lot_info = [
            f"Խումբ {xumb} ԼՈՏ {lot} {entalot or ''} մեկնարկային գինը {gin} ՀՀ դրամ," for xumb, lot, entalot, gin in lot_info]

        context = contents[0].model_dump()
        context.update({
            "id": RichText(i, font=FONT, size=12*2, bold=True, underline=True),
            "lot_info": RichText('\n'.join(lot_info), font=FONT, size=12*2, bold=False, underline=False),
        })

        save_path = f"{file_name}_{i}.docx"
        if os.path.exists(save_path):
            continue

        doc.render(context)
        doc.save(save_path)


def run_process(args, numbers):
    processes = []
    errors = []

    grouped = {}
    for paymanagri_hamar, obj in groupby(data, lambda row: row["paymanagri_hamar"]):
        grouped[paymanagri_hamar] = list(obj)

    with ProcessPoolExecutor(max_workers=os.cpu_count() // 2) as executor:
        for index, d in enumerate(grouped, 2):
            run = True
            if args.numbers:
                run = index in numbers

            if run:
                raw_row = grouped[d][0]
                row = Row(**raw_row)
                if len(grouped[d]) == 1:
                    processes.append((index, executor.submit(ardzanagrutyun, row)))
                    processes.append((index, executor.submit(paymanagir, row)))
                else:
                    additional_info = {
                        "groups": []
                    }
                    for obj in grouped[d]:
                        obj = Row(**obj)
                        additional_info["groups"].append(
                            {
                                "xumb": obj.xumb,
                                "lot": obj.lot,
                                "entalot": obj.entalot if obj.entalot else "",
                                "guyqi_anvanum": translate(obj.guyqi_anvanum),
                                "meknarkayin_gin": Row.gin_to_str(obj.meknarkayin_gin),
                                "guyqi_arjeq": Row.gin_to_str(obj.guyqi_arjeq),
                                "guyqayin_hamar": obj.guyqayin_hamar
                            }
                        )
                    processes.append((index, executor.submit(ardzanagrutyun, obj, additional_info, "_grouped")))
                    processes.append((index, executor.submit(paymanagir, row, additional_info, "_grouped")))
        processes.append((index, executor.submit(vkayakan)))


    # with ProcessPoolExecutor(max_workers=os.cpu_count() // 2) as executor:
    #     for index, raw_row in enumerate(data, 2):
    #         run = True
    #         if args.numbers:
    #             run = index in numbers

    #         row = Row(**raw_row)

    #         if run:
    #             processes.append((index, executor.submit(ardzanagrutyun, row)))
    #             processes.append((index, executor.submit(paymanagir, row)))
    #     processes.append((index, executor.submit(vkayakan)))

    for i, thread in processes:
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

    for i, user in enumerate(users_list, 2):
        users[i] = user

    if args.numbers:
        numbers = [int(row_num) for row_num in args.numbers.split(',')]

    run_process(args, numbers) # ~44 s


if __name__ == "__main__":
    main()
