from generators import MazeGeneratorDFS
from solvers import MazeSolverDFS
from graphic import MlxMazeRenderer, MlxAPI
from dataclasses import dataclass


@dataclass
class SpeedConfig:
    value: float = 0.5
    slowest_sec: float = 5.0
    fastest_sec: float = 0.005
    fps: int = 60

    def get_gears(self) -> tuple[int, int]:
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


class MazeSolverApp:
    def __init__(self, dims=(31, 21), size=20):
        self.dims, self.size = dims, size
        self.speed = SpeedConfig()
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
        self.full_path = MazeSolverDFS().solve(self.maze)
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
        delay, steps = self.speed.get_gears()
        self.frame_counter += 1
        if self.frame_counter >= delay:
            self.frame_counter = 0
            for _ in range(steps):
                try:
                    self.current_path.add(next(self.step_iterator))
                except StopIteration:
                    self.finished = True
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
