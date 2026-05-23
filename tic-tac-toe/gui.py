import pygame
import sys

WIDTH, HEIGHT = 1280, 720
PANEL_WIDTH = 280
BOARD_SIZE = 480
CELL_SIZE = BOARD_SIZE // 3
BOARD_LEFT = (WIDTH - BOARD_SIZE) // 2
BOARD_TOP = (HEIGHT - BOARD_SIZE) // 2

CLAUDE_ORANGE = (207, 98,  42)   # #CF622A — Claude brand orange
CLAUDE_DARK   = (45,  35,  25)   # near-black warm
BG            = (250, 248, 245)  # warm white
PANEL_BG      = (243, 239, 233)  # warm off-white
BOARD_BG      = (255, 255, 255)  # pure white
GRID          = CLAUDE_ORANGE
X_COLOR       = CLAUDE_ORANGE
O_COLOR       = CLAUDE_DARK
WHITE         = (255, 255, 255)
GOLD          = CLAUDE_ORANGE
DIM           = (160, 145, 130)  # warm muted


class GameRenderer:

    def __init__(self, x_name: str, o_name: str):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption("Agent Arena — Tic Tac Toe")
        self.x_name = x_name
        self.o_name = o_name
        self.clock = pygame.time.Clock()
        self.font_large  = pygame.font.SysFont("Georgia", 32, bold=True)
        self.font_medium = pygame.font.SysFont("Georgia", 20)
        self.font_small  = pygame.font.SysFont("Arial",   15)

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def _draw_panel(self, name: str, marker: str, reasoning: str, x: int, is_active: bool) -> None:
        color = X_COLOR if marker == "X" else O_COLOR
        panel_rect = pygame.Rect(x, 0, PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)
        if is_active:
            pygame.draw.rect(self.screen, GOLD, panel_rect, 3)

        name_surf = self.font_large.render(name, True, color)
        self.screen.blit(name_surf, (x + (PANEL_WIDTH - name_surf.get_width()) // 2, 20))

        badge = self.font_medium.render(f"Playing as {marker}", True, CLAUDE_DARK)
        self.screen.blit(badge, (x + (PANEL_WIDTH - badge.get_width()) // 2, 65))

        pygame.draw.line(self.screen, color, (x + 20, 100), (x + PANEL_WIDTH - 20, 100), 2)

        label = self.font_small.render("REASONING", True, DIM)
        self.screen.blit(label, (x + 20, 115))

        if reasoning:
            lines = self._wrap_text(reasoning, self.font_small, PANEL_WIDTH - 40)
            y = 140
            for line in lines:
                if y > HEIGHT - 30:
                    break
                self.screen.blit(self.font_small.render(line, True, CLAUDE_DARK), (x + 20, y))
                y += 20

    def _draw_board(self, board: list[list[str | None]]) -> None:
        pygame.draw.rect(self.screen, BOARD_BG,
                         pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_SIZE, BOARD_SIZE),
                         border_radius=12)

        for i in range(1, 3):
            x = BOARD_LEFT + i * CELL_SIZE
            pygame.draw.line(self.screen, GRID, (x, BOARD_TOP + 20), (x, BOARD_TOP + BOARD_SIZE - 20), 3)
            y = BOARD_TOP + i * CELL_SIZE
            pygame.draw.line(self.screen, GRID, (BOARD_LEFT + 20, y), (BOARD_LEFT + BOARD_SIZE - 20, y), 3)

        pad = 30
        for r in range(3):
            for c in range(3):
                cell = board[r][c]
                if cell is None:
                    continue
                cx = BOARD_LEFT + c * CELL_SIZE + CELL_SIZE // 2
                cy = BOARD_TOP  + r * CELL_SIZE + CELL_SIZE // 2
                if cell == "X":
                    pygame.draw.line(self.screen, X_COLOR,
                                     (cx - CELL_SIZE // 2 + pad, cy - CELL_SIZE // 2 + pad),
                                     (cx + CELL_SIZE // 2 - pad, cy + CELL_SIZE // 2 - pad), 8)
                    pygame.draw.line(self.screen, X_COLOR,
                                     (cx + CELL_SIZE // 2 - pad, cy - CELL_SIZE // 2 + pad),
                                     (cx - CELL_SIZE // 2 + pad, cy + CELL_SIZE // 2 - pad), 8)
                else:
                    pygame.draw.circle(self.screen, O_COLOR, (cx, cy), CELL_SIZE // 2 - pad, 8)

    def _draw_header(self, current_marker: str) -> None:
        title = self.font_medium.render("AGENT ARENA", True, CLAUDE_ORANGE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))
        if current_marker:
            name  = self.x_name if current_marker == "X" else self.o_name
            color = X_COLOR    if current_marker == "X" else O_COLOR
            turn  = self.font_small.render(f"{name}'s turn", True, color)
            self.screen.blit(turn, (WIDTH // 2 - turn.get_width() // 2, 45))

    def draw(self, board: list[list[str | None]], x_reasoning: str, o_reasoning: str, current_marker: str) -> None:
        self.screen.fill(BG)
        self._draw_header(current_marker)
        self._draw_panel(self.x_name, "X", x_reasoning, 0,              current_marker == "X")
        self._draw_panel(self.o_name, "O", o_reasoning, WIDTH - PANEL_WIDTH, current_marker == "O")
        self._draw_board(board)
        pygame.display.flip()
        self.clock.tick(60)

    def _draw_overlay(self, message: str, color: tuple[int, int, int]) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((250, 248, 245, 200))
        self.screen.blit(overlay, (0, 0))
        text = self.font_large.render(message, True, CLAUDE_DARK)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 30))
        pygame.display.flip()

    def draw_winner(self, board: list[list[str | None]], winner_name: str, x_reasoning: str, o_reasoning: str) -> None:
        self.draw(board, x_reasoning, o_reasoning, "")
        self._draw_overlay(f"{winner_name} wins!", GOLD)

    def draw_draw(self, board: list[list[str | None]], x_reasoning: str, o_reasoning: str) -> None:
        self.draw(board, x_reasoning, o_reasoning, "")
        self._draw_overlay("It's a draw!", WHITE)

    def wait_for_close(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
