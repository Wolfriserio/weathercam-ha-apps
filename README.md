# Weathercam HA Apps

A polished two-app package for **Home Assistant** that turns weather camera snapshots into daily timelapse videos and presents them in a built-in **calendar-style viewer**.

## What this repository contains

### 1. Weathercam Timelapse
Builds a daily timelapse from snapshots and stores it in a clean archive structure.

Features:
- creates one **MP4 per day**
- creates one **thumbnail JPG per day**
- supports a configurable minimum image count
- works well with 5-minute snapshot automations

### 2. Weathercam Calendar
Provides an **Ingress UI inside Home Assistant** with:
- **year selection**
- **month selection**
- clickable **calendar view**
- popup video player
- download button
- day thumbnails
- quick jump to the **latest available day**

---

## Expected directory structure

### Input snapshots

```text
/media/weathercam/snapshots/YYYY-MM-DD/*.jpg
```

Example:

```text
/media/weathercam/snapshots/2026-04-21/weathercam_20260421_120000.jpg
```

### Timelapse output

```text
/media/weathercam/timelapse/YYYY/MM/DD.mp4
/media/weathercam/timelapse/YYYY/MM/DD.jpg
```

Example:

```text
/media/weathercam/timelapse/2026/04/21.mp4
/media/weathercam/timelapse/2026/04/21.jpg
```

---

## How it works

1. Home Assistant creates weathercam snapshots during the day.
2. The **Weathercam Timelapse** app builds the daily video and thumbnail.
3. The **Weathercam Calendar** app automatically scans the timelapse folders.
4. New **years**, **months**, and **days** appear in the calendar UI the next time the app UI is opened or refreshed.

No manual month or year maintenance is required.

---

## Installation

## Step 1: Put this repository on GitHub

Create a GitHub repository and upload the contents of this folder.

Important:
Update the `url:` in `repository.yaml` to your real GitHub repository URL.

Example:

```yaml
url: https://github.com/<your-user>/<your-repo>
```

---

## Step 2: Add the repository to Home Assistant

In Home Assistant:

1. Open **Settings → Apps → App Store**
2. Open the menu in the top right
3. Choose **Repositories**
4. Add your GitHub repository URL

After that, both apps should appear:
- **Weathercam Timelapse**
- **Weathercam Calendar**

---

## Step 3: Install the apps

Install both apps in this order:

1. **Weathercam Timelapse**
2. **Weathercam Calendar**

---

## Step 4: Configure the apps

### Weathercam Timelapse
Recommended defaults:

- `date`: leave empty
- `framerate`: `12`
- `min_images`: `10`

### Weathercam Calendar
Recommended defaults:

- `root_dir`: `/media/weathercam/timelapse`
- `title`: `Weathercam Timelapse`

---

## Home Assistant automation example

The apps do **not** create snapshots by themselves.
You still need a normal Home Assistant automation that stores snapshots from your camera.

### Snapshot automation example

```yaml
- id: weathercam_snapshot_every_5_min
  alias: Weathercam Snapshot every 5 minutes
  mode: single
  trigger:
    - platform: time_pattern
      minutes: "/5"
  action:
    - variables:
        folder_date: "{{ now().strftime('%Y-%m-%d') }}"
        file_ts: "{{ now().strftime('%Y%m%d_%H%M%S') }}"
    - action: shell_command.prepare_weathercam_dir
      data:
        folder: "{{ folder_date }}"
    - action: camera.snapshot
      target:
        entity_id: camera.your_weathercam
      data:
        filename: "/media/weathercam/snapshots/{{ folder_date }}/weathercam_{{ file_ts }}.jpg"
```

### Daily timelapse build example

```yaml
- id: weathercam_build_daily_timelapse
  alias: Weathercam Timelapse build daily
  mode: single
  trigger:
    - platform: time
      at: "23:59:00"
  action:
    - action: hassio.app_start
      data:
        app: local_weathercam_timelapse
```

### Cleanup example

```yaml
- id: weathercam_cleanup_files
  alias: Weathercam Timelapse Cleanup
  mode: single
  trigger:
    - platform: time
      at: "00:20:00"
  action:
    - action: shell_command.cleanup_weathercam_timelapse
```

Note:
If the app is installed from a GitHub repository, the app slug may differ from `local_weathercam_timelapse` depending on the repository slug.

---

## Shell commands example

These shell commands are useful in `configuration.yaml`:

```yaml
ffmpeg:

shell_command:
  prepare_weathercam_dir: >-
    mkdir -p /media/weathercam/snapshots/{{ folder }}
  cleanup_weathercam_timelapse: >-
    find /media/weathercam/snapshots -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \; &&
    find /media/weathercam/timelapse -type f -name '*.mp4' -mtime +365 -delete &&
    find /media/weathercam/timelapse -type f -name '*.jpg' -mtime +365 -delete
```

---

## Calendar app behavior

The calendar app scans the timelapse directory dynamically.

That means:
- when a new **year folder** appears, it becomes selectable
- when a new **month folder** appears, it becomes selectable
- when a new **day video** appears, that day becomes active in the calendar

Usually a simple reload of the app UI is enough to see new content.

---

## Notes about thumbnails

Thumbnails are stored next to the MP4 files as `.jpg` files.

Example:

```text
/media/weathercam/timelapse/2026/04/21.mp4
/media/weathercam/timelapse/2026/04/21.jpg
```

The calendar UI automatically uses the thumbnail if present.
If no thumbnail exists, the day remains clickable but shows no preview image.

---

## Recommended use case

This package is ideal for:
- weather stations
- garden cameras
- skyline cameras
- roof cameras
- cloud movement timelapses
- sunrise / sunset monitoring

---

## Troubleshooting

### The calendar says “Keine Timelapse-Videos gefunden”
Check these points:
- `root_dir` in **Weathercam Calendar** is correct
- the folder contains files in `YYYY/MM/DD.mp4`
- the app was rebuilt after file changes
- the app log shows the correct path

### The timelapse app starts but no video is created
Check these points:
- enough snapshots exist for the day
- `min_images` is not too high
- the snapshot folder name matches `YYYY-MM-DD`
- the app log shows the detected image count

### A new month does not appear
Usually reloading or reopening the calendar UI is enough.
If needed:
- restart the app
- rebuild the app

---

## Repository contents

```text
repository.yaml
weathercam_timelapse/
weathercam_calendar/
README.md
LICENSE
```

---

## Roadmap ideas

Possible future improvements:
- smarter thumbnail selection
- weather data overlay in timelapses
- direct month statistics
- thumbnail generation from video frames
- multiple camera support
- automatic pruning rules in the UI

---

## License

This repository includes an MIT license.

---

## Credits

Built for Home Assistant users who want a clean self-hosted alternative to limited cloud timelapse archives.
