import argparse
import dspy
import json
import random
import os
from tqdm import tqdm
from utils import save_json
from dspy.evaluate import SemanticF1

lm = dspy.LM("deepseek/deepseek-chat", api_key="",
             api_base="https://api.deepseek.com")
dspy.configure(lm=lm)


def get_answer(data_type, ori_answer):
    if "ideal" in data_type:
        return ori_answer[0]
    elif data_type == "exact_factoid":
        return str(ori_answer)
    elif data_type == "exact_list":
        return str([s[0] for s in ori_answer])
    else:
        return ori_answer


def build_examples(data, dev_rate=0.1):
    data = [dspy.Example(**d).with_inputs("question") for d in data]
    random.Random(0).shuffle(data)
    split_point = int(len(data) * (1 - dev_rate))
    trainset, devset = data[:split_point], data[split_point:]
    len(trainset), len(devset)
    return trainset, devset


class RAG(dspy.Module):
    def __init__(self, search_dict):
        super(RAG, self).__init__()
        self.respond = dspy.ChainOfThought("context, question -> response")
        self.search_dict = search_dict

    def search(self, question):
        return self.search_dict.get(question, [])

    def forward(self, question):
        context = self.search(question)
        return self.respond(context=context, question=question)


def test():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_type", type=str, default="exact_yesno")
    parser.add_argument("--file_name", type=str, default="12B1_golden")
    parser.add_argument("--input_dir", type=str, default="../data/")
    parser.add_argument("--snippet_dir", type=str, default="../data/snippet/")
    parser.add_argument("--model_dir", type=str, default="../models/")
    parser.add_argument("--output_dir", type=str, default="../results/")
    args = parser.parse_args()

    json_dir = str(os.path.join(args.input_dir, args.data_type))
    json_name = f"{args.file_name}.json"
    testdata = json.load(open(os.path.join(json_dir, json_name), "r", encoding="utf-8"))
    snippet_dict = json.load(open(os.path.join(args.snippet_dir, f"{args.file_name}.json"), "r", encoding="utf-8"))
    if not os.path.exists(args.output_dir): os.makedirs(args.output_dir)

    rag = RAG(snippet_dict)
    rag.load(os.path.join(args.model_dir, f"heavy_{args.data_type}_optimized_rag.json"))
    for i, item in enumerate(tqdm(testdata)):
        pred = rag(question=item["question"])
        item["pred"] = pred.response
        if i % 10 == 0:
            print("Question:", item["question"])
            print("Response:", pred)
            # with open(os.path.join(args.output_dir, json_name + "_tmp"), "w", encoding="utf-8") as f:
            #     f.write(json.dumps(testdata))
    json_dir = str(os.path.join(args.output_dir, args.data_type))
    save_json(json_dir, json_name, "heavy_" + testdata)


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_type", type=str, default="exact_yesno")
    parser.add_argument("--file_name", type=str, default="training12b_new")
    parser.add_argument("--input_dir", type=str, default="../data/")
    parser.add_argument("--snippet_dir", type=str, default="../data/snippet/")
    parser.add_argument("--model_dir", type=str, default="../models/")
    args = parser.parse_args()

    json_name = f"{args.data_type}/{args.file_name}.json"
    train_data = json.load(open(os.path.join(args.input_dir, json_name), "r", encoding="utf-8"))
    for item in train_data:
        item["response"] = get_answer(item["type"], item["response"])
        # print(item["response"])
    trainset, devset = build_examples(train_data, dev_rate=0.1)
    print(trainset[0])
    metric = SemanticF1(decompositional=True)
    snippet_dict = json.load(open(os.path.join(args.snippet_dir, f"{args.file_name}.json"), "r", encoding="utf-8"))

    tp = dspy.MIPROv2(metric=metric, auto="heavy", num_threads=24)
    optimized_rag = tp.compile(RAG(snippet_dict), trainset=trainset, max_bootstrapped_demos=2, max_labeled_demos=2,
                               requires_permission_to_run=False)
    optimized_rag.save(os.path.join(args.model_dir, f"heavy_{args.data_type}_optimized_rag.json"))


if __name__ == "__main__":
    train()
    # test()
