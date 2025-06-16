TASK_INST = {
    "exact_yesno": "Answer the following yes/no question with a single word: 'yes' or 'no'. Do not provide any additional explanation or text.\n\n"
                   "##Question:Is the protein Papilin secreted?\n##Answer:yes\n\n"
                   "##Question:{body}\n##Answer:",
    "exact_factoid": "Answer the following factoid question with a concise list of up to 5 entities, ranked by confidence (highest first). Format as a JSON-style list without explanations.\n\n"
                     "##Question:What is usually the age of diagnosis in Duchenne muscular dystrophy?\n##Answer:[\"4.43 years old\", \"4.9 years old\", \"between 3 and 11 years of age\", \"4.9 years\", \"3 - 5 years\"]\n\n"
                     "##Question:{body}\n##Answer:",
    "exact_list": "Answer the following list question with a concise JSON-style list of relevant entities. Do not provide explanations or additional text.\n\n"
                  "##Question:Hepcidin is a key regulator of what processes?\n##Answer:[\"iron homeostasis\", \"inflammation\", \"anemia\", \"hypoxia\", \"bone morphogenetic protein signaling pathway\"]\n\n"
                  "##Question:{body}\n##Answer:",
    "ideal_yesno": "Answer the following question concisely and directly.\n\n"
                   "##Question:Is the protein Papilin secreted?\n##Answer:Yes, papilin is a secreted protein\n\n"
                   "##Question:{body}\n##Answer:",
    "ideal_factoid": "Answer the following question concisely and directly.\n\n"
                     "##Question:What is usually the age of diagnosis in Duchenne muscular dystrophy?\n##Answer:The usual age of diagnosis in Duchenne muscular dystrophy is around 4.9 years.\n\n"
                     "##Question:{body}\n##Answer:",
    "ideal_list": "Answer the following question concisely and directly.\n\n"
                  "##Question:Hepcidin is a key regulator of what processes?\n##Answer:Hepcidin is a key regulator of systemic iron homeostasis.\n\n"
                  "##Question:{body}\n##Answer:",
    "ideal_summary": "Answer the following question concisely and directly.\n\n"
                     "##Question: What does Cal-light do?\n##Answer: Cal-Light, that translates neuronal-activity-mediated calcium signaling into gene expression in a light-dependent manner\n\n"
                     "##Question: {body}\n##Answer:",
}

"""
[1]
根据如下问题(query)、期望输出及相应的结果评判准则，为"yesno"类问题编写**简短**且**通用**的**英文**大模型提示，引导大模型以正确的格式输出答案。
输入示例：
"query": "Is the protein Papilin secreted?", 
"answer": "yes", 
"query_type": "yesno", 
结果评判准则：对于每个是/否问题，每个参与系统的"确切"答案必须是"是"或"否"。该回答将与BIOASQ生物医学专家团队为该问题关联的黄金"确切"答案（同样是"是"或"否"）进行比较。

[2]
根据如下问题(query)、期望输出及相应的结果评判准则，为"factoid"类问题编写**简短**且**通用**的**英文**大模型提示，引导大模型以正确的格式输出答案。
输入示例：
"query": "What is usually the age of diagnosis in Duchenne muscular dystrophy?", 
"answer": ["4.43 years old", "4.9 years old", "between 3 and 11 years of age", "4.9 years", "3 - 5 years"], 
"query_type": "factoid", 
结果评判准则：对于每个事实类问题，每个参赛系统必须返回最多5个实体名称的列表，按置信度从高到低排序。

[3]
根据如下问题(query)、期望输出及相应的结果评判准则，为"list"类问题编写**简短**且**通用**的**英文**大模型提示，引导大模型以正确的格式输出答案。
"query": "Hepcidin is a key regulator of what processes?", 
"answer": [["iron homeostasis", "iron metabolism", "iron transport"], ["inflammation"], ["anemia"], ["hypoxia"], ["bone morphogenetic protein signaling pathway"]], 
"query_type": "list", 
结果评判准则：对于每个列表问题，每个参与的系统都必须返回一个实体名称列表，这些名称共同构成一个答案（例如，某种疾病的常见症状）；出于实际考虑，每个返回列表的最大允许大小可能会受到限制（例如，最多100个名称，每个名称最多100个字符）。

[4]
根据如下问题(query)、期望输出及相应的结果评判准则，为"yesno"类问题编写**简短**且**通用**的**英文**大模型提示，引导大模型以正确的格式输出答案。
输入示例：
"query": "Is the protein Papilin secreted?", 
"answer": "Yes,  papilin is a secreted protein", 
"query_type": "yesno", 
结果评判准则：使用ROUGE自动进行评估。大致来说，ROUGE会计算自动构建的答案与一组由人工构建的参考（标准）摘要Refs之间的重叠部分。

[5]
根据如下问题(query)、期望输出及相应的结果评判准则，为"factoid"类问题编写**简短**且**通用**的**英文**大模型提示，引导大模型以正确的格式输出答案。
输入示例：
"query": "What is usually the age of diagnosis in Duchenne muscular dystrophy?", 
"answer": "The usual age of diagnosis in Duchenne muscular dystrophy is around 4.9 years.", 
"query_type": "factoid", 
结果评判准则：使用ROUGE自动进行评估。大致来说，ROUGE会计算自动构建的答案与一组由人工构建的参考（标准）摘要Refs之间的重叠部分。

[6]
根据如下问题(query)、期望输出及相应的结果评判准则，为问题编写**简短**且**通用**的**英文**大模型提示，引导大模型以正确的格式输出答案。
"query": "Hepcidin is a key regulator of what processes?", 
"answer": "Hepcidin is a key regulator of systemic iron homeostasis.", 
结果评判准则：使用ROUGE自动进行评估。大致来说，ROUGE会计算自动构建的答案与一组由人工构建的参考（标准）摘要Refs之间的重叠部分。

[7]
根据如下问题(query)、期望输出及相应的结果评判准则，为"summary"类问题编写**简短**且**通用**的**英文**大模型提示，引导大模型以正确的格式输出答案。
"query": "What does Cal-light do?",
"answer": "Cal-Light, that translates neuronal-activity-mediated calcium signaling into gene expression in a light-dependent manner",
"query_type": "summary",
结果评判准则：使用ROUGE自动进行评估。大致来说，ROUGE会计算自动构建的答案与一组由人工构建的参考（标准）摘要Refs之间的重叠部分。
"""
