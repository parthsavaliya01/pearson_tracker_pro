from config import LINE_POSITION, INSIDE_DIRECTION, FRAME_WIDTH, EDGE_MARGIN


class PeopleCounter:
    def __init__(self):
        self.unique_ids = set()
        self.active_ids = set()

        self.prev_cx: dict[int, float] = {}

        self.pending: dict[int, str] = {}

        self.enter_count = 0
        self.exit_count  = 0

    @staticmethod
    def _foot_cx(box):
        x1, y1, x2, y2 = box
        return (x1 + x2) / 2.0

    def _near_edge(self, cx: float) -> bool:
        """Returns True if foot is near the left or right frame edge."""
        return cx < EDGE_MARGIN or cx > (FRAME_WIDTH - EDGE_MARGIN)

    def _confirm(self, track_id: int):
        """Commit a pending crossing as a real count."""
        direction = self.pending.pop(track_id, None)
        if direction == 'enter':
            self.enter_count += 1
        elif direction == 'exit':
            self.exit_count += 1

    def _cancel(self, track_id: int):
        """Person reversed — discard the pending crossing."""
        self.pending.pop(track_id, None)

    def update(self, boxes, ids):
        current_ids = set()

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

            crossed_toward_inside  = (prev > line) and (cx <= line)  # right→left
            crossed_toward_outside = (prev < line) and (cx >= line)  # left→right

            if INSIDE_DIRECTION == 'left':

                crossed_entry = crossed_toward_inside
                crossed_exit  = crossed_toward_outside
            else:
                # moving left→right = entering
                crossed_entry = crossed_toward_outside
                crossed_exit  = crossed_toward_inside

            # ── stage 1: line was just crossed ────────────────────────
            if track_id not in self.pending:
                if crossed_entry:
                    self.pending[track_id] = 'enter'
                elif crossed_exit:
                    self.pending[track_id] = 'exit'

            elif track_id in self.pending:
                pending_dir = self.pending[track_id]

                if pending_dir == 'enter' and crossed_exit:
                    self._cancel(track_id)
                elif pending_dir == 'exit' and crossed_entry:
                    self._cancel(track_id)

                elif self._near_edge(cx):
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
            len(current_ids),
            self.enter_count,
            self.exit_count,
        )
