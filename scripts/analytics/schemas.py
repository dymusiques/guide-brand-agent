"""CSV column schemas for multi-platform analytics warehouse."""

from __future__ import annotations

PLATFORMS = ("xiaohongshu", "instagram", "youtube")

REQUIRED: dict[str, list[str]] = {
    "xiaohongshu": [
        "note_id",
        "publish_date",
        "title",
        "pillar",
        "views",
        "likes",
        "collects",
        "comments",
        "dm_count",
    ],
    "instagram": [
        "post_id",
        "publish_date",
        "title",
        "pillar",
        "reach",
        "likes",
        "comments",
        "saves",
        "dm_count",
    ],
    "youtube": [
        "video_id",
        "publish_date",
        "title",
        "pillar",
        "views",
        "likes",
        "comments",
    ],
}

OPTIONAL_COLUMNS: dict[str, list[str]] = {
    "xiaohongshu": [
        "impressions",
        "shares",
        "follows_from_note",
        "dm_keywords",
        "aligned_at_publish",
        "brief_path",
    ],
    "instagram": [
        "caption_snippet",
        "impressions",
        "shares",
        "follows_from_post",
        "dm_keywords",
        "brief_path",
    ],
    "youtube": [
        "watch_time_hours",
        "shares",
        "subscribers_gained",
        "dm_or_email_inquiries",
        "inquiry_keywords",
        "brief_path",
    ],
}

CANONICAL_FILES = {
    "xiaohongshu": "notes.csv",
    "instagram": "posts.csv",
    "youtube": "videos.csv",
}
