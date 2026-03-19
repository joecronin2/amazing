from TestImpl import MazeGeneratorDFS, MazeSolverDFS
import time
from graphic import MlxMazeRenderer, MlxAPI
from typing import Any, Optional, Callable
from dataclasses import dataclass


class MazeGame:
    def __init__(self, dims: tuple[int, int] = (31, 21), size: int = 20):
        self.size = size
        self.maze = MazeGeneratorDFS().generate(dims)
        self.player_pos = self.maze.start

        self.w, self.h = self.maze.width * size, self.maze.height * size

        self.api: Optional[MlxAPI] = None
        self.win: Any = None
        self.renderer: Optional[MlxMazeRenderer] = None

        self.visited: set[tuple[int, int]] = {self.player_pos}

        self.actions: dict[int, Callable[[], Any]] = {
            65361: lambda: self._move_player((-1, 0)),
            65362: lambda: self._move_player((0, -1)),
            65363: lambda: self._move_player((1, 0)),
            65364: lambda: self._move_player((0, 1)),
            65307: self._exit,
        }

    def _move_player(self, d: tuple[int, int]) -> None:
        n = (self.player_pos[0] + d[0], self.player_pos[1] + d[1])
        if self.maze.in_bounds(n) and not self.maze.is_wall(n):
            self.player_pos = n
            self.visited.add(n)
            if n == self.maze.end:
                self._exit()

    def _setup_hooks(self) -> None:
        if not self.api or not self.win:
            return
        api, win = self.api, self.win
        api.on_key_down(win, self._handle_input, self)
        api.on_close(win, lambda _: api.loop_exit())
        api.on_loop(self._update, self)

    def _handle_input(self, code: int, _) -> None:
        if action := self.actions.get(code):
            action()

    def _update(self, _) -> int:
        if self.renderer:
            self.renderer.render(self.player_pos, self.visited)
        return 0

    def _exit(self) -> None:
        if self.api:
            self.api.loop_exit()

    def run(self) -> None:
        with MlxAPI() as api:
            self.api = api
            self.win = api.create_window((self.w, self.h), "A-Maze-Ing")
            self.renderer = MlxMazeRenderer(api, self.win, self.maze, self.size)
            self._setup_hooks()
            api.loop()


@dataclass
class SpeedConfig:
    value: float = 0.5
    slowest_sec: float = 5.0
    fastest_sec: float = 0.005
    fps: int = 60

    def get_gears(self) -> tuple[int, int]:
        """Calculates (delay_frames, steps_per_frame) using an exponential curve."""
        duration = (
            self.slowest_sec * (self.fastest_sec / self.slowest_sec) ** self.value
        )
        frame_time = 1.0 / self.fps
        if duration >= frame_time:
            delay = round(duration / frame_time)
            return max(1, delay), 1
        else:
            steps = round(frame_time / duration)
            return 1, max(1, steps)

    def adjust(self, delta: float):
        """Adjusts the speed index while keeping it in [0.0, 1.0]."""
        self.value = max(0.0, min(1.0, self.value + delta))

    def get_current_duration(self) -> float:
        return self.slowest_sec * (self.fastest_sec / self.slowest_sec) ** self.value


class SolverStats:
    def __init__(self):
        self.algo_ms = 0.0
        self.start_time: Optional[float] = None

    def record_algo(self, start: float, end: float):
        self.algo_ms = (end - start) * 1000

    def start_visual(self):
        self.start_time = time.perf_counter()

    def report(self):
        if not self.start_time:
            return
        visual_ms = (time.perf_counter() - self.start_time) * 1000
        print(f"\n--- Performance ---\nAlgo:   {self.algo_ms:.4f}ms")
        print(
            f"Visual: {visual_ms:.2f}ms\nRatio:  {visual_ms/self.algo_ms:.1f}x slower"
        )


class MazeSolverApp:
    def __init__(self, dims=(31, 21), size=20):
        self.dims, self.size = dims, size
        self.speed = SpeedConfig()
        self.stats = SolverStats()
        self.api, self.win, self.renderer = None, None, None

        self._reset_logic()
        self.speed = SpeedConfig(value=0.5)
        self.actions = {
            65307: self._exit,
            32: self._toggle_pause,
            65293: self._reset_logic,
            61: lambda: self._adjust_speed(0.05),
            45: lambda: self._adjust_speed(-0.05),
        }

    def _reset_logic(self) -> None:
        self.maze = MazeGeneratorDFS().generate(self.dims)

        t0 = time.perf_counter()
        self.full_path = MazeSolverDFS().solve(self.maze)
        self.stats.record_algo(t0, time.perf_counter())

        self.step_iterator = iter(self.full_path)
        self.current_path: set[tuple[int, int]] = set()
        self.paused = self.finished = False
        self.frame_counter = 0

        if self.renderer:
            self.renderer.maze = self.maze

    def _adjust_speed(self, delta: float):
        self.speed.adjust(delta)
        delay, steps = self.speed.get_gears()
        curr_sec = self.speed.get_current_duration()
        print(f"Target: {curr_sec:.3f}s/move | Gears: {steps} steps @ {delay}f delay")

    def _update(self, _) -> int:
        if self.paused or self.finished or not self.renderer:
            return 0
        if not self.stats.start_time:
            self.stats.start_visual()
        delay, steps = self.speed.get_gears()
        self.frame_counter += 1
        if self.frame_counter >= delay:
            self.frame_counter = 0
            for _ in range(steps):
                try:
                    self.current_path.add(next(self.step_iterator))
                except StopIteration:
                    self.finished = True
                    self.stats.report()
                    break

        self.renderer.render(active_path=self.current_path)
        return 0

    def run(self) -> None:
        w, h = self.maze.width * self.size, self.maze.height * self.size
        with MlxAPI() as api:
            self.api = api
            self.win = api.create_window((w, h), "Maze Benchmark")
            self.renderer = MlxMazeRenderer(api, self.win, self.maze, self.size)
            api.on_key_down(
                self.win, lambda c, _: self.actions.get(c, lambda: None)(), self
            )
            api.on_loop(self._update, self)
            api.loop()

    def _toggle_pause(self):
        self.paused = not self.paused

    def _exit(self):
        self.api.loop_exit() if self.api else None


def main():
    app = MazeSolverApp()
    app.run()


if __name__ == "__main__":
    main()
