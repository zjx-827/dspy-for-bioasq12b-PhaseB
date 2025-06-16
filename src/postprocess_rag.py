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
    parser.add_argument("--data_type", type=str, default="all")
    parser.add_argument("--file_name", type=str, default="12B4_golden")
    parser.add_argument("--input_dir", type=str, default="../results/")
    parser.add_argument("--output_dir", type=str, default="../results_final/")
    args = parser.parse_args()

    json_name = f"{args.data_type}/{args.file_name}.json"
    ori_results = json.load(open(os.path.join(args.input_dir, json_name), "r", encoding="utf-8"))
    if not os.path.exists(args.output_dir): os.makedirs(args.output_dir)

    results_dict = {}
    for i, item in enumerate(ori_results):
        t1, t2 = item["type"].split("_")
        results_dict.setdefault(item["id"], {"type": t2})
        if t1 == "ideal":
            results_dict[item["id"]].setdefault("ideal_answer", item["pred"])
        else:
            if t2 in ["list", "factoid"]:
                results_dict[item["id"]].setdefault("exact_answer", get_list(item["pred"]))
            else:
                results_dict[item["id"]].setdefault("exact_answer", item["pred"])
    results_list = []
    for k, v in results_dict.items():
        if v["type"] == "summary":
            results_list.append({"id": k, "ideal_answer": v["ideal_answer"]})
        else:
            results_list.append({"id": k, "ideal_answer": v["ideal_answer"], "exact_answer": v["exact_answer"]})

    with open(os.path.join(args.output_dir, f"rag_{args.file_name}.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps({"questions": results_list}))


if __name__ == "__main__":
    main()
