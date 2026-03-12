from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlretrieve

import cv2
import mediapipe as mp

from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python import vision

from .features import PoseFeature, create_pose_feature


MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
    "pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
)


@dataclass(slots=True)
class ExtractedFrame:
    index: int
    timestamp_ms: int
    pose: PoseFeature | None


def ensure_pose_model(model_path: Path) -> Path:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    if not model_path.exists():
        urlretrieve(MODEL_URL, model_path)
    return model_path


class PoseExtractor:
    def __init__(self, model_path: Path | None = None) -> None:
        model_path = ensure_pose_model(
            model_path or Path.home() / ".pose-prototype" / "models" / "pose_landmarker_lite.task"
        )
        options = vision.PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(model_path)),
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            output_segmentation_masks=False,
        )
        self._landmarker = vision.PoseLandmarker.create_from_options(options)

    def close(self) -> None:
        self._landmarker.close()

    def extract(self, frame_bgr, index: int, timestamp_ms: int) -> ExtractedFrame:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self._landmarker.detect_for_video(mp_image, timestamp_ms)

        pose_feature = None
        if result.pose_landmarks:
            world_landmarks = result.pose_world_landmarks[0] if result.pose_world_landmarks else None
            pose_feature = create_pose_feature(result.pose_landmarks[0], world_landmarks=world_landmarks)
        return ExtractedFrame(index=index, timestamp_ms=timestamp_ms, pose=pose_feature)
