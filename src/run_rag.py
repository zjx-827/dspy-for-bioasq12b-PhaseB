import argparse
import dspy
import json
import random
import os
from tqdm import tqdm

lm = dspy.LM("deepseek/deepseek-chat", api_key="",
             api_base="https://api.deepseek.com")
dspy.configure(lm=lm)


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", type=str, default="12B4_golden")
    parser.add_argument("--input_dir", type=str, default="../data/all/")
    parser.add_argument("--snippet_dir", type=str, default="../data/snippet/")
    parser.add_argument("--output_dir", type=str, default="../results/all/")
    args = parser.parse_args()

    json_name = f"{args.file_name}.json"
    testdata = json.load(open(os.path.join(args.input_dir, json_name), "r", encoding="utf-8"))
    snippet_dict = json.load(open(os.path.join(args.snippet_dir, json_name), "r", encoding="utf-8"))
    if not os.path.exists(args.output_dir): os.makedirs(args.output_dir)
    rag = RAG(snippet_dict)
    for i, item in enumerate(tqdm(testdata)):
        pred = rag(question=item["question"])
        item["pred"] = pred.response
        if i % 10 == 0:
            print("Question:", item["question"])
            print("Response:", pred)
            # with open(os.path.join(args.output_dir, json_name + "_tmp"), "w", encoding="utf-8") as f:
            #     f.write(json.dumps(testdata))
    with open(os.path.join(args.output_dir, json_name), "w", encoding="utf-8") as f:
        f.write(json.dumps(testdata))


if __name__ == "__main__":
    main()
