from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from .template_builder import MotionTemplate


Orientation = Literal["normal", "mirror"]


@dataclass(slots=True)
class DetectionEvent:
    count: int
    standard: bool
    score: float


@dataclass(slots=True)
class MatchStatus:
    phase: str
    count: int
    last_standard: bool | None
    current_orientation: Orientation | None
    current_index: int | None
    current_distance: float | None
    progress: float
    event: DetectionEvent | None = None


class ActionMatcher:
    def __init__(self, template: MotionTemplate) -> None:
        self.template = template
        self.sequence = template.sequence_array
        self.mirror_sequence = template.mirror_sequence_array
        self.reset()

    def reset(self) -> None:
        self.phase = "idle"
        self.count = 0
        self.last_standard = None
        self.orientation: Orientation | None = None
        self.start_hits = 0
        self.cooldown = 0
        self.current_index = 0
        self.max_index = 0
        self.segment_distances: list[float] = []
        self.frames_in_segment = 0
        self.current_distance: float | None = None
        self.missing_frames = 0

    def _start_distance(self, feature: np.ndarray) -> tuple[Orientation, float]:
        normal = float(np.linalg.norm(feature - self.template.start_pose_array))
        mirror = float(np.linalg.norm(feature - self.template.mirror_start_pose_array))
        if normal <= mirror:
            return "normal", normal
        return "mirror", mirror

    def _advance_index(self, feature: np.ndarray) -> tuple[int, float]:
        assert self.orientation is not None
        sequence = self.sequence if self.orientation == "normal" else self.mirror_sequence
        upper = min(
            len(sequence) - 1,
            self.current_index + self.template.max_advance_per_frame,
        )
        lower = max(0, self.current_index - 1)
        candidates = range(lower, upper + 1)
        best_index = self.current_index
        best_distance = float("inf")
        for idx in candidates:
            distance = float(np.linalg.norm(feature - sequence[idx]))
            if distance < best_distance:
                best_index = idx
                best_distance = distance
        return best_index, best_distance

    def update(self, feature: np.ndarray | None) -> MatchStatus:
        if feature is None:
            self.missing_frames += 1
            if self.phase == "tracking" and self.missing_frames <= 2:
                progress = self.max_index / max(1, self.template.template_length - 1)
                return MatchStatus(
                    phase=self.phase,
                    count=self.count,
                    last_standard=self.last_standard,
                    current_orientation=self.orientation,
                    current_index=self.current_index,
                    current_distance=self.current_distance,
                    progress=progress,
                    event=None,
                )
            if self.phase == "tracking":
                self.phase = "idle"
                self.orientation = None
                self.start_hits = 0
                self.segment_distances.clear()
                self.frames_in_segment = 0
                self.current_index = 0
                self.max_index = 0
                self.current_distance = None
            return MatchStatus(
                phase=self.phase,
                count=self.count,
                last_standard=self.last_standard,
                current_orientation=self.orientation,
                current_index=None,
                current_distance=None,
                progress=0.0,
                event=None,
            )

        self.missing_frames = 0
        event = None
        start_orientation, start_distance = self._start_distance(feature)

        if self.phase == "cooldown":
            self.cooldown = max(0, self.cooldown - 1)
            if start_distance <= self.template.start_threshold:
                self.start_hits += 1
                if self.cooldown == 0 and self.start_hits >= self.template.start_hold_frames:
                    self.phase = "tracking"
                    self.orientation = start_orientation
                    self.current_index = 0
                    self.max_index = 0
                    self.segment_distances = []
                    self.frames_in_segment = 0
                    self.start_hits = 0
            elif start_distance > self.template.start_threshold:
                self.start_hits = 0

        elif self.phase == "idle":
            if start_distance <= self.template.start_threshold:
                if self.orientation == start_orientation or self.orientation is None:
                    self.start_hits += 1
                else:
                    self.start_hits = 1
                self.orientation = start_orientation
                if self.start_hits >= self.template.start_hold_frames:
                    self.phase = "tracking"
                    self.current_index = 0
                    self.max_index = 0
                    self.segment_distances = []
                    self.frames_in_segment = 0
                    self.start_hits = 0
            else:
                self.start_hits = 0
                self.orientation = None

        if self.phase == "tracking":
            idx, distance = self._advance_index(feature)
            self.current_index = idx
            self.current_distance = distance
            self.max_index = max(self.max_index, idx)
            self.segment_distances.append(distance)
            self.frames_in_segment += 1

            progress = self.max_index / max(1, self.template.template_length - 1)
            end_band_start = self.template.template_length - self.template.end_band_size

            if progress >= self.template.coverage_threshold and idx >= end_band_start:
                avg_distance = float(np.mean(self.segment_distances))
                if avg_distance <= self.template.match_threshold:
                    standard = avg_distance <= self.template.standard_threshold
                    self.count += 1
                    self.last_standard = standard
                    event = DetectionEvent(
                        count=self.count,
                        standard=standard,
                        score=avg_distance,
                    )
                    self.phase = "cooldown"
                    self.cooldown = self.template.cooldown_frames
                    self.current_index = 0
                    self.max_index = 0
                    self.segment_distances = []
                    self.frames_in_segment = 0
                    self.current_distance = avg_distance
                elif self.frames_in_segment > self.template.template_length * 2:
                    self.phase = "idle"
                    self.orientation = None
                    self.current_index = 0
                    self.max_index = 0
                    self.segment_distances = []
                    self.frames_in_segment = 0
                    self.current_distance = None

        progress = 0.0
        if self.phase == "tracking":
            progress = self.max_index / max(1, self.template.template_length - 1)

        return MatchStatus(
            phase=self.phase,
            count=self.count,
            last_standard=self.last_standard,
            current_orientation=self.orientation,
            current_index=self.current_index if self.phase == "tracking" else None,
            current_distance=self.current_distance,
            progress=progress,
            event=event,
        )
