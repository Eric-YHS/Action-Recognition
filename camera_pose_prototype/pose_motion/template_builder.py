from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path

import cv2
import numpy as np

from .features import interpolate_sequence
from .pose_extractor import PoseExtractor


@dataclass(slots=True)
class MotionTemplate:
    action_id: int
    action_name: str
    source_video: str
    fps: float
    sample_fps: float
    template_length: int
    feature_dim: int
    sequence: list[list[float]]
    mirror_sequence: list[list[float]]
    start_pose: list[float]
    mirror_start_pose: list[float]
    end_pose: list[float]
    mirror_end_pose: list[float]
    start_threshold: float
    match_threshold: float
    standard_threshold: float
    coverage_threshold: float
    start_hold_frames: int
    cooldown_frames: int
    max_advance_per_frame: int
    end_band_size: int

    @property
    def sequence_array(self) -> np.ndarray:
        return np.asarray(self.sequence, dtype=np.float32)

    @property
    def mirror_sequence_array(self) -> np.ndarray:
        return np.asarray(self.mirror_sequence, dtype=np.float32)

    @property
    def start_pose_array(self) -> np.ndarray:
        return np.asarray(self.start_pose, dtype=np.float32)

    @property
    def mirror_start_pose_array(self) -> np.ndarray:
        return np.asarray(self.mirror_start_pose, dtype=np.float32)


def _calibrate_thresholds(sequence: np.ndarray) -> tuple[float, float, float]:
    frame_deltas = np.linalg.norm(np.diff(sequence, axis=0), axis=1)
    motion_scale = float(np.median(frame_deltas)) if len(frame_deltas) else 0.08
    trajectory_spread = float(np.mean(np.linalg.norm(sequence - sequence[0], axis=1)))

    start_threshold = max(0.30, motion_scale * 3.0)
    match_threshold = max(0.55, min(2.0, trajectory_spread * 0.95))
    standard_threshold = min(match_threshold, max(0.52, match_threshold * 0.97))
    return start_threshold, match_threshold, standard_threshold


def build_motion_template(
    video_path: Path,
    action_id: int,
    action_name: str,
    sample_fps: float = 6.0,
    template_length: int | None = 32,
) -> MotionTemplate:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频: {video_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 25.0)
    frame_interval = max(1, int(round(fps / sample_fps)))
    extractor = PoseExtractor()

    features = []
    mirrored_features = []
    frame_index = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            if frame_index % frame_interval != 0:
                frame_index += 1
                continue

            extracted = extractor.extract(frame, frame_index, int((frame_index / fps) * 1000))
            if extracted.pose is not None:
                features.append(extracted.pose.feature)
                mirrored_features.append(extracted.pose.mirrored_feature)
            frame_index += 1
    finally:
        cap.release()
        extractor.close()

    if len(features) < 8:
        raise RuntimeError(f"视频有效姿态帧过少: {video_path}")

    raw_sequence = np.asarray(features, dtype=np.float32)
    raw_mirror_sequence = np.asarray(mirrored_features, dtype=np.float32)
    target_length = template_length or 32

    sequence = interpolate_sequence(raw_sequence, target_length)
    mirror_sequence = interpolate_sequence(raw_mirror_sequence, target_length)
    start_threshold, match_threshold, standard_threshold = _calibrate_thresholds(sequence)

    return MotionTemplate(
        action_id=action_id,
        action_name=action_name,
        source_video=str(video_path),
        fps=fps,
        sample_fps=sample_fps,
        template_length=target_length,
        feature_dim=int(sequence.shape[1]),
        sequence=sequence.tolist(),
        mirror_sequence=mirror_sequence.tolist(),
        start_pose=sequence[0].tolist(),
        mirror_start_pose=mirror_sequence[0].tolist(),
        end_pose=sequence[-1].tolist(),
        mirror_end_pose=mirror_sequence[-1].tolist(),
        start_threshold=start_threshold,
        match_threshold=match_threshold,
        standard_threshold=standard_threshold,
        coverage_threshold=0.60,
        start_hold_frames=1,
        cooldown_frames=1,
        max_advance_per_frame=max(4, target_length // 6),
        end_band_size=max(4, target_length // 6),
    )


def save_template(template: MotionTemplate, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(asdict(template), f, ensure_ascii=False, indent=2)


def load_template(template_path: Path) -> MotionTemplate:
    with template_path.open("r", encoding="utf-8") as f:
        return MotionTemplate(**json.load(f))
