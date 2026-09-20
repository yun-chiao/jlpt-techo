#!/usr/bin/env python3
"""
日檢手帖 Threads 自動發送器・解答回覆器・Token 續期與成效週報 (publish.py)

特點：
1. 無狀態冪等防重（Idempotent）：發文前自動查詢帳號最近貼文，若當日該專欄已發布則自動跳過，
   絕不重複發文，也不需每天 commit 狀態回 git 造成衝突。
2. 同串自動公布解答：出題 3 小時後自動定位當日題目貼文 ID，在同串底下回覆【解答公布】（走 1,000 則/日回覆額度）。
3. 佇列優先＋即時兜底：優先讀取 content/threads-queue/YYYY-Www.json（保留人工改稿），
   若佇列檔不存在則即時接地生成，永不斷更。

環境變數（GitHub Actions Secrets）：
  THREADS_USER_ID       Threads 使用者 ID
  THREADS_ACCESS_TOKEN  Threads 60 天長期 Access Token
  DRY_RUN               設為 "1" 時只印出內容不實際呼叫 API
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from generate_week import (
  QUEUE_DIR,
  REPO_ROOT,
  SLOT_HEADERS,
  TAIPEI_TZ,
  generate_day_posts,
  load_all_data,
)

GRAPH_BASE = "https://graph.threads.net/v1.0"


def get_post_for_date_and_slot(date_obj: dt.date, slot: str) -> dict[str, Any]:
  """優先從已生成的週佇列讀取（若你有手動編輯過 JSON 會保留修改），找不到則即時生成。"""
  iso_year, iso_week, _ = date_obj.isocalendar()
  week_file = QUEUE_DIR / f"{iso_year}-W{iso_week:02d}.json"
  if week_file.exists():
    with open(week_file, encoding="utf-8") as f:
      q = json.load(f)
    for post in q.get("posts", []):
      if post.get("date") == date_obj.isoformat() and post.get("slot") == slot:
        return post

  data = load_all_data()
  for post in generate_day_posts(date_obj, data, api_key=os.environ.get("GEMINI_API_KEY")):
    if post["slot"] == slot:
      return post
  raise KeyError(f"找不到 slot={slot} ({date_obj.isoformat()})")


def http_json(url: str, method: str = "GET", params: dict[str, str] | None = None) -> dict[str, Any]:
  if method == "GET" and params:
    url = f"{url}?{urllib.parse.urlencode(params)}"
    data_bytes = None
  elif params:
    data_bytes = urllib.parse.urlencode(params).encode("utf-8")
  else:
    data_bytes = None

  req = urllib.request.Request(url, data=data_bytes, method=method)
  for attempt in range(3):
    try:
      with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
      err_body = exc.read().decode("utf-8", errors="replace")
      if exc.code == 429 and attempt < 2:
        wait_s = 15 * (attempt + 1)
        print(f"  [429 rate limit] 等待 {wait_s}s 後重試...", file=sys.stderr)
        time.sleep(wait_s)
        continue
      raise RuntimeError(f"Threads API HTTP {exc.code}: {err_body}") from exc


def list_recent_threads(user_id: str, token: str, limit: int = 20) -> list[dict[str, Any]]:
  resp = http_json(
    f"{GRAPH_BASE}/{user_id}/threads",
    method="GET",
    params={
      "fields": "id,text,timestamp",
      "limit": str(limit),
      "access_token": token,
    },
  )
  return resp.get("data", [])


def find_today_post_by_prefix(
  recent: list[dict[str, Any]],
  date_obj: dt.date,
  header_prefix: str,
) -> dict[str, Any] | None:
  for item in recent:
    text = item.get("text", "")
    ts = item.get("timestamp", "")
    if not text.startswith(header_prefix):
      continue
    if ts:
      try:
        dt_utc = dt.datetime.fromisoformat(ts.replace("+0000", "+00:00"))
        dt_tpe = dt_utc.astimezone(TAIPEI_TZ)
        if dt_tpe.date() == date_obj:
          return item
      except Exception:
        pass
  return None


def has_answer_reply(media_id: str, token: str) -> bool:
  resp = http_json(
    f"{GRAPH_BASE}/{media_id}/replies",
    method="GET",
    params={
      "fields": "id,text",
      "access_token": token,
    },
  )
  for rep in resp.get("data", []):
    if rep.get("text", "").startswith("【解答公布】"):
      return True
  return False


def publish_threads_text(
  user_id: str,
  token: str,
  text: str,
  reply_to_id: str | None = None,
) -> str:
  """兩步驟發布 Threads 貼文（或同串回覆），回傳發布後的 media_id。"""
  create_params: dict[str, str] = {
    "media_type": "TEXT",
    "text": text,
    "access_token": token,
  }
  if reply_to_id:
    create_params["reply_to_id"] = reply_to_id

  container = http_json(f"{GRAPH_BASE}/{user_id}/threads", method="POST", params=create_params)
  creation_id = container["id"]
  # 等待容器就緒後發布
  time.sleep(3)
  published = http_json(
    f"{GRAPH_BASE}/{user_id}/threads_publish",
    method="POST",
    params={
      "creation_id": creation_id,
      "access_token": token,
    },
  )
  return published["id"]


def resolve_credentials() -> tuple[str, str]:
  """取得 (user_id, token)。若未設定 THREADS_USER_ID，自動用 token 呼叫 /v1.0/me 查詢。"""
  token = os.environ.get("THREADS_ACCESS_TOKEN", "").strip()
  if not token:
    raise RuntimeError("缺少 THREADS_ACCESS_TOKEN 環境變數（請至 GitHub Settings -> Secrets and variables -> Actions 新增）。")
  user_id = os.environ.get("THREADS_USER_ID", "").strip()
  if not user_id:
    me = http_json(
      f"{GRAPH_BASE}/me",
      method="GET",
      params={"fields": "id,username", "access_token": token},
    )
    user_id = str(me["id"])
    print(f"ℹ️ 已透過 /v1.0/me 自動取得 THREADS_USER_ID = {user_id} (@{me.get('username', '')})")
  return user_id, token


def run_publish_slot(date_obj: dt.date, slot: str, dry_run: bool) -> None:
  post = get_post_for_date_and_slot(date_obj, slot)
  text = post["text"]
  header_line = text.splitlines()[0]

  print(f"=== [{date_obj.isoformat()} {post['scheduled_time']}] 發送時段：{slot} ({post['topic']}) ===")
  print(text)
  print(f"--- 字數：{len(text)} / 500 ---\n")

  if dry_run:
    print("🟡 [DRY_RUN] 乾跑模式：未實際呼叫 Threads API。")
    return

  user_id, token = resolve_credentials()

  recent = list_recent_threads(user_id, token, limit=20)
  existing = find_today_post_by_prefix(recent, date_obj, header_line)
  if existing:
    print(f"⏭️ 今日已發過此專欄（media_id={existing['id']}），自動跳過防重。")
    return

  media_id = publish_threads_text(user_id, token, text)
  print(f"✅ 發布成功！media_id = {media_id}")


def run_reply_quiz(date_obj: dt.date, slot: str, dry_run: bool) -> None:
  post = get_post_for_date_and_slot(date_obj, slot)
  reply_text = post.get("reply_text")
  if not reply_text:
    print(f"[{slot}] 無解答回覆內容，略過。")
    return

  header_line = post["text"].splitlines()[0]
  print(f"=== [{date_obj.isoformat()} {post.get('reply_scheduled_time')}] 同串回覆解答：{slot} ===")
  print(reply_text)
  print(f"--- 字數：{len(reply_text)} / 500 ---\n")

  if dry_run:
    print("🟡 [DRY_RUN] 乾跑模式：未實際呼叫 Threads API。")
    return

  user_id, token = resolve_credentials()

  recent = list_recent_threads(user_id, token, limit=20)
  quiz_thread = find_today_post_by_prefix(recent, date_obj, header_line)
  if not quiz_thread:
    print(f"⚠️ 找不到今日已發布的 `{header_line}` 貼文，無法掛載解答回覆。", file=sys.stderr)
    return

  parent_id = quiz_thread["id"]
  if has_answer_reply(parent_id, token):
    print(f"⏭️ 該題目串（{parent_id}）底下已有【解答公布】，自動跳過防重。")
    return

  reply_id = publish_threads_text(user_id, token, reply_text, reply_to_id=parent_id)
  print(f"✅ 已在題目串 {parent_id} 底下公布解答！reply_id = {reply_id}")


def run_refresh_token(dry_run: bool) -> None:
  if dry_run:
    print("🟡 [DRY_RUN] 將呼叫 GET https://graph.threads.net/refresh_access_token 續期 60 天長期 token。")
    return
  token = os.environ.get("THREADS_ACCESS_TOKEN", "").strip()
  if not token:
    raise RuntimeError("缺少 THREADS_ACCESS_TOKEN 環境變數。")
  resp = http_json(
    "https://graph.threads.net/refresh_access_token",
    method="GET",
    params={
      "grant_type": "th_refresh_token",
      "access_token": token,
    },
  )
  expires_days = resp.get("expires_in", 0) // 86400
  print(f"✅ Token 續期成功！新效期約 {expires_days} 天。")


def run_insights_report(dry_run: bool) -> None:
  if dry_run:
    print("🟡 [DRY_RUN] 將拉取最近 25 則貼文的 views/likes/replies/reposts 產出成效表。")
    return
  user_id, token = resolve_credentials()

  recent = list_recent_threads(user_id, token, limit=25)
  stats_by_col: dict[str, list[dict[str, int]]] = {}
  for item in recent:
    media_id = item["id"]
    first_line = item.get("text", "").splitlines()[0] if item.get("text") else "其他"
    col = first_line.split("｜")[0] if "｜" in first_line else "其他貼文"
    try:
      ins = http_json(
        f"{GRAPH_BASE}/{media_id}/insights",
        method="GET",
        params={
          "metric": "views,likes,replies,reposts,quotes",
          "access_token": token,
        },
      )
      m_map = {m["name"]: int(m.get("values", [{"value": 0}])[0].get("value", 0)) for m in ins.get("data", [])}
      stats_by_col.setdefault(col, []).append(m_map)
    except Exception as exc:
      print(f"  [insights skip {media_id}] {exc}", file=sys.stderr)

  lines = [
    "# 日檢手帖 Threads 近期專欄成效統計",
    "",
    "| 專欄 | 貼文數 | 平均曝光 (views) | 平均愛心 (likes) | 平均留言 (replies) | 平均轉發 (reposts) |",
    "|---|---:|---:|---:|---:|---:|",
  ]
  for col, rows in stats_by_col.items():
    n = len(rows)
    avg_v = sum(r.get("views", 0) for r in rows) // max(1, n)
    avg_l = sum(r.get("likes", 0) for r in rows) / max(1, n)
    avg_r = sum(r.get("replies", 0) for r in rows) / max(1, n)
    avg_rp = sum(r.get("reposts", 0) for r in rows) / max(1, n)
    lines.append(f"| {col} | {n} | {avg_v} | {avg_l:.1f} | {avg_r:.1f} | {avg_rp:.1f} |")

  out_path = QUEUE_DIR / "insights-latest.md"
  out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
  print("\n".join(lines))
  print(f"\n✅ 已寫入 {out_path.relative_to(REPO_ROOT)}")


def run_catchup(date_obj: dt.date, now_hhmm: str, dry_run: bool) -> None:
  """檢查當日截至目前台北時間 (HH:MM) 所有已到點的時段與解答回覆，未發者自動補發，已發者自動跳過。"""
  schedule_plan = [
    ("08:00", "slot", "vocab"),
    ("12:30", "slot", "quiz_easy"),
    ("15:30", "reply", "quiz_easy"),
    ("15:30", "slot", "grammar"),
    ("18:30", "slot", "quote"),
    ("21:00", "slot", "quiz_hard"),
    ("23:50", "reply", "quiz_hard"),
  ]
  print(f"⏱️ [Catchup 巡檢] 台北日期={date_obj.isoformat()} 目前時間={now_hhmm}")
  for due_hhmm, kind, target in schedule_plan:
    if now_hhmm >= due_hhmm:
      if kind == "slot":
        run_publish_slot(date_obj, target, dry_run)
      else:
        run_reply_quiz(date_obj, target, dry_run)


def main() -> None:
  parser = argparse.ArgumentParser(description="日檢手帖 Threads 自動發送與管理工具")
  parser.add_argument("--date", type=str, default="", help="指定日期 YYYY-MM-DD（預設台北今日）")
  parser.add_argument(
    "--slot",
    choices=["vocab", "quiz_easy", "grammar", "quote", "quiz_hard", "all"],
    help="發送指定時段貼文（all 會依序印出/發送當日全部 5 則）",
  )
  parser.add_argument(
    "--reply-quiz",
    choices=["quiz_easy", "quiz_hard"],
    help="在當日題目串底下自動回覆公布解答",
  )
  parser.add_argument("--catchup", action="store_true", help="自動巡檢當日所有已到點時段，未發者補發、已發者跳過")
  parser.add_argument("--refresh-token", action="store_true", help="續期 60 天長期 Threads Access Token")
  parser.add_argument("--insights", action="store_true", help="拉取 Threads Insights 產出專欄成效表")
  parser.add_argument("--dry-run", action="store_true", help="只印出內容不實際發送")
  args = parser.parse_args()

  dry_run = args.dry_run or os.environ.get("DRY_RUN") == "1"
  now_tpe = dt.datetime.now(TAIPEI_TZ)
  date_obj = dt.date.fromisoformat(args.date) if args.date else now_tpe.date()

  if args.refresh_token:
    run_refresh_token(dry_run)
    return
  if args.insights:
    run_insights_report(dry_run)
    return
  if args.catchup:
    run_catchup(date_obj, now_tpe.strftime("%H:%M"), dry_run)
    return
  if args.reply_quiz:
    run_reply_quiz(date_obj, args.reply_quiz, dry_run)
    return
  if args.slot == "all":
    for s in ["vocab", "quiz_easy", "grammar", "quote", "quiz_hard"]:
      run_publish_slot(date_obj, s, dry_run)
      if s in ("quiz_easy", "quiz_hard"):
        run_reply_quiz(date_obj, s, dry_run)
    return
  if args.slot:
    run_publish_slot(date_obj, args.slot, dry_run)
    return

  parser.print_help()


if __name__ == "__main__":
  main()
