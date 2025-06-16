import argparse
from utils import *
from task_instructions import TASK_INST


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, default="../data/")
    args = parser.parse_args()

    files = os.listdir(args.input_dir)

    for file in files:
        if not file.endswith(".json"): continue
        file_path = os.path.join(args.input_dir, file)
        ori_data = json.load(open(file_path, "r", encoding="utf-8"))["questions"]
        all_data = []
        type_data = {}
        snippet_dict = {}
        for item in ori_data:
            data_type = item["type"]
            snippets = [snippet["text"] for snippet in item["snippets"]]
            # ==================== "ideal"结果 ====================
            question = TASK_INST[f"ideal_{data_type}"].format_map(item)
            tmp_dict = {"id": item["id"], "type": f"ideal_{data_type}", "question": question,
                        "response": item["ideal_answer"]}
            all_data.append(tmp_dict)
            snippet_dict[question] = snippets
            type_data.setdefault(f"ideal_{data_type}", []).append(tmp_dict)
            # ==================== "exact"结果 ====================
            if data_type != "summary":
                question = TASK_INST[f"exact_{data_type}"].format_map(item)
                tmp_dict = {"id": item["id"], "type": f"exact_{data_type}", "question": question,
                            "response": item["exact_answer"]}
                all_data.append(tmp_dict)
                snippet_dict[question] = snippets
                type_data.setdefault(f"exact_{data_type}", []).append(tmp_dict)

        save_json(os.path.join(args.input_dir, "all"), file, all_data)
        save_json(os.path.join(args.input_dir, "snippet"), file, snippet_dict)
        for data_type in type_data:  save_json(os.path.join(args.input_dir, data_type), file, type_data[data_type])


if __name__ == "__main__":
    main()
