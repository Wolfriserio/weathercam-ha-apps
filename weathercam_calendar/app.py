import os
import re
from pathlib import Path
from flask import Flask, jsonify, abort, send_file

app = Flask(__name__)

ROOT_DIR = Path(os.environ.get("ROOT_DIR", "/media/weathercam/timelapse")).resolve()
APP_TITLE = os.environ.get("APP_TITLE", "Weathercam Timelapse")


def safe_year(value: str) -> bool:
    return bool(re.fullmatch(r"\d{4}", value))


def safe_month(value: str) -> bool:
    return bool(re.fullmatch(r"\d{2}", value))


def safe_day(value: str) -> bool:
    return bool(re.fullmatch(r"\d{2}", value))


def scan_structure():
    result = {}
    if not ROOT_DIR.exists():
        return result

    for year_dir in sorted([p for p in ROOT_DIR.iterdir() if p.is_dir() and safe_year(p.name)]):
        months = {}
        for month_dir in sorted([p for p in year_dir.iterdir() if p.is_dir() and safe_month(p.name)]):
            days = {}
            for file in sorted(month_dir.glob("*.mp4")):
                day = file.stem
                if safe_day(day):
                    thumb = month_dir / f"{day}.jpg"
                    days[day] = {
                        "video": True,
                        "thumb": thumb.exists()
                    }
            if days:
                months[month_dir.name] = days
        if months:
            result[year_dir.name] = months

    return result


@app.get("/api/index")
def api_index():
    return jsonify({
        "title": APP_TITLE,
        "root_dir": str(ROOT_DIR),
        "data": scan_structure(),
    })


@app.get("/api/video/<year>/<month>/<day>")
def api_video(year: str, month: str, day: str):
    if not (safe_year(year) and safe_month(month) and safe_day(day)):
        abort(404)

    file_path = (ROOT_DIR / year / month / f"{day}.mp4").resolve()

    if not str(file_path).startswith(str(ROOT_DIR)):
        abort(403)

    if not file_path.exists() or not file_path.is_file():
        abort(404)

    return send_file(file_path, mimetype="video/mp4", conditional=True)


@app.get("/api/thumb/<year>/<month>/<day>")
def api_thumb(year: str, month: str, day: str):
    if not (safe_year(year) and safe_month(month) and safe_day(day)):
        abort(404)

    file_path = (ROOT_DIR / year / month / f"{day}.jpg").resolve()

    if not str(file_path).startswith(str(ROOT_DIR)):
        abort(403)

    if not file_path.exists() or not file_path.is_file():
        abort(404)

    return send_file(file_path, mimetype="image/jpeg", conditional=True)


@app.get("/")
def index():
    html = """
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>__APP_TITLE__</title>
  <style>
    :root {
      --bg: #09152b;
      --panel: #1f2c42;
      --panel-2: #2b3b55;
      --text: #f8fafc;
      --muted: #9fb0c8;
      --accent: #60a5fa;
      --accent-2: #3b82f6;
      --good: #93c5fd;
      --empty: rgba(255,255,255,0.04);
      --shadow: 0 10px 30px rgba(0,0,0,0.35);
      --radius: 18px;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }

    .wrap {
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
    }

    .topbar {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }

    .title {
      font-size: 1.9rem;
      font-weight: 800;
    }

    .controls {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }

    select, button {
      background: var(--panel);
      color: var(--text);
      border: 1px solid var(--panel-2);
      border-radius: 14px;
      padding: 10px 14px;
      font-size: 0.95rem;
      cursor: pointer;
    }

    button:hover, select:hover {
      border-color: var(--accent);
    }

    .quickbar {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin: 8px 0 20px;
    }

    .month-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 12px 0 16px;
      gap: 12px;
    }

    .month-label {
      font-size: 1.4rem;
      font-weight: 800;
    }

    .weekday-grid, .calendar-grid {
      display: grid;
      grid-template-columns: repeat(7, minmax(0, 1fr));
      gap: 12px;
    }

    .weekday {
      text-align: center;
      color: var(--muted);
      font-weight: 700;
      padding: 8px 0;
    }

    .day {
      min-height: 104px;
      border-radius: var(--radius);
      background: var(--panel);
      background-size: cover;
      background-position: center;
      overflow: hidden;
      box-shadow: var(--shadow);
      border: 1px solid transparent;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 12px;
    }

    .day.empty {
      background: var(--empty);
      box-shadow: none;
      border-color: rgba(255,255,255,0.03);
    }

    .day.has-video {
      cursor: pointer;
      border-color: rgba(96,165,250,0.45);
      transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
    }

    .day.has-video:hover {
      transform: translateY(-2px);
      border-color: var(--accent);
      background: #233652;
    }

    .day-number {
      font-size: 1.15rem;
      font-weight: 800;
      text-shadow: 0 1px 2px rgba(0,0,0,0.45);
    }

    .day-status {
      font-size: 0.88rem;
      color: var(--muted);
      text-shadow: 0 1px 2px rgba(0,0,0,0.45);
    }

    .has-video .day-status {
      color: #ffffff;
      font-weight: 700;
    }

    .today {
      outline: 2px solid var(--accent);
      outline-offset: 1px;
    }

    .empty-state {
      color: var(--muted);
      padding: 24px 0;
      text-align: center;
    }

    .modal {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.76);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 18px;
      z-index: 9999;
    }

    .modal.open {
      display: flex;
    }

    .modal-box {
      width: min(1180px, 100%);
      background: var(--panel);
      border-radius: 22px;
      box-shadow: var(--shadow);
      overflow: hidden;
      border: 1px solid var(--panel-2);
    }

    .modal-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 14px 18px;
      border-bottom: 1px solid var(--panel-2);
    }

    .modal-title {
      font-size: 1.05rem;
      font-weight: 800;
    }

    .modal-actions {
      display: flex;
      gap: 10px;
      align-items: center;
    }

    .download-btn {
      text-decoration: none;
      background: var(--accent-2);
      color: white;
      border-radius: 12px;
      padding: 10px 14px;
      font-size: 0.9rem;
      font-weight: 700;
      border: 0;
    }

    .close-btn {
      background: transparent;
      border: 0;
      color: var(--text);
      font-size: 1.6rem;
      cursor: pointer;
      padding: 0 8px;
    }

    video {
      width: 100%;
      max-height: 82vh;
      background: #000;
      display: block;
    }

    @media (max-width: 700px) {
      .wrap {
        padding: 16px;
      }
      .day {
        min-height: 84px;
        padding: 10px;
      }
      .day-status {
        font-size: 0.78rem;
      }
      .title {
        font-size: 1.5rem;
      }
      .month-label {
        font-size: 1.15rem;
      }
      .modal-actions {
        gap: 6px;
      }
      .download-btn {
        padding: 8px 10px;
        font-size: 0.82rem;
      }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <div class="title" id="app-title">__APP_TITLE__</div>
      <div class="controls">
        <button id="prev-month">◀</button>
        <select id="year-select"></select>
        <select id="month-select"></select>
        <button id="next-month">▶</button>
      </div>
    </div>

    <div class="quickbar">
      <button id="jump-latest">Letzter verfügbarer Tag</button>
    </div>

    <div class="month-header">
      <div class="month-label" id="month-label">–</div>
    </div>

    <div class="weekday-grid">
      <div class="weekday">Mo</div>
      <div class="weekday">Di</div>
      <div class="weekday">Mi</div>
      <div class="weekday">Do</div>
      <div class="weekday">Fr</div>
      <div class="weekday">Sa</div>
      <div class="weekday">So</div>
    </div>

    <div class="calendar-grid" id="calendar"></div>
    <div class="empty-state" id="empty-state" style="display:none;">Keine Videos gefunden.</div>
  </div>

  <div class="modal" id="video-modal">
    <div class="modal-box">
      <div class="modal-head">
        <div class="modal-title" id="modal-title">Video</div>
        <div class="modal-actions">
          <a id="download-link" class="download-btn" href="#" download>Zeitraffer laden</a>
          <button class="close-btn" id="close-modal">×</button>
        </div>
      </div>
      <video id="video-player" controls playsinline></video>
    </div>
  </div>

  <script>
    const MONTH_NAMES = {
      "01": "Januar", "02": "Februar", "03": "März", "04": "April",
      "05": "Mai", "06": "Juni", "07": "Juli", "08": "August",
      "09": "September", "10": "Oktober", "11": "November", "12": "Dezember"
    };

    let indexData = {};
    let selectedYear = null;
    let selectedMonth = null;

    const yearSelect = document.getElementById("year-select");
    const monthSelect = document.getElementById("month-select");
    const monthLabel = document.getElementById("month-label");
    const calendar = document.getElementById("calendar");
    const emptyState = document.getElementById("empty-state");
    const modal = document.getElementById("video-modal");
    const videoPlayer = document.getElementById("video-player");
    const modalTitle = document.getElementById("modal-title");
    const downloadLink = document.getElementById("download-link");

    function sortKeys(keys) {
      return [...keys].sort((a, b) => a.localeCompare(b));
    }

    function getAvailableYears() {
      return sortKeys(Object.keys(indexData));
    }

    function getAvailableMonths(year) {
      if (!indexData[year]) return [];
      return sortKeys(Object.keys(indexData[year]));
    }

    function getAvailableDays(year, month) {
      return indexData[year]?.[month] || {};
    }

    function getLatestAvailable() {
      const years = getAvailableYears();
      if (!years.length) return null;
      const latestYear = years[years.length - 1];
      const months = getAvailableMonths(latestYear);
      if (!months.length) return null;
      const latestMonth = months[months.length - 1];
      const days = sortKeys(Object.keys(indexData[latestYear][latestMonth] || {}));
      if (!days.length) return null;
      return { year: latestYear, month: latestMonth, day: days[days.length - 1] };
    }

    function fillYearSelect() {
      yearSelect.innerHTML = "";
      for (const year of getAvailableYears()) {
        const opt = document.createElement("option");
        opt.value = year;
        opt.textContent = year;
        yearSelect.appendChild(opt);
      }
    }

    function fillMonthSelect() {
      monthSelect.innerHTML = "";
      for (const month of getAvailableMonths(selectedYear)) {
        const opt = document.createElement("option");
        opt.value = month;
        opt.textContent = MONTH_NAMES[month] || month;
        monthSelect.appendChild(opt);
      }
    }

    function daysInMonth(year, month) {
      return new Date(Number(year), Number(month), 0).getDate();
    }

    function firstWeekdayOffset(year, month) {
      const jsDay = new Date(`${year}-${month}-01`).getDay();
      return jsDay === 0 ? 6 : jsDay - 1;
    }

    function openVideo(year, month, day) {
      const url = `./api/video/${year}/${month}/${day}`;
      modalTitle.textContent = `Timelapse ${day}.${month}.${year}`;
      downloadLink.href = url;
      downloadLink.download = `${year}-${month}-${day}.mp4`;
      videoPlayer.src = url;
      modal.classList.add("open");
      videoPlayer.load();
      videoPlayer.play().catch(() => {});
    }

    function closeVideo() {
      modal.classList.remove("open");
      videoPlayer.pause();
      videoPlayer.removeAttribute("src");
      videoPlayer.load();
      downloadLink.href = "#";
    }

    function renderCalendar() {
      calendar.innerHTML = "";

      if (!selectedYear || !selectedMonth) {
        emptyState.style.display = "block";
        return;
      }

      emptyState.style.display = "none";
      monthLabel.textContent = `${MONTH_NAMES[selectedMonth] || selectedMonth} ${selectedYear}`;

      const availableDays = getAvailableDays(selectedYear, selectedMonth);
      const totalDays = daysInMonth(selectedYear, selectedMonth);
      const offset = firstWeekdayOffset(selectedYear, selectedMonth);

      for (let i = 0; i < offset; i++) {
        const card = document.createElement("div");
        card.className = "day empty";
        calendar.appendChild(card);
      }

      const today = new Date();
      const todayY = String(today.getFullYear());
      const todayM = String(today.getMonth() + 1).padStart(2, "0");
      const todayD = String(today.getDate()).padStart(2, "0");

      for (let day = 1; day <= totalDays; day++) {
        const dd = String(day).padStart(2, "0");
        const dayData = availableDays[dd] || null;
        const hasVideo = !!dayData;
        const hasThumb = !!(dayData && dayData.thumb);

        const card = document.createElement("div");
        card.className = "day" + (hasVideo ? " has-video" : " empty");

        if (selectedYear === todayY && selectedMonth === todayM && dd === todayD) {
          card.classList.add("today");
        }

        if (hasThumb) {
          card.style.backgroundImage = `linear-gradient(rgba(9,21,43,0.20), rgba(9,21,43,0.55)), url('./api/thumb/${selectedYear}/${selectedMonth}/${dd}')`;
        }

        card.innerHTML = `
          <div class="day-number">${dd}</div>
          <div class="day-status">${hasVideo ? "" : "Kein Video"}</div>
        `;

        if (hasVideo) {
          card.addEventListener("click", () => openVideo(selectedYear, selectedMonth, dd));
        }

        calendar.appendChild(card);
      }
    }

    function setSelection(year, month) {
      selectedYear = year;
      fillMonthSelect();

      const availableMonths = getAvailableMonths(selectedYear);
      if (!availableMonths.length) {
        selectedMonth = null;
      } else {
        selectedMonth = availableMonths.includes(month) ? month : availableMonths[availableMonths.length - 1];
      }

      yearSelect.value = selectedYear;
      if (selectedMonth) {
        monthSelect.value = selectedMonth;
      }
      renderCalendar();
    }

    function moveMonth(step) {
      const years = getAvailableYears();
      if (!selectedYear || !selectedMonth) return;

      const pairs = [];
      for (const y of years) {
        for (const m of getAvailableMonths(y)) {
          pairs.push(`${y}-${m}`);
        }
      }

      const current = `${selectedYear}-${selectedMonth}`;
      const idx = pairs.indexOf(current);
      if (idx === -1) return;

      const nextIdx = idx + step;
      if (nextIdx < 0 || nextIdx >= pairs.length) return;

      const parts = pairs[nextIdx].split("-");
      setSelection(parts[0], parts[1]);
    }

    function jumpToLatest() {
      const latest = getLatestAvailable();
      if (!latest) return;
      setSelection(latest.year, latest.month);
      setTimeout(() => openVideo(latest.year, latest.month, latest.day), 50);
    }

    async function init() {
      const res = await fetch("./api/index");
      const payload = await res.json();
      indexData = payload.data || {};
      document.getElementById("app-title").textContent = payload.title || "Weathercam Timelapse";

      const years = getAvailableYears();
      if (!years.length) {
        emptyState.style.display = "block";
        emptyState.textContent = "Keine Timelapse-Videos gefunden.";
        return;
      }

      fillYearSelect();

      const latest = getLatestAvailable();
      if (latest) {
        setSelection(latest.year, latest.month);
      }
    }

    yearSelect.addEventListener("change", (e) => {
      setSelection(e.target.value, selectedMonth);
    });

    monthSelect.addEventListener("change", (e) => {
      selectedMonth = e.target.value;
      renderCalendar();
    });

    document.getElementById("prev-month").addEventListener("click", () => moveMonth(-1));
    document.getElementById("next-month").addEventListener("click", () => moveMonth(1));
    document.getElementById("jump-latest").addEventListener("click", jumpToLatest);
    document.getElementById("close-modal").addEventListener("click", closeVideo);
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeVideo();
    });

    init();
  </script>
</body>
</html>
"""
    return html.replace("__APP_TITLE__", APP_TITLE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099, debug=False)
