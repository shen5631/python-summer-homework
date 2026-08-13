"""일본 여행지 추천 프로그램.

사용자가 원하는 활동을 선택하면, 그 활동에 맞는 일본 지역과 관광지를 추천해주는 프로그램입니다.
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk

try:
    from PIL import Image, ImageDraw, ImageFont, ImageTk
except ModuleNotFoundError:
    Image = None
    ImageDraw = None
    ImageFont = None
    ImageTk = None

REGION_RECOMMENDATIONS = {
    "홋카이도": {
        "summary": "눈과 겨울 스포츠, 자연 풍경이 매력적인 북부 지역입니다.",
        "image": "images/hokkaido.jpg",
        "places": [
            "니세코: 스키와 눈 풍경을 즐길 수 있는 인기 겨울 리조트",
            "후라노: 라벤더 밭과 들판 풍경이 아름다운 곳",
            "시레토코: 자연 보호 구역으로 트레킹과 풍경 감상이 좋음",
            "오타루: 겨울 야경과 항구 분위기가 인상적인 도시",
        ],
        "activities": {
            "스키/눈": ["니세코", "후라노"],
            "온천/휴식": ["오타루", "시레토코"],
            "자연/풍경": ["시레토코", "후라노"],
            "도시/먹거리": ["오타루"],
        },
    },
    "도호쿠": {
        "summary": "산, 온천, 시골 분위기와 문화 체험이 잘 어울리는 지역입니다.",
        "image": "images/tohoku.jpg",
        "places": [
            "아오모리: 네부타마와 사시미로 유명한 북쪽 도시",
            "센다이: 음식과 도시 분위기가 무난하게 즐기기 좋은 곳",
            "기누가와 온천: 온천과 전통 휴식이 가능한 곳",
            "하치노헤: 자연과 온천을 함께 즐기기 좋은 지역",
        ],
        "activities": {
            "온천/휴식": ["기누가와 온천", "하치노헤"],
            "자연/풍경": ["하치노헤", "아오모리"],
            "도시/먹거리": ["센다이"],
            "문화/역사": ["아오모리"],
        },
    },
    "간토": {
        "summary": "도시 관광, 먹거리, 쇼핑, 야경을 함께 즐길 수 있는 지역입니다.",
        "image": "images/kanto.jpg",
        "places": [
            "도쿄: 타워, 신주쿠, 오다이바 등 도시 체험의 핵심",
            "하코네: 온천과 산 풍경이 조화로운 휴식지",
            "닛코: 숲과 사원, 역사적인 분위기",
            "카마쿠라: 해안 풍경과 큰 부처상 관광지",
        ],
        "activities": {
            "도시/쇼핑": ["도쿄"],
            "온천/휴식": ["하코네"],
            "자연/풍경": ["닛코"],
            "해변/산책": ["카마쿠라"],
        },
    },
    "간사이": {
        "summary": "전통과 현대가 함께 있는 일본의 대표적인 관광 지역입니다.",
        "image": "images/kansai.jpg",
        "places": [
            "교토: 사원, 정원, 전통 거리와 기모노 문화",
            "오사카: 먹거리와 신나는 야경, 쇼핑이 강점",
            "나라: 고대 건축과 사슴이 매력적인 도시",
            "기노사키 온천: 고요한 온천 휴식과 전통 분위기",
        ],
        "activities": {
            "문화/역사": ["교토", "나라"],
            "먹거리/도시": ["오사카"],
            "온천/휴식": ["기노사키 온천"],
            "사진/산책": ["교토"],
        },
    },
    "규슈": {
        "summary": "따뜻한 기후와 바다, 온천, 음식이 강점인 남부 지역입니다.",
        "image": "images/kyushu.jpg",
        "places": [
            "후쿠오카: 야시장과 현대적인 도시 분위기",
            "벳푸: 대표 온천 도시로 몸과 마음을 힐링",
            "아소: 활화산과 자연 풍경이 멋진 곳",
            "가고시마: 해안과 화산이 어우러진 매력적인 도시",
        ],
        "activities": {
            "온천/휴식": ["벳푸"],
            "먹거리/도시": ["후쿠오카"],
            "자연/풍경": ["아소", "가고시마"],
            "바다/해변": ["가고시마"],
        },
    },
    "오키나와": {
        "summary": "맑은 바다와 열대 분위기, 해변 활동이 매력적인 지역입니다.",
        "image": "images/okinawa.jpg",
        "places": [
            "나하: 도시 문화와 바다를 함께 즐길 수 있는 곳",
            "케라마 제도: 맑고 얕은 바다에서 수영과 스노클링",
            "모토부: 해변과 휴식이 잘 어울리는 곳",
            "이시가키: 아름다운 바다와 자연 풍경",
        ],
        "activities": {
            "바다/해변": ["케라마 제도", "모토부"],
            "수영/스노클링": ["케라마 제도"],
            "휴식/바캉스": ["나하", "이시가키"],
            "자연/풍경": ["이시가키"],
        },
    },
}

ACTIVITY_KEYWORDS = {
    "스키/눈": ["스키", "눈", "겨울", "snow", "ski", "winter"],
    "온천/휴식": ["온천", "휴식", "힐링", "온수", "onsen", "relax"],
    "자연/풍경": ["자연", "풍경", "산", "강", "forest", "nature", "lake"],
    "도시/쇼핑": ["도시", "쇼핑", "먹거리", "야경", "city", "shopping", "food"],
    "문화/역사": ["문화", "역사", "사원", "고전", "history", "temple", "culture"],
    "바다/해변": ["바다", "해변", "바캉스", "해안", "beach", "sea", "ocean"],
    "수영/스노클링": ["수영", "스노클링", "물놀이", "snorkel", "swim"],
    "사진/산책": ["사진", "산책", "거리", "walk", "photo"],
}


def get_region_summary() -> str:
    lines = []
    for region, info in REGION_RECOMMENDATIONS.items():
        places = ", ".join(info["places"])[:120]
        lines.append(f"{region}: {places}...")
    return "\n".join(lines)


def get_activity_recommendation(activity: str) -> str:
    """활동 이름을 받아 가장 잘 맞는 일본 지역과 관광지를 추천한다."""
    text = activity.strip().lower()

    for key, keywords in ACTIVITY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            best_region = None
            match_places = []
            for region, info in REGION_RECOMMENDATIONS.items():
                if key in info["activities"]:
                    match_places.extend(info["activities"][key])
                    if best_region is None:
                        best_region = region
            if best_region:
                return f"추천 활동: {key}\n추천 지역: {best_region}\n추천 장소: {', '.join(match_places)[:200]}"

    return "추천 활동: 도시/쇼핑\n추천 지역: 간토\n추천 장소: 도쿄, 하코네"


def get_recommendations(region: str) -> str:
    """지역 선택에 따른 관광지와 놀거리를 추천해 문자열로 반환."""
    region_name = region.strip()
    if region_name in REGION_RECOMMENDATIONS:
        info = REGION_RECOMMENDATIONS[region_name]
        places = "\n- ".join(info["places"])
        return f"추천 지역: {region_name}\n설명: {info['summary']}\n대표 관광지/놀거리:\n- {places}"

    normalized = region_name.lower()
    if "홋카이" in normalized or "hokkaido" in normalized:
        info = REGION_RECOMMENDATIONS["홋카이도"]
    elif "도호쿠" in normalized or "tohoku" in normalized:
        info = REGION_RECOMMENDATIONS["도호쿠"]
    elif "간토" in normalized or "kanto" in normalized:
        info = REGION_RECOMMENDATIONS["간토"]
    elif "간사이" in normalized or "kansai" in normalized:
        info = REGION_RECOMMENDATIONS["간사이"]
    elif "규슈" in normalized or "kyushu" in normalized:
        info = REGION_RECOMMENDATIONS["규슈"]
    elif "오키나와" in normalized or "okinawa" in normalized:
        info = REGION_RECOMMENDATIONS["오키나와"]
    else:
        info = REGION_RECOMMENDATIONS["간사이"]

    places = "\n- ".join(info["places"])
    return f"추천 지역: {next(key for key, value in REGION_RECOMMENDATIONS.items() if value == info)}\n설명: {info['summary']}\n대표 관광지/놀거리:\n- {places}"


def ensure_region_image(region_name: str, path: str) -> str:
    directory = os.path.join(os.path.dirname(__file__), "images")
    os.makedirs(directory, exist_ok=True)
    full_path = os.path.join(directory, os.path.basename(path))

    if os.path.exists(full_path):
        return full_path

    if Image is None:
        return path

    width, height = 320, 220
    image = Image.new("RGB", (width, height), color=(245, 235, 226))
    draw = ImageDraw.Draw(image)

    palette = {
        "홋카이도": (127, 166, 213),
        "도호쿠": (135, 188, 120),
        "간토": (217, 163, 106),
        "간사이": (193, 113, 103),
        "규슈": (198, 92, 92),
        "오키나와": (110, 187, 175),
    }
    color = palette.get(region_name, (180, 170, 160))

    draw.rectangle((0, 100, width, height), fill=(color[0], color[1], color[2]))
    draw.polygon([(0, 140), (120, 60), (260, 140), (220, 180), (70, 180)], fill=(255, 233, 150))
    draw.polygon([(60, 150), (130, 110), (195, 150), (175, 180), (90, 180)], fill=(105, 150, 120))
    draw.rectangle((0, 160, width, height), fill=(122, 158, 187))

    try:
        font = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 20)
    except OSError:
        font = ImageFont.load_default()

    draw.text((20, 18), region_name, fill=(255, 255, 255), font=font)
    image.save(full_path)
    return full_path


def load_image(path: str, size=(420, 240)):
    if Image is None or ImageTk is None:
        return None
    if not os.path.exists(path):
        return None
    try:
        image = Image.open(path)
        image = image.copy()
        original_w, original_h = image.size
        target_w, target_h = size

        scale = max(target_w / original_w, target_h / original_h)
        resized_w = max(1, int(original_w * scale))
        resized_h = max(1, int(original_h * scale))
        resized = image.resize((resized_w, resized_h), Image.LANCZOS)

        canvas = Image.new("RGB", size, color=(255, 255, 255))
        left = (target_w - resized_w) // 2
        top = (target_h - resized_h) // 2
        canvas.paste(resized, (left, top))
        return ImageTk.PhotoImage(canvas)
    except Exception:
        return None


def run_gui() -> None:
    root = tk.Tk()
    root.title("일본 여행 추천")
    root.geometry("1100x760")
    root.minsize(980, 680)
    root.resizable(True, True)

    bg = "#f7efe7"
    accent = "#c8433a"
    deep = "#2d2a2a"
    soft = "#fffaf5"

    root.configure(bg=bg)

    header = tk.Frame(root, bg=accent, height=110)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="日本 여행 추천",
        font=("Malgun Gothic", 24, "bold"),
        bg=accent,
        fg="white",
        anchor="w",
        padx=26,
        pady=18,
    )
    title.pack(anchor="w")

    subtitle = tk.Label(
        header,
        text="당신의 취향에 맞는 일본 여행지를 골라드립니다",
        font=("Malgun Gothic", 10),
        bg=accent,
        fg="#fff1ee",
        anchor="w",
        padx=26,
    )
    subtitle.pack(anchor="w", pady=(0, 18))

    main_frame = tk.Frame(root, bg=bg, padx=24, pady=18)
    main_frame.pack(fill="both", expand=True)

    left_panel = tk.Frame(main_frame, bg=bg)
    left_panel.pack(side="left", fill="y")

    card_left = tk.Frame(left_panel, bg=soft, bd=1, relief="solid", padx=18, pady=16, width=300)
    card_left.pack(fill="y", padx=(0, 16))

    tk.Label(card_left, text="여행 스타일 선택", bg=soft, fg=deep, font=("Malgun Gothic", 12, "bold")).pack(anchor="w", pady=(0, 10))

    activity_var = tk.StringVar(value="온천/휴식")
    activity_combo = ttk.Combobox(card_left, textvariable=activity_var, state="readonly", width=28)
    activity_combo["values"] = [
        "온천/휴식",
        "스키/눈",
        "자연/풍경",
        "도시/쇼핑",
        "문화/역사",
        "바다/해변",
        "수영/스노클링",
        "사진/산책",
    ]
    activity_combo.pack(anchor="w", pady=(0, 12))

    tk.Label(card_left, text="지역 선택", bg=soft, fg=deep, font=("Malgun Gothic", 12, "bold")).pack(anchor="w", pady=(0, 10))
    region_var = tk.StringVar(value="간사이")
    region_combo = ttk.Combobox(card_left, textvariable=region_var, state="readonly", width=28)
    region_combo["values"] = ["홋카이도", "도호쿠", "간토", "간사이", "규슈", "오키나와"]
    region_combo.pack(anchor="w", pady=(0, 16))

    def update_image_for_region(selected_region: str) -> None:
        info = REGION_RECOMMENDATIONS.get(selected_region, REGION_RECOMMENDATIONS["간사이"])
        image_path = info.get("image", "")
        real_path = ensure_region_image(selected_region, image_path)
        photo = load_image(real_path)
        if photo is not None:
            image_label.configure(image=photo)
            image_label.image = photo
        else:
            image_label.configure(image="")
            image_label.image = None

    def handle_recommend() -> None:
        activity = activity_var.get()
        region = region_var.get()
        activity_result = get_activity_recommendation(activity)
        region_result = get_recommendations(region)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"{activity_result}\n\n{region_result}")
        update_image_for_region(region)

    recommend_button = tk.Button(
        card_left,
        text="추천 받기",
        bg=accent,
        fg="white",
        font=("Malgun Gothic", 10, "bold"),
        bd=0,
        padx=28,
        pady=10,
        command=handle_recommend,
    )
    recommend_button.pack(anchor="w")

    image_frame = tk.Frame(main_frame, bg=bg)
    image_frame.pack(side="left", fill="both", expand=True)

    image_label = tk.Label(image_frame, bg="#f0e2d5", width=40, height=18, compound="center")
    image_label.pack(fill="both", expand=True, pady=(0, 12))
    image_label.configure(anchor="center")
    update_image_for_region("간사이")

    result_panel = tk.Frame(image_frame, bg=soft, bd=1, relief="solid", padx=18, pady=16)
    result_panel.pack(fill="x")

    tk.Label(result_panel, text="추천 결과", bg=soft, fg=deep, font=("Malgun Gothic", 13, "bold")).pack(anchor="w")
    result_text = tk.Text(result_panel, width=58, height=11, wrap="word", font=("Malgun Gothic", 10), bg="#fffdfb", fg=deep, bd=0, relief="flat")
    result_text.pack(fill="both", expand=True, pady=(12, 0))
    result_text.insert(tk.END, "여행 스타일을 선택하고 추천 받기 버튼을 눌러 주세요.\n\n예시:\n- 온천/휴식\n- 스키/눈\n- 바다/해변")

    region_combo.bind("<<ComboboxSelected>>", lambda event: update_image_for_region(region_var.get()))

    root.mainloop()


if __name__ == "__main__":
    run_gui()
