import numpy as np
from config import LINE_POSITION

class PeopleCounter:
    def __init__(self):
        self.unique_ids = set()
        self.id_mapping = {}
        self.next_unique_id = 0

        self.previous_positions = {}
        self.id_last_seen = {}

        self.frame_count = 0

        self.crossed_ids = set()
        self.enter_count = 0
        self.exit_count = 0

    def _get_center(self, box):
        x1, y1, x2, y2 = box
        return int((x1 + x2) / 2), int((y1 + y2) / 2)

    def update(self, boxes, ids):
        self.frame_count += 1

        if ids is None or len(ids) == 0:
            return len(self.unique_ids), 0, self.enter_count, self.exit_count

        current_ids = set()

        for box, tracker_id in zip(boxes, ids):
            tracker_id = int(tracker_id)
            cx, cy = self._get_center(box)

            if tracker_id not in self.id_mapping:
                matched = False
                for stable_id, (px, py) in self.previous_positions.items():
                    dist = np.hypot(cx - px, cy - py)

                    if dist < 30:
                        self.id_mapping[tracker_id] = stable_id
                        matched = True
                        break

                if not matched:
                    self.id_mapping[tracker_id] = self.next_unique_id
                    self.next_unique_id += 1

            stable_id = self.id_mapping[tracker_id]

            self.unique_ids.add(stable_id)
            current_ids.add(stable_id)

            if stable_id in self.previous_positions:
                prev_x, prev_y = self.previous_positions[stable_id]

                if prev_x < LINE_POSITION and cx >= LINE_POSITION:
                    if stable_id not in self.crossed_ids:
                        self.enter_count += 1
                        self.crossed_ids.add(stable_id)

                elif prev_x > LINE_POSITION and cx <= LINE_POSITION:
                    if stable_id not in self.crossed_ids:
                        self.exit_count += 1
                        self.crossed_ids.add(stable_id)

            self.previous_positions[stable_id] = (cx, cy)
            self.id_last_seen[stable_id] = self.frame_count

        to_delete = []
        for sid, last_seen in self.id_last_seen.items():
            if self.frame_count - last_seen > 20:
                to_delete.append(sid)

        for sid in to_delete:
            self.previous_positions.pop(sid, None)
            self.id_last_seen.pop(sid, None)
            self.crossed_ids.discard(sid)

        return len(self.unique_ids), len(current_ids), self.enter_count, self.exit_count