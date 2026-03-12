from __future__ import annotations

from pathlib import Path

from pose_motion.template_builder import build_motion_template, save_template


def main() -> None:
    root = Path(__file__).resolve().parent
    action_dir = root.parent / "action"
    output_dir = root / "data" / "templates"

    videos = sorted(action_dir.glob("*.mp4"))
    if not videos:
        raise RuntimeError(f"未找到标准动作视频: {action_dir}")

    for idx, video_path in enumerate(videos, start=1):
        action_name = f"动作{idx}"
        template = build_motion_template(
            video_path=video_path,
            action_id=idx,
            action_name=action_name,
        )
        output_path = output_dir / f"action_{idx:02d}.json"
        save_template(template, output_path)
        print(f"[ok] {action_name} -> {output_path.name}  source={video_path.name}")


if __name__ == "__main__":
    main()
