from __future__ import annotations

import argparse
from pathlib import Path

from pose_motion.runner import load_templates, run_source


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="动作检测原型")
    parser.add_argument("--action", type=int, required=True, help="动作编号，从 1 开始")
    parser.add_argument("--video", type=Path, help="输入视频路径")
    parser.add_argument("--webcam", type=int, help="摄像头编号")
    parser.add_argument("--repeat", type=int, default=1, help="视频重复播放次数，仅视频模式有效")
    parser.add_argument("--display", action="store_true", help="是否打开实时窗口")
    parser.add_argument("--save-output", action="store_true", help="是否输出标注视频")
    parser.add_argument("--mirror", action="store_true", help="输入画面做左右镜像后再检测")
    parser.add_argument("--template-dir", type=Path, default=Path("data/templates"), help="模板目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if (args.video is None) == (args.webcam is None):
        raise SystemExit("`--video` 和 `--webcam` 必须二选一")

    root = Path(__file__).resolve().parent
    template_dir = (root / args.template_dir).resolve()
    templates = load_templates(template_dir)
    if args.action not in templates:
        raise SystemExit(f"动作 {args.action} 的模板不存在，请先运行 build_templates.py")

    template = templates[args.action]
    output_path = None
    if args.save_output and args.video is not None:
        output_path = root / "outputs" / f"action_{args.action:02d}_{args.video.stem}_annotated.mp4"

    summary = run_source(
        template=template,
        video_path=args.video.resolve() if args.video is not None else None,
        webcam_id=args.webcam,
        repeat=args.repeat,
        display=args.display,
        output_path=output_path,
        mirror_input=args.mirror,
    )

    print(
        f"[summary] action={summary.action_name} source={summary.source} "
        f"frames={summary.frames_processed} count={summary.detections} last_standard={summary.last_standard}"
    )
    if output_path is not None:
        print(f"[output] {output_path}")


if __name__ == "__main__":
    main()
