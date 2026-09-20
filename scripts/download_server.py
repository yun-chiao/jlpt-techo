#!/usr/bin/env python3
"""
客製化下載伺服器：強制在所有 response 帶上 Content-Disposition: attachment 標頭，
讓瀏覽器點擊連結時 100% 跳出系統下載儲存視窗，不再開空白分頁。
"""

import http.server
import os
import socketserver
import urllib.parse
from pathlib import Path

PORT = 8731
DIRECTORY = Path(__file__).resolve().parents[1] / "dist-products"


class DownloadHandler(http.server.SimpleHTTPRequestHandler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=str(DIRECTORY), **kwargs)

  def end_headers(self):
    # 若是 zip 或 apkg 檔案，強制加上 attachment 標頭與 octet-stream
    clean_path = urllib.parse.unquote(self.path).split("?")[0]
    filename = os.path.basename(clean_path)
    if filename.endswith(".zip") or filename.endswith(".apkg"):
      self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
      self.send_header("Content-Type", "application/octet-stream")
    super().end_headers()


if __name__ == "__main__":
  os.chdir(DIRECTORY)
  # 允許 port 重用
  socketserver.TCPServer.allow_reuse_address = True
  with socketserver.TCPServer(("0.0.0.0", PORT), DownloadHandler) as httpd:
    print(f"Serving downloads from {DIRECTORY} on port {PORT} with forced attachment headers...")
    httpd.serve_forever()
