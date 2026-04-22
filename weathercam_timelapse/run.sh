#!/usr/bin/with-contenv bashio
set -euo pipefail

DATE="${DATE:-}"
FRAMERATE="${FRAMERATE:-12}"
MIN_IMAGES="${MIN_IMAGES:-10}"

if [ -z "${DATE}" ]; then
  DATE="$(date +%F)"
fi

YEAR="$(date -d "${DATE}" +%Y)"
MONTH="$(date -d "${DATE}" +%m)"
DAY="$(date -d "${DATE}" +%d)"

BASE="/media/weathercam"
SNAPDIR="${BASE}/snapshots/${DATE}"
OUTDIR="${BASE}/timelapse/${YEAR}/${MONTH}"
TMPDIR="/tmp/weathercam_${DATE}"

echo "Starte Timelapse-Build für Datum: ${DATE}"
echo "Snapshot-Ordner: ${SNAPDIR}"
echo "Zielordner: ${OUTDIR}"

mkdir -p "${OUTDIR}"

if [ ! -d "${SNAPDIR}" ]; then
  echo "Snapshot-Ordner nicht gefunden: ${SNAPDIR}"
  exit 0
fi

mapfile -t FILES < <(find "${SNAPDIR}" -maxdepth 1 -type f -name '*.jpg' | sort)

COUNT="${#FILES[@]}"

echo "Gefundene Bilder: ${COUNT}"

if [ "${COUNT}" -lt "${MIN_IMAGES}" ]; then
  echo "Zu wenige Bilder für Timelapse: ${COUNT} (Minimum: ${MIN_IMAGES})"
  exit 0
fi

rm -rf "${TMPDIR}"
mkdir -p "${TMPDIR}"

for i in "${!FILES[@]}"; do
  cp "${FILES[$i]}" "$(printf "%s/frame_%05d.jpg" "${TMPDIR}" "$((i + 1))")"
done

VIDEO_FILE="${OUTDIR}/${DAY}.mp4"
THUMB_FILE="${OUTDIR}/${DAY}.jpg"

ffmpeg -y \
  -framerate "${FRAMERATE}" \
  -i "${TMPDIR}/frame_%05d.jpg" \
  -c:v libx264 \
  -pix_fmt yuv420p \
  "${VIDEO_FILE}"

MID_INDEX=$((COUNT / 2))
MID_SOURCE="${FILES[$MID_INDEX]}"

if [ -n "${MID_SOURCE}" ] && [ -f "${MID_SOURCE}" ]; then
  cp "${MID_SOURCE}" "${THUMB_FILE}"
  echo "Thumbnail erstellt aus mittlerem Snapshot: ${THUMB_FILE}"
fi

rm -rf "${TMPDIR}"

echo "Timelapse erstellt: ${VIDEO_FILE}"
