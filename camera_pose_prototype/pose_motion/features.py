from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np

from .constants import ANGLE_ORDER, ANGLE_TRIPLETS, LANDMARK_INDEX, LANDMARK_ORDER, LEFT_RIGHT_PAIRS


@dataclass(slots=True)
class PoseFeature:
    feature: np.ndarray
    mirrored_feature: np.ndarray
    visibility: float
    coords_2d: dict[str, np.ndarray]
    mirrored_coords_2d: dict[str, np.ndarray]
    coords_3d: dict[str, np.ndarray]
    mirrored_coords_3d: dict[str, np.ndarray]


def _angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    ba = a - b
    bc = c - b
    denom = np.linalg.norm(ba) * np.linalg.norm(bc)
    if denom < 1e-6:
        return 0.0
    cosine = np.clip(np.dot(ba, bc) / denom, -1.0, 1.0)
    return math.acos(cosine) / math.pi


def _rotate(coords: dict[str, np.ndarray], angle: float) -> dict[str, np.ndarray]:
    c = math.cos(angle)
    s = math.sin(angle)
    rot = np.array([[c, -s], [s, c]], dtype=np.float32)
    return {name: rot @ point for name, point in coords.items()}


def _build_feature(coords_2d: dict[str, np.ndarray], coords_3d: dict[str, np.ndarray]) -> np.ndarray:
    xy = []
    for name in LANDMARK_ORDER:
        xy.extend(coords_2d[name].tolist())

    angles = []
    for name in ANGLE_ORDER:
        a_name, b_name, c_name = ANGLE_TRIPLETS[name]
        angles.append(_angle(coords_2d[a_name], coords_2d[b_name], coords_2d[c_name]))

    return np.asarray(xy + angles, dtype=np.float32)


def _mirror_coords(coords: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    mirrored = {name: point.copy() for name, point in coords.items()}
    for left_name, right_name in LEFT_RIGHT_PAIRS:
        left_point = coords[right_name].copy()
        right_point = coords[left_name].copy()
        left_point[0] *= -1.0
        right_point[0] *= -1.0
        mirrored[left_name] = left_point
        mirrored[right_name] = right_point

    mirrored["nose"] = mirrored["nose"].copy()
    mirrored["nose"][0] *= -1.0
    return mirrored


def _normalize_world_coords(world_selected: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    shoulder_center = (world_selected["left_shoulder"] + world_selected["right_shoulder"]) / 2.0
    hip_center = (world_selected["left_hip"] + world_selected["right_hip"]) / 2.0
    shoulder_width = np.linalg.norm(world_selected["left_shoulder"] - world_selected["right_shoulder"])
    hip_width = np.linalg.norm(world_selected["left_hip"] - world_selected["right_hip"])
    torso_len = np.linalg.norm(shoulder_center - hip_center)
    scale = max(shoulder_width, hip_width, torso_len * 1.5, 1e-4)
    return {name: (point - hip_center) / scale for name, point in world_selected.items()}


def _coords_from_landmarks(
    landmarks: Iterable,
    world_landmarks: Iterable | None = None,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], float] | None:
    selected_2d = {}
    visibilities = []
    for name, idx in LANDMARK_INDEX.items():
        landmark = landmarks[idx]
        selected_2d[name] = np.asarray([landmark.x, landmark.y], dtype=np.float32)
        visibilities.append(float(getattr(landmark, "visibility", 1.0)))

    shoulder_center = (selected_2d["left_shoulder"] + selected_2d["right_shoulder"]) / 2.0
    hip_center = (selected_2d["left_hip"] + selected_2d["right_hip"]) / 2.0
    shoulder_width = np.linalg.norm(selected_2d["left_shoulder"] - selected_2d["right_shoulder"])
    hip_width = np.linalg.norm(selected_2d["left_hip"] - selected_2d["right_hip"])
    torso_len = np.linalg.norm(shoulder_center - hip_center)
    scale = max(shoulder_width, hip_width, torso_len * 1.5, 1e-4)

    coords_2d = {name: (point - hip_center) / scale for name, point in selected_2d.items()}

    torso = shoulder_center - hip_center
    align_angle = math.atan2(float(torso[0]), float(-torso[1]))
    coords_2d = _rotate(coords_2d, -align_angle)

    if world_landmarks is not None:
        world_selected = {}
        for name, idx in LANDMARK_INDEX.items():
            landmark = world_landmarks[idx]
            world_selected[name] = np.asarray([landmark.x, landmark.y, landmark.z], dtype=np.float32)
        coords_3d = _normalize_world_coords(world_selected)
    else:
        coords_3d = {name: np.asarray([p[0], p[1], 0.0], dtype=np.float32) for name, p in coords_2d.items()}

    return coords_2d, coords_3d, float(np.mean(visibilities))


def create_pose_feature(
    landmarks: Iterable,
    world_landmarks: Iterable | None = None,
    min_visibility: float = 0.4,
) -> PoseFeature | None:
    payload = _coords_from_landmarks(landmarks, world_landmarks=world_landmarks)
    if payload is None:
        return None

    coords_2d, coords_3d, visibility = payload
    if visibility < min_visibility:
        return None

    mirrored_coords_2d = _mirror_coords(coords_2d)
    mirrored_coords_3d = _mirror_coords(coords_3d)
    return PoseFeature(
        feature=_build_feature(coords_2d, coords_3d),
        mirrored_feature=_build_feature(mirrored_coords_2d, mirrored_coords_3d),
        visibility=visibility,
        coords_2d=coords_2d,
        mirrored_coords_2d=mirrored_coords_2d,
        coords_3d=coords_3d,
        mirrored_coords_3d=mirrored_coords_3d,
    )


def interpolate_sequence(sequence: np.ndarray, target_len: int) -> np.ndarray:
    if len(sequence) == target_len:
        return sequence.astype(np.float32, copy=True)

    src_x = np.linspace(0.0, 1.0, num=len(sequence), dtype=np.float32)
    dst_x = np.linspace(0.0, 1.0, num=target_len, dtype=np.float32)
    out = np.empty((target_len, sequence.shape[1]), dtype=np.float32)
    for col in range(sequence.shape[1]):
        out[:, col] = np.interp(dst_x, src_x, sequence[:, col]).astype(np.float32)
    return out


def smooth_sequence(sequence: np.ndarray, alpha: float = 0.45) -> np.ndarray:
    if len(sequence) == 0:
        return sequence
    smoothed = np.empty_like(sequence, dtype=np.float32)
    smoothed[0] = sequence[0]
    for i in range(1, len(sequence)):
        smoothed[i] = alpha * sequence[i] + (1.0 - alpha) * smoothed[i - 1]
    return smoothed
