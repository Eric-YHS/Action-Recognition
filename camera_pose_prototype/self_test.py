from __future__ import annotations

import argparse
from pathlib import Path

from pose_motion.runner import load_templates, run_source


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="标准动作视频自测")
    parser.add_argument("--repeat", type=int, default=2, help="把同一个标准视频连续播放几次")
    parser.add_argument("--mirror", action="store_true", help="对输入视频做镜像后再检测")
    parser.add_argument("--template-dir", type=Path, default=Path("data/templates"), help="模板目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent
    action_dir = root.parent / "action"
    template_dir = (root / args.template_dir).resolve()
    templates = load_templates(template_dir)
    videos = sorted(action_dir.glob("*.mp4"))

    print(f"[self-test] repeat={args.repeat}")
    for idx, video_path in enumerate(videos, start=1):
        template = templates[idx]
        summary = run_source(
            template=template,
            video_path=video_path,
            repeat=args.repeat,
            display=False,
            output_path=None,
            mirror_input=args.mirror,
        )
        print(
            f"动作{idx}: video={video_path.name} count={summary.detections} "
            f"last_standard={summary.last_standard} frames={summary.frames_processed}"
        )


if __name__ == "__main__":
    main()
