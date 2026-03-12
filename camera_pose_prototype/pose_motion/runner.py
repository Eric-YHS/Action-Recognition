from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import cv2
import numpy as np

from .matcher import MatchStatus, ActionMatcher
from .pose_extractor import PoseExtractor
from .template_builder import MotionTemplate, load_template


@dataclass(slots=True)
class RunSummary:
    action_id: int
    action_name: str
    source: str
    frames_processed: int
    detections: int
    last_standard: bool | None


def load_templates(template_dir: Path) -> dict[int, MotionTemplate]:
    templates = {}
    for path in sorted(template_dir.glob("action_*.json")):
        template = load_template(path)
        templates[template.action_id] = template
    return templates


def _iter_video_frames(video_path: Path, repeat: int = 1) -> Iterator[tuple[np.ndarray, float, int]]:
    for _ in range(repeat):
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise RuntimeError(f"无法打开视频: {video_path}")

        fps = float(cap.get(cv2.CAP_PROP_FPS) or 25.0)
        frame_index = 0
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                yield frame, fps, frame_index
                frame_index += 1
        finally:
            cap.release()


def _iter_webcam_frames(camera_id: int) -> Iterator[tuple[np.ndarray, float, int]]:
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError(f"无法打开摄像头: {camera_id}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 25.0)
    frame_index = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            yield frame, fps, frame_index
            frame_index += 1
    finally:
        cap.release()


def _should_process(frame_index: int, src_fps: float, sample_fps: float) -> bool:
    step = max(1, int(round(src_fps / sample_fps)))
    return frame_index % step == 0


def overlay_status(frame: np.ndarray, template: MotionTemplate, status: MatchStatus) -> np.ndarray:
    canvas = frame.copy()
    lines = [
        f"{template.action_name}  count={status.count}",
        f"phase={status.phase}  progress={status.progress:.0%}",
        f"distance={status.current_distance:.3f}" if status.current_distance is not None else "distance=n/a",
        f"last={'标准' if status.last_standard else '不标准' if status.last_standard is not None else '未触发'}",
    ]
    y = 30
    for line in lines:
        cv2.putText(canvas, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (20, 240, 20), 2, cv2.LINE_AA)
        y += 32

    if status.event is not None:
        label = "标准" if status.event.standard else "不标准"
        color = (20, 240, 20) if status.event.standard else (10, 80, 240)
        cv2.putText(canvas, f"本次: {label}", (20, y + 16), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3, cv2.LINE_AA)
    return canvas


def run_source(
    template: MotionTemplate,
    video_path: Path | None = None,
    webcam_id: int | None = None,
    repeat: int = 1,
    sample_fps: float | None = None,
    display: bool = False,
    output_path: Path | None = None,
    mirror_input: bool = False,
) -> RunSummary:
    if (video_path is None) == (webcam_id is None):
        raise ValueError("视频和摄像头只能二选一")

    sample_fps = sample_fps or template.sample_fps
    extractor = PoseExtractor()
    matcher = ActionMatcher(template)

    writer = None
    frames_processed = 0

    if video_path is not None:
        iterator = _iter_video_frames(video_path, repeat=repeat)
        source_name = str(video_path)
    else:
        iterator = _iter_webcam_frames(webcam_id or 0)
        source_name = f"webcam:{webcam_id}"

    try:
        for global_frame_index, (frame, fps, source_frame_index) in enumerate(iterator):
            if mirror_input:
                frame = cv2.flip(frame, 1)

            if not _should_process(source_frame_index, fps, sample_fps):
                if display:
                    cv2.imshow("pose-detector", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                continue

            timestamp_ms = int((frames_processed / max(sample_fps, 1.0)) * 1000)
            extracted = extractor.extract(frame, global_frame_index, timestamp_ms)
            pose_feature = extracted.pose.feature if extracted.pose is not None else None
            status = matcher.update(pose_feature)
            frames_processed += 1

            annotated = overlay_status(frame, template, status)
            if output_path is not None:
                if writer is None:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    h, w = annotated.shape[:2]
                    writer = cv2.VideoWriter(
                        str(output_path),
                        cv2.VideoWriter_fourcc(*"mp4v"),
                        max(sample_fps, 5.0),
                        (w, h),
                    )
                writer.write(annotated)

            if display:
                cv2.imshow("pose-detector", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        if writer is not None:
            writer.release()
        if display:
            cv2.destroyAllWindows()
        extractor.close()

    return RunSummary(
        action_id=template.action_id,
        action_name=template.action_name,
        source=source_name,
        frames_processed=frames_processed,
        detections=matcher.count,
        last_standard=matcher.last_standard,
    )
