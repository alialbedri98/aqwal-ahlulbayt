"""
ينشر تلقائياً قولاً واحداً من ملف quotes.csv على انستغرام
عبر Instagram Graph API. يشتغل من داخل GitHub Actions.

المتغيرات المطلوبة (تُقرأ من GitHub Secrets):
  IG_USER_ID       -> رقم حساب انستا Business (Instagram Business Account ID)
  IG_ACCESS_TOKEN  -> Long-Lived Page Access Token
  GH_PAGES_BASE    -> رابط GitHub Pages لمستودعك، مثال:
                       https://username.github.io/repo-name
  ORDER            -> 1 أو 2 أو 3 (أي قول باليوم ينشر الآن)
"""

import os
import csv
import sys
import datetime
import requests

GRAPH_URL = "https://graph.facebook.com/v19.0"


def get_today_day_number(total_days=30):
    """يحدد رقم اليوم (1-30) بناءً على يوم الشهر الحالي، ويدور تلقائياً كل شهر."""
    day_of_month = datetime.date.today().day  # 1..31
    return ((day_of_month - 1) % total_days) + 1


def load_quote(day, order):
    with open("quotes.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["اليوم"]) == day and int(row["الترتيب"]) == order:
                return row["القول"], row["القائل"]
    return None, None


def build_caption(quote, narrator):
    return (
        f"{quote}\n"
        f"- {narrator}\n\n"
        f"#اهل_البيت #حكم_ومواعظ #الامام_علي #اقوال_دينية"
    )


def post_to_instagram(image_url, caption, ig_user_id, access_token):
    # 1) إنشاء container للصورة
    create_resp = requests.post(
        f"{GRAPH_URL}/{ig_user_id}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token,
        },
        timeout=30,
    )
    create_resp.raise_for_status()
    creation_id = create_resp.json()["id"]

    # 2) نشر الـ container
    publish_resp = requests.post(
        f"{GRAPH_URL}/{ig_user_id}/media_publish",
        data={
            "creation_id": creation_id,
            "access_token": access_token,
        },
        timeout=30,
    )
    publish_resp.raise_for_status()
    return publish_resp.json()


def main():
    ig_user_id = os.environ["IG_USER_ID"]
    access_token = os.environ["IG_ACCESS_TOKEN"]
    gh_pages_base = os.environ["GH_PAGES_BASE"].rstrip("/")
    order = int(os.environ.get("ORDER", "1"))

    day = get_today_day_number(total_days=30)
    quote, narrator = load_quote(day, order)

    if quote is None:
        print(f"لم يتم العثور على قول لليوم {day} بالترتيب {order}")
        sys.exit(1)

    image_url = f"{gh_pages_base}/day{day:02d}_{order}.jpg"
    caption = build_caption(quote, narrator)

    print(f"اليوم {day} - القول {order}")
    print(f"رابط الصورة: {image_url}")
    print(f"النص المرافق:\n{caption}")

    result = post_to_instagram(image_url, caption, ig_user_id, access_token)
    print("تم النشر بنجاح:", result)


if __name__ == "__main__":
    main()
