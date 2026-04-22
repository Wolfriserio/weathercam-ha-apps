# Weathercam HA Apps

A polished two-app package for **Home Assistant** that turns weather camera snapshots into daily timelapse videos and presents them in a built-in **calendar-style viewer**.

The idea behind this project was simple:  
**Ecowitt only keeps timelapse videos for a few days**, so I wanted a local Home Assistant based alternative with long-term storage, automatic daily processing, and a much nicer way to browse older recordings.

---

# English

## Overview

This repository contains two Home Assistant apps:

### 1. Weathercam Timelapse
Builds a daily timelapse from weather camera snapshots and stores it in a clean archive structure.

**Features**
- creates one **MP4 video per day**
- creates one **thumbnail JPG per day**
- supports a configurable minimum image count
- works well with 5-minute snapshot automations
- stores output in a structured archive by **year / month / day**

### 2. Weathercam Calendar
Provides a built-in **Ingress UI inside Home Assistant** for browsing timelapse videos.

**Features**
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

1. Home Assistant creates weather camera snapshots during the day
2. **Weathercam Timelapse** builds the daily MP4 and thumbnail
3. **Weathercam Calendar** scans the timelapse archive automatically
4. New **years**, **months**, and **days** appear automatically the next time the app UI is opened or refreshed

No manual month or year maintenance is required.

---

## Installation

1. In Home Assistant, open **Settings → Apps → App Store**
2. Open the menu in the top right
3. Choose **Repositories**
4. Add this repository URL:

   `https://github.com/Wolfriserio/weathercam-ha-apps`

5. Refresh the App Store

After that, these apps should appear:
- **Weathercam Timelapse**
- **Weathercam Calendar**

---

## Recommended install order

1. Install **Weathercam Timelapse**
2. Install **Weathercam Calendar**

---

## Initial setup

### Weathercam Timelapse
Set up your snapshot workflow so that daily videos are written to:

```text
/media/weathercam/timelapse/YYYY/MM/DD.mp4
```

Example:

```text
/media/weathercam/timelapse/2026/04/21.mp4
```

Optional thumbnails can be stored next to the video:

```text
/media/weathercam/timelapse/YYYY/MM/DD.jpg
```

### Weathercam Calendar
Open the app configuration and keep the default path unless you use a custom location:

```text
/media/weathercam/timelapse
```

The calendar app scans this folder structure automatically.  
New years, months, and days appear automatically after reopening or refreshing the app.

---

## Lovelace integration

The Weathercam Calendar app can also be embedded directly into a Home Assistant dashboard.

### Full calendar view

Use a manual card with one of the following examples.

#### Option 1: iframe

```yaml
type: iframe
url: /app/local_weathercam_calendar
aspect_ratio: 75%
```

#### Option 2: webpage

```yaml
type: webpage
url: /app/local_weathercam_calendar
aspect_ratio: 75%
```

### Simple launcher button

If you prefer a compact shortcut card, you can use:

```yaml
type: button
name: Weathercam Calendar
icon: mdi:calendar-month
tap_action:
  action: navigate
  navigation_path: /app/local_weathercam_calendar
```

### Notes

- `iframe` and `webpage` behavior may vary depending on the Home Assistant frontend version
- If one card type does not work properly, try the other one
- The path `/app/local_weathercam_calendar` opens the installed Weathercam Calendar app directly inside Home Assistant

---

## Notes

- The calendar only highlights days where a matching `.mp4` file exists
- If a matching `.jpg` file exists, it is used as the preview thumbnail
- The built-in popup player plays videos directly inside Home Assistant

---

# Deutsch

## Überblick

Dieses Repository enthält zwei Apps für Home Assistant:

### 1. Weathercam Timelapse
Erstellt aus Wetterkamera-Snapshots einen täglichen Zeitraffer und speichert ihn in einer sauberen Archivstruktur.

**Funktionen**
- erstellt **eine MP4-Datei pro Tag**
- erstellt **ein JPG-Vorschaubild pro Tag**
- unterstützt eine konfigurierbare Mindestanzahl an Bildern
- funktioniert sehr gut mit 5-Minuten-Snapshot-Automationen
- speichert die Ausgabe strukturiert nach **Jahr / Monat / Tag**

### 2. Weathercam Calendar
Stellt eine integrierte **Ingress-Oberfläche innerhalb von Home Assistant** zum Durchsuchen der Zeitraffer bereit.

**Funktionen**
- **Jahresauswahl**
- **Monatsauswahl**
- anklickbare **Kalenderansicht**
- Video-Popup-Player
- Download-Button
- Tages-Vorschaubilder
- Schnellzugriff auf den **zuletzt verfügbaren Tag**

---

## Erwartete Ordnerstruktur

### Eingangs-Snapshots

```text
/media/weathercam/snapshots/YYYY-MM-DD/*.jpg
```

Beispiel:

```text
/media/weathercam/snapshots/2026-04-21/weathercam_20260421_120000.jpg
```

### Zeitraffer-Ausgabe

```text
/media/weathercam/timelapse/YYYY/MM/DD.mp4
/media/weathercam/timelapse/YYYY/MM/DD.jpg
```

Beispiel:

```text
/media/weathercam/timelapse/2026/04/21.mp4
/media/weathercam/timelapse/2026/04/21.jpg
```

---

## So funktioniert es

1. Home Assistant erstellt tagsüber Wetterkamera-Snapshots
2. **Weathercam Timelapse** baut daraus die tägliche MP4-Datei und das Vorschaubild
3. **Weathercam Calendar** liest das Zeitraffer-Archiv automatisch ein
4. Neue **Jahre**, **Monate** und **Tage** erscheinen automatisch, sobald die App-Oberfläche neu geöffnet oder aktualisiert wird

Eine manuelle Pflege von Monaten oder Jahren ist nicht nötig.

---

## Installation

1. In Home Assistant **Einstellungen → Apps → App Store** öffnen
2. Das Menü oben rechts öffnen
3. **Repositories** auswählen
4. Diese Repository-URL hinzufügen:

   `https://github.com/Wolfriserio/weathercam-ha-apps`

5. Den App Store aktualisieren

Danach sollten diese Apps erscheinen:
- **Weathercam Timelapse**
- **Weathercam Calendar**

---

## Empfohlene Installationsreihenfolge

1. Zuerst **Weathercam Timelapse** installieren
2. Danach **Weathercam Calendar** installieren

---

## Erste Einrichtung

### Weathercam Timelapse
Richte deinen Snapshot-Workflow so ein, dass die Tagesvideos hier abgelegt werden:

```text
/media/weathercam/timelapse/YYYY/MM/DD.mp4
```

Beispiel:

```text
/media/weathercam/timelapse/2026/04/21.mp4
```

Optionale Vorschaubilder können direkt daneben gespeichert werden:

```text
/media/weathercam/timelapse/YYYY/MM/DD.jpg
```

### Weathercam Calendar
In der App-Konfiguration kann der Standardpfad in der Regel unverändert bleiben:

```text
/media/weathercam/timelapse
```

Die Kalender-App liest diese Ordnerstruktur automatisch ein.  
Neue Jahre, Monate und Tage erscheinen automatisch, sobald die App neu geöffnet oder aktualisiert wird.

---

## Lovelace-Integration

Die Weathercam-Calendar-App kann auch direkt in ein Home-Assistant-Dashboard eingebettet werden.

### Vollständige Kalenderansicht

Verwende dazu eine manuelle Karte mit einem der folgenden Beispiele.

#### Option 1: iframe

```yaml
type: iframe
url: /app/local_weathercam_calendar
aspect_ratio: 75%
```

#### Option 2: webpage

```yaml
type: webpage
url: /app/local_weathercam_calendar
aspect_ratio: 75%
```

### Einfacher Start-Button

Wenn du lieber nur eine kompakte Schnellzugriffs-Karte möchtest, kannst du Folgendes verwenden:

```yaml
type: button
name: Weathercam Kalender
icon: mdi:calendar-month
tap_action:
  action: navigate
  navigation_path: /app/local_weathercam_calendar
```

### Hinweise zur Lovelace-Integration

- Das Verhalten von `iframe` und `webpage` kann je nach Home-Assistant-Frontend-Version leicht variieren
- Wenn ein Kartentyp nicht sauber funktioniert, probiere den anderen
- Der Pfad `/app/local_weathercam_calendar` öffnet die installierte Weathercam-Calendar-App direkt innerhalb von Home Assistant

---

## Hinweise

- Im Kalender werden nur Tage hervorgehoben, an denen eine passende `.mp4`-Datei vorhanden ist
- Wenn zusätzlich eine passende `.jpg`-Datei vorhanden ist, wird sie als Vorschaubild verwendet
- Das integrierte Video-Popup spielt die Dateien direkt innerhalb von Home Assistant ab
