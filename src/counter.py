from config import EDGE_MARGIN, FRAME_WIDTH, INSIDE_DIRECTION, LINE_POSITION


class PeopleCounter:
    def __init__(self):
        self.unique_ids = set()
        self.active_ids = set()
        self.prev_cx: dict[int, float] = {}
        self.pending: dict[int, dict[str, int]] = {}
        self.enter_count = 0
        self.exit_count = 0
        self.current_occupancy = 0
        self.frame_count = 0

    @staticmethod
    def _foot_cx(box):
        x1, y1, x2, y2 = box
        return (x1 + x2) / 2.0

    def _near_edge(self, cx: float) -> bool:
        return cx < EDGE_MARGIN or cx > (FRAME_WIDTH - EDGE_MARGIN)

    def _confirm(self, track_id: int):
        pending = self.pending.pop(track_id, None)
        if not pending:
            return

        if pending["direction"] == "enter":
            self.enter_count += 1
            self.current_occupancy = max(0, self.current_occupancy + 1)
        elif pending["direction"] == "exit":
            self.exit_count += 1
            self.current_occupancy = max(0, self.current_occupancy - 1)

    def _cancel(self, track_id: int):
        self.pending.pop(track_id, None)

    def update(self, boxes, ids):
        current_ids = set()
        self.frame_count += 1

        for box, track_id in zip(boxes, ids):
            track_id = int(track_id)
            current_ids.add(track_id)
            cx = self._foot_cx(box)

            if track_id not in self.active_ids:
                self.unique_ids.add(track_id)
                self.active_ids.add(track_id)
                self.prev_cx[track_id] = cx
                continue

            prev = self.prev_cx.get(track_id, cx)
            line = float(LINE_POSITION)
            crossed_toward_inside = (prev > line) and (cx <= line)
            crossed_toward_outside = (prev < line) and (cx >= line)

            if INSIDE_DIRECTION == "left":
                crossed_entry = crossed_toward_inside
                crossed_exit = crossed_toward_outside
            else:
                crossed_entry = crossed_toward_outside
                crossed_exit = crossed_toward_inside

            if track_id not in self.pending:
                if crossed_entry:
                    self.pending[track_id] = {"direction": "enter", "frame": self.frame_count}
                elif crossed_exit:
                    self.pending[track_id] = {"direction": "exit", "frame": self.frame_count}
            else:
                pending = self.pending[track_id]
                if pending["direction"] == "enter" and crossed_exit:
                    self._cancel(track_id)
                elif pending["direction"] == "exit" and crossed_entry:
                    self._cancel(track_id)
                elif self._near_edge(cx) or (self.frame_count - pending["frame"]) >= 2:
                    self._confirm(track_id)

            self.prev_cx[track_id] = cx

        lost = self.active_ids - current_ids
        for tid in lost:
            if tid in self.pending:
                self._confirm(tid)
            self.prev_cx.pop(tid, None)
        self.active_ids -= lost

        return (
            len(self.unique_ids),
            self.current_occupancy,
            self.enter_count,
            self.exit_count,
        )
