import argparse
import json
import ast
import os


def get_list(ori_str):
    result = ast.literal_eval(ori_str)
    result = [[r] for r in result]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", type=str, default="12B4_golden")
    parser.add_argument("--input_dir", type=str, default="../results/")
    parser.add_argument("--output_dir", type=str, default="../results_final/")
    args = parser.parse_args()

    t2s = ["yesno", "factoid", "list", "summary"]

    results_dict = {}
    if not os.path.exists(args.output_dir): os.makedirs(args.output_dir)

    for t2 in t2s:

        json_dir = os.path.join(args.input_dir, f"ideal_{t2}")
        ori_results = json.load(open(os.path.join(json_dir, f"{args.file_name}.json"), "r", encoding="utf-8"))
        for i, item in enumerate(ori_results):
            results_dict.setdefault(item["id"], {"type": t2})
            results_dict[item["id"]].setdefault("ideal_answer", item["pred"])
        if t2 in ["list", "factoid"]:
            json_dir = os.path.join(args.input_dir, f"exact_{t2}")
            ori_results = json.load(open(os.path.join(json_dir, f"{args.file_name}.json"), "r", encoding="utf-8"))
            for i, item in enumerate(ori_results):
                results_dict[item["id"]].setdefault("exact_answer", get_list(item["pred"]))
        elif t2 == "yesno":
            json_dir = os.path.join(args.input_dir, f"exact_{t2}")
            ori_results = json.load(open(os.path.join(json_dir, f"{args.file_name}.json"), "r", encoding="utf-8"))
            for i, item in enumerate(ori_results):
                results_dict[item["id"]].setdefault("exact_answer", item["pred"])
    results_list = []
    for k, v in results_dict.items():
        if v["type"] == "summary":
            results_list.append({"id": k, "ideal_answer": v["ideal_answer"]})
        else:
            results_list.append({"id": k, "ideal_answer": v["ideal_answer"], "exact_answer": v["exact_answer"]})

    with open(os.path.join(args.output_dir, f"heavy_opt_{args.file_name}.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps({"questions": results_list}))


if __name__ == "__main__":
    main()
