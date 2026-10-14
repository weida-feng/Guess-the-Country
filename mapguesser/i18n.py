"""English and Chinese interface strings."""

MESSAGES = {
    "en": {
        "eyebrow": "GEOGRAPHY QUIZ · 10 ROUNDS",
        "intro": "Recognize the outline. Choose the country or region. How many can you get right?",
        "how_to_play": "How to play",
        "instructions": "Choose one of four answers for each map. Each correct answer earns one point. There are ten rounds, with no repeated maps.",
        "language_hint": "Switch language anytime — your question and score stay the same.",
        "restart": "Start a new game",
        "dataset": "{count} country and region outlines",
        "completed": "Completed {count} of {total}",
        "score": "Score",
        "question": "Round {number} of {total}",
        "choose": "Which country or region is this?",
        "correct": "Correct! This is {name}.",
        "incorrect": "The correct answer is {name}.",
        "game_over": "Game complete",
        "final_score": "You scored {score} out of {total}. Ready for another round?",
        "play_again": "Play again",
        "next_question": "Next question",
    },
    "zh": {
        "eyebrow": "地理猜谜 · 十题挑战",
        "intro": "观察地图轮廓，选择对应的国家或地区。你能答对几题？",
        "how_to_play": "怎么玩",
        "instructions": "每题从四个选项中选择答案，答对得一分。一局共十题，地图不会重复。",
        "language_hint": "随时切换语言，当前题目和分数都会保留。",
        "restart": "开始新游戏",
        "dataset": "{count} 个国家和地区的地图轮廓",
        "completed": "已完成 {count} / {total} 题",
        "score": "得分",
        "question": "第 {number} / {total} 题",
        "choose": "这是哪个国家或地区？",
        "correct": "答对了！这是{name}。",
        "incorrect": "正确答案是{name}。",
        "game_over": "游戏结束",
        "final_score": "你答对了 {score} / {total} 题。再挑战一次吧！",
        "play_again": "再玩一次",
        "next_question": "下一题",
    },
}


def translate(key: str, language: str, **values: object) -> str:
    return MESSAGES[language][key].format(**values)
