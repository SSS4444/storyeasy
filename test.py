# -*- coding: utf-8 -*-

from openai import OpenAI
import os
import json
import time

client = OpenAI(
    api_key="sk-RjAGV8eReTIx",
    base_url="https://api.moonshot.cn/v1",
)

#判断用户决策合理与否
def judge_action(action):
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是一个小红帽行为合理与否的检查者。用户是小红帽，traits: [善良勇敢, 好奇心强, 穿着红色斗篷, 善于交朋友, 对森林生物有爱心],小红帽是一个活泼可爱的小女孩，她以她的善良和勇气而闻名。她喜欢穿着她标志性的红色斗篷，这使她在森林中非常显眼。她对森林中的动物和植物都充满了爱心，她的任务是安全地前往奶奶的小屋，并收集一些有用的草药。她坚信家人的爱是她最大的财富。她会输入一些行为，如果符合规则，规则是这是一个童话世界，只要小红帽的行为不是非常不合理，比如杀人，这不符合小红帽善良的特点；与大灰狼肉搏成功，这不符合小红帽是个小女孩的特点。那就允许。你输出1，不合理你输出0，并且输出不合理的理由，以字符串的形式输出，输出的形式是0，理由，邀请用户重新输入决策，输出格式为字符串"},
            {"role": "user", "content": action}
        ],
        temperature=1,
    )
    return completion.choices[0].message.content

history=[]

#依据用户合理的行为生成回复
def gen_response(last_story,action):
    completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
            {"role": "system",
            "content":"小红帽故事的主要人物描述是：- 小红帽（用户扮演）：小红帽是一个活泼可爱的小女孩，她以她的善良和勇气而闻名。她喜欢穿着她标志性的红色斗篷，这使她在森林中非常显眼。她对森林中的动物和植物都充满了爱心，她的任务是安全地前往奶奶的小屋，并收集一些有用的草药。她坚信家人的爱是她最大的财富。- 大灰狼：大灰狼是森林中的一个狡猾而危险的掠食者，以其强壮的身体和狩猎技巧而闻名。他擅长伪装和设下陷阱，他的任务是寻找猎物并设下陷阱来捕捉它们。他对小红帽和她的奶奶怀有恶意，并且相信只有力量和狡猾才能在森林中生存。- 奶奶：小红帽的奶奶，生病了，住在森林那头的小屋里。奶奶是一个慈祥和智慧的老人，她以其对家庭的深厚爱和丰富的生活经验而闻名。她擅长讲故事，并且对森林中的动植物有着深刻的了解。她的任务是照顾小红帽，并传授她智慧和故事。她相信家庭和智慧是生命中最宝贵的东西。- 猎人：猎人是森林中的一位勇敢和坚定的保护者，他以其射击技巧和对森林的保护而闻名。他对动物有同情心，并且对正义有着坚定的信念。他的任务是保护森林和它的居民，追踪并对抗那些威胁到和平的生物，如大灰狼。他相信正义和保护是他的职责。"},
            {"role": "system",
             "content": "小红帽故事的地点描述帽：- 森林：一片广阔而神秘的森林，充满了各种奇妙的生物。- 奶奶的房子：一间温馨的小屋，位于森林的另一边。"},
            {"role": "system",
            "content": f"###你应该保留的记忆情节是：{last_story}。"},
            {"role": "system",
             "content": "你正在参与一个互动式童话故事创作，你扮演一个和用户一起讲小红帽故事的主持人，用户扮演小红帽，你要根据用户输入的行为以及童话世界的法则来生成相应的回复，然后邀请引导用户接着做出决策"},
            {"role": "user", "content": action}
            ],
            temperature=0.5,
        )

    ans = completion.choices[0].message.content
    history.append({"role": "user", "content": action})
    history.append({"role": "assistant", "content": ans})
    return ans

#记录总结故事情节
def gen_easy_story(h_history):
    history_json = json.dumps(h_history)
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你要根据这个对话总结出故事情节，要求，简单，最大限度保留故事情节，以字符串形式输出"},
            {"role": "user", "content": history_json},
        ],
        temperature=1,
    )
    return completion.choices[0].message.content

print("欢迎来到小红帽的奇幻森林冒险！🌳🐺🧸\n你好，勇敢的冒险者！在这个由经典童话改编的交互式故事中，你将扮演我们的主角——小红帽。穿上你那件鲜艳的红色斗篷，准备好踏上一段充满奇遇和惊喜的旅程吧。\n🏡 你的起点是你家——一个温馨的小屋，坐落在村庄的边缘。你的奶奶独自一人住在森林的另一边，她今天邀请你过去共度一个愉快的下午。\n🌲 森林里充满了未知，有美丽的风景，也有潜在的危险。你会遇到各种各样的森林居民，包括友好的动物们和一些不那么友好的角色。\n📜 你的任务是安全地穿过森林，到达奶奶的家，同时收集一些有用的草药，也许还能发现一些隐藏的秘密。\n🎒 记得，作为小红帽，你拥有善良、勇敢、好奇心强等特质，你将用这些特质来解决途中遇到的难题。\n现在，请告诉我，你的第一个决定是什么？是直接走向森林，还是先准备一些旅途中可能需要的物品？或者是其他的什么。输入你的选择，让我们的故事开始吧！\n请输入你想做什么：")
n = 0



while True:
    last_story_description=''
    n+=1
    if n > 1 :
        last_story_description = current_story_description
    use_action = input()
    ans_judge_action = judge_action(use_action)
    while (ans_judge_action[0] == '0'):
        use_action = input(ans_judge_action[2:])
        ans_judge_action = judge_action(use_action)
    response = gen_response(last_story_description,use_action)
    print(response)
    time.sleep(60)

    current_story_description = gen_easy_story(history)