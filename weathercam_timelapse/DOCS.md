# Weathercam Timelapse

Builds daily timelapse videos and thumbnails from snapshots stored under:

`/media/weathercam/snapshots/YYYY-MM-DD/*.jpg`

Output:

- Video: `/media/weathercam/timelapse/YYYY/MM/DD.mp4`
- Thumbnail: `/media/weathercam/timelapse/YYYY/MM/DD.jpg`

## Options

- `date`: Date in `YYYY-MM-DD` format. Empty = today.
- `framerate`: Output FPS. Default `12`.
- `min_images`: Minimum number of snapshots required. Default `10`.
