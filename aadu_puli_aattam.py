import pygame
import sys
import random
from dataclasses import dataclass

# ============================================================
# AADU PULI AATTAM
# Digital Tiger and Goat Strategy Game
#
# Player  : Goats
# Computer: Tigers
#
# Phase 1 : Player places 15 goats
# Phase 2 : Player moves goats / computer moves tigers
#
# Controls:
#   Mouse       -> Select and move goats
#   R           -> Restart
#   ESC         -> Exit
# ============================================================


# ============================================================
# 1. INITIALIZATION
# ============================================================

pygame.init()

WIDTH = 1000
HEIGHT = 760

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aadu Puli Aattam")

clock = pygame.time.Clock()
FPS = 60


# ============================================================
# 2. COLORS
# ============================================================

BACKGROUND = (245, 232, 205)
BOARD_COLOR = (105, 65, 35)
BOARD_LIGHT = (180, 135, 80)

GOAT_COLOR = (245, 245, 245)
GOAT_BORDER = (35, 35, 35)

TIGER_COLOR = (220, 105, 25)
TIGER_BORDER = (80, 35, 10)

HIGHLIGHT = (80, 190, 90)
SELECTED = (245, 200, 50)

TEXT = (45, 30, 20)
WHITE = (255, 255, 255)
RED = (190, 45, 40)

PANEL = (255, 247, 225)


# ============================================================
# 3. FONTS
# ============================================================

TITLE_FONT = pygame.font.SysFont(
    "Arial", 36, bold=True
)

HEADING_FONT = pygame.font.SysFont(
    "Arial", 25, bold=True
)

FONT = pygame.font.SysFont(
    "Arial", 20, bold=True
)

SMALL_FONT = pygame.font.SysFont(
    "Arial", 16
)


# ============================================================
# 4. GAME CONSTANTS
# ============================================================

TOTAL_GOATS = 15
TIGER_WIN_CAPTURE_COUNT = 5

GOAT = "GOAT"
TIGER = "TIGER"

PLACEMENT_PHASE = "PLACEMENT"
PLAY_PHASE = "PLAY"

PLAYER_TURN = "PLAYER"
AI_TURN = "AI"

GAME_RUNNING = "RUNNING"
GAME_OVER = "GAME_OVER"


# ============================================================
# 5. BOARD
# ============================================================
#
# The board below contains 25 playable positions.
#
# The larger number of positions allows:
#
#   3 Tigers
#   15 Goats
#
# to exist simultaneously.
#
# This is a simplified digital board inspired by
# Aadu Puli Aattam. Regional traditional boards can differ.
# ============================================================


NODE_POSITIONS = {

    0:  (500, 110),

    1:  (350, 170),
    2:  (650, 170),

    3:  (230, 250),
    4:  (380, 250),
    5:  (500, 250),
    6:  (620, 250),
    7:  (770, 250),

    8:  (300, 350),
    9:  (420, 350),
    10: (500, 350),
    11: (580, 350),
    12: (700, 350),

    13: (300, 450),
    14: (420, 450),
    15: (500, 450),
    16: (580, 450),
    17: (700, 450),

    18: (230, 550),
    19: (380, 550),
    20: (500, 550),
    21: (620, 550),
    22: (770, 550),

    23: (350, 630),
    24: (650, 630)
}


# ============================================================
# 6. BOARD CONNECTIONS
# ============================================================

EDGES = [

    # Top
    (0, 1),
    (0, 2),
    (1, 2),

    # Upper section
    (1, 3),
    (1, 4),

    (2, 6),
    (2, 7),

    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),

    # Middle
    (3, 8),
    (4, 9),
    (5, 10),
    (6, 11),
    (7, 12),

    (8, 9),
    (9, 10),
    (10, 11),
    (11, 12),

    # Middle verticals
    (8, 13),
    (9, 14),
    (10, 15),
    (11, 16),
    (12, 17),

    # Lower middle
    (13, 14),
    (14, 15),
    (15, 16),
    (16, 17),

    # Bottom section
    (13, 18),
    (14, 19),
    (15, 20),
    (16, 21),
    (17, 22),

    (18, 19),
    (19, 20),
    (20, 21),
    (21, 22),

    # Bottom
    (18, 23),
    (19, 23),
    (20, 23),

    (20, 24),
    (21, 24),
    (22, 24),

    (23, 24)
]


# ============================================================
# 7. CREATE ADJACENCY LIST
# ============================================================

ADJACENCY = {
    node: [] for node in NODE_POSITIONS
}

for a, b in EDGES:

    ADJACENCY[a].append(b)
    ADJACENCY[b].append(a)


# ============================================================
# 8. GAME DATA CLASSES
# ============================================================

@dataclass
class GameState:

    goats: set
    tigers: set

    goats_placed: int
    goats_captured: int

    phase: str
    turn: str
    status: str

    selected_goat: int | None


# ============================================================
# 9. GAME CLASS
# ============================================================

class AaduPuliAattam:

    def __init__(self):

        self.reset()

    # --------------------------------------------------------
    # RESET GAME
    # --------------------------------------------------------

    def reset(self):

        self.state = GameState(

            goats=set(),

            # Three computer-controlled tigers
            tigers={0, 3, 7},

            goats_placed=0,

            goats_captured=0,

            phase=PLACEMENT_PHASE,

            turn=PLAYER_TURN,

            status=GAME_RUNNING,

            selected_goat=None
        )

        self.message = (
            "Place your goats on empty positions."
        )

        self.ai_timer = 0

    # ========================================================
    # BOARD UTILITIES
    # ========================================================

    def is_occupied(self, node):

        return (
            node in self.state.goats
            or node in self.state.tigers
        )

    # --------------------------------------------------------

    def is_valid_node(self, node):

        return node in NODE_POSITIONS

    # --------------------------------------------------------

    def get_clicked_node(self, mouse_position):

        mx, my = mouse_position

        for node, (x, y) in NODE_POSITIONS.items():

            distance = (
                (mx - x) ** 2 +
                (my - y) ** 2
            ) ** 0.5

            if distance <= 28:

                return node

        return None

    # ========================================================
    # GOAT RULES
    # ========================================================

    def get_goat_moves(self, goat):

        if goat not in self.state.goats:

            return []

        legal_moves = []

        for neighbour in ADJACENCY[goat]:

            if not self.is_occupied(neighbour):

                legal_moves.append(neighbour)

        return legal_moves

    # ========================================================
    # TIGER RULES
    # ========================================================

    def get_tiger_moves(self, tiger):

        """
        Returns:

            [
                (destination, captured_goat),
                ...
            ]

        captured_goat = None
            -> normal movement

        captured_goat = node
            -> tiger captures goat
        """

        if tiger not in self.state.tigers:

            return []

        moves = []

        # ----------------------------------------------------
        # Normal movement
        # ----------------------------------------------------

        for neighbour in ADJACENCY[tiger]:

            if not self.is_occupied(neighbour):

                moves.append(
                    (neighbour, None)
                )

        # ----------------------------------------------------
        # Capture movement
        # ----------------------------------------------------

        for goat in ADJACENCY[tiger]:

            if goat not in self.state.goats:

                continue

            for destination in ADJACENCY[goat]:

                if destination == tiger:

                    continue

                if self.is_occupied(destination):

                    continue

                moves.append(
                    (destination, goat)
                )

        return moves

    # ========================================================
    # GAME STATE CHECKS
    # ========================================================

    def tiger_has_moves(self):

        for tiger in self.state.tigers:

            if self.get_tiger_moves(tiger):

                return True

        return False

    # --------------------------------------------------------

    def check_winner(self):

        if (
            self.state.goats_captured
            >= TIGER_WIN_CAPTURE_COUNT
        ):

            self.end_game(
                "TIGERS WIN!"
            )

            return True

        if (
            self.state.phase == PLAY_PHASE
            and not self.tiger_has_moves()
        ):

            self.end_game(
                "GOATS WIN!"
            )

            return True

        return False

    # ========================================================
    # GAME END
    # ========================================================

    def end_game(self, message):

        self.state.status = GAME_OVER

        self.message = message

    # ========================================================
    # GOAT PLACEMENT
    # ========================================================

    def place_goat(self, node):

        if self.state.phase != PLACEMENT_PHASE:

            return

        if self.state.turn != PLAYER_TURN:

            return

        if self.is_occupied(node):

            self.message = (
                "That position is occupied."
            )

            return

        # Place goat
        self.state.goats.add(node)

        self.state.goats_placed += 1

        # ----------------------------------------------------
        # All goats placed
        # ----------------------------------------------------

        if (
            self.state.goats_placed
            == TOTAL_GOATS
        ):

            self.state.phase = PLAY_PHASE

            self.state.turn = PLAYER_TURN

            self.message = (
                "All goats placed! Select a goat to move."
            )

            return

        # ----------------------------------------------------
        # Continue placement
        # ----------------------------------------------------

        self.message = (
            f"Goat {self.state.goats_placed} placed. "
            f"Place goat "
            f"{self.state.goats_placed + 1}."
        )

    # ========================================================
    # GOAT MOVEMENT
    # ========================================================

    def handle_goat_click(self, node):

        if self.state.phase != PLAY_PHASE:

            return

        if self.state.turn != PLAYER_TURN:

            return

        # ----------------------------------------------------
        # No goat selected
        # ----------------------------------------------------

        if self.state.selected_goat is None:

            if node in self.state.goats:

                self.state.selected_goat = node

                self.message = (
                    "Choose a highlighted position."
                )

            else:

                self.message = (
                    "Click one of your goats."
                )

            return

        # ----------------------------------------------------
        # Goat already selected
        # ----------------------------------------------------

        selected = self.state.selected_goat

        legal_moves = self.get_goat_moves(
            selected
        )

        # ----------------------------------------------------
        # Valid destination
        # ----------------------------------------------------

        if node in legal_moves:

            self.state.goats.remove(selected)

            self.state.goats.add(node)

            self.state.selected_goat = None

            self.state.turn = AI_TURN

            self.message = (
                "Tiger is thinking..."
            )

            self.ai_timer = pygame.time.get_ticks()

            return

        # ----------------------------------------------------
        # Select another goat
        # ----------------------------------------------------

        if node in self.state.goats:

            self.state.selected_goat = node

            return

        # ----------------------------------------------------
        # Invalid selection
        # ----------------------------------------------------

        self.state.selected_goat = None

        self.message = (
            "Invalid move. Select a goat again."
        )

    # ========================================================
    # TIGER AI
    # ========================================================

    def make_ai_move(self):

        if self.state.status == GAME_OVER:

            return

        if self.state.turn != AI_TURN:

            return

        all_captures = []

        all_moves = []

        # ----------------------------------------------------
        # Find legal moves
        # ----------------------------------------------------

        for tiger in self.state.tigers:

            moves = self.get_tiger_moves(
                tiger
            )

            for destination, captured in moves:

                move = (
                    tiger,
                    destination,
                    captured
                )

                all_moves.append(move)

                if captured is not None:

                    all_captures.append(move)

        # ----------------------------------------------------
        # No legal moves
        # ----------------------------------------------------

        if not all_moves:

            self.end_game(
                "GOATS WIN!"
            )

            return

        # ----------------------------------------------------
        # Tiger prioritizes captures
        # ----------------------------------------------------

        if all_captures:

            tiger, destination, captured = (
                random.choice(all_captures)
            )

        else:

            tiger, destination, captured = (
                random.choice(all_moves)
            )

        # ----------------------------------------------------
        # Execute tiger movement
        # ----------------------------------------------------

        self.state.tigers.remove(tiger)

        self.state.tigers.add(destination)

        # ----------------------------------------------------
        # Capture goat
        # ----------------------------------------------------

        if captured is not None:

            self.state.goats.remove(
                captured
            )

            self.state.goats_captured += 1

            self.message = (
                f"Tiger captured a goat! "
                f"Captured: "
                f"{self.state.goats_captured}/"
                f"{TIGER_WIN_CAPTURE_COUNT}"
            )

        else:

            self.message = (
                "Tiger moved. Your turn."
            )

        # ----------------------------------------------------
        # Return control to player
        # ----------------------------------------------------

        self.state.turn = PLAYER_TURN

        self.check_winner()

    # ========================================================
    # HANDLE INPUT
    # ========================================================

    def handle_click(self, mouse_position):

        if self.state.status == GAME_OVER:

            return

        node = self.get_clicked_node(
            mouse_position
        )

        if node is None:

            return

        # Placement
        if self.state.phase == PLACEMENT_PHASE:

            self.place_goat(node)

        # Normal play
        elif self.state.phase == PLAY_PHASE:

            self.handle_goat_click(node)

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self):

        if self.state.status == GAME_OVER:

            return

        # ----------------------------------------------------
        # AI delay
        # ----------------------------------------------------

        if self.state.turn == AI_TURN:

            current_time = pygame.time.get_ticks()

            if current_time - self.ai_timer >= 600:

                self.make_ai_move()

    # ========================================================
    # DRAW TEXT
    # ========================================================

    def draw_text(
        self,
        text,
        position,
        font,
        color=TEXT
    ):

        image = font.render(
            text,
            True,
            color
        )

        screen.blit(
            image,
            position
        )

    # ========================================================
    # DRAW BOARD
    # ========================================================

    def draw_board(self):

        # ----------------------------------------------------
        # Background
        # ----------------------------------------------------

        screen.fill(
            BACKGROUND
        )

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        title = TITLE_FONT.render(
            "AADU PULI AATTAM",
            True,
            TEXT
        )

        screen.blit(
            title,
            (
                WIDTH // 2
                - title.get_width() // 2,
                18
            )
        )

        subtitle = SMALL_FONT.render(
            "You = GOATS    |    Computer = TIGERS",
            True,
            BOARD_COLOR
        )

        screen.blit(
            subtitle,
            (
                WIDTH // 2
                - subtitle.get_width() // 2,
                60
            )
        )

        # ----------------------------------------------------
        # Board panel
        # ----------------------------------------------------

        pygame.draw.rect(
            screen,
            PANEL,
            (120, 85, 760, 520),
            border_radius=20
        )

        # ----------------------------------------------------
        # Draw edges
        # ----------------------------------------------------

        for a, b in EDGES:

            pygame.draw.line(
                screen,
                BOARD_COLOR,
                NODE_POSITIONS[a],
                NODE_POSITIONS[b],
                5
            )

        # ----------------------------------------------------
        # Selected goat
        # ----------------------------------------------------

        selected = (
            self.state.selected_goat
        )

        if selected is not None:

            x, y = NODE_POSITIONS[selected]

            pygame.draw.circle(
                screen,
                SELECTED,
                (x, y),
                32
            )

            # Highlight legal moves
            for destination in self.get_goat_moves(
                selected
            ):

                dx, dy = NODE_POSITIONS[
                    destination
                ]

                pygame.draw.circle(
                    screen,
                    HIGHLIGHT,
                    (dx, dy),
                    17
                )

        # ----------------------------------------------------
        # Board nodes
        # ----------------------------------------------------

        for node, position in NODE_POSITIONS.items():

            pygame.draw.circle(
                screen,
                BOARD_COLOR,
                position,
                8
            )

        # ----------------------------------------------------
        # Draw goats
        # ----------------------------------------------------

        for goat in self.state.goats:

            x, y = NODE_POSITIONS[goat]

            pygame.draw.circle(
                screen,
                GOAT_COLOR,
                (x, y),
                23
            )

            pygame.draw.circle(
                screen,
                GOAT_BORDER,
                (x, y),
                23,
                3
            )

            label = SMALL_FONT.render(
                "G",
                True,
                TEXT
            )

            screen.blit(
                label,
                (
                    x - label.get_width() // 2,
                    y - label.get_height() // 2
                )
            )

        # ----------------------------------------------------
        # Draw tigers
        # ----------------------------------------------------

        for tiger in self.state.tigers:

            x, y = NODE_POSITIONS[tiger]

            pygame.draw.circle(
                screen,
                TIGER_COLOR,
                (x, y),
                27
            )

            pygame.draw.circle(
                screen,
                TIGER_BORDER,
                (x, y),
                27,
                3
            )

            label = FONT.render(
                "T",
                True,
                WHITE
            )

            screen.blit(
                label,
                (
                    x - label.get_width() // 2,
                    y - label.get_height() // 2
                )
            )

        # ====================================================
        # INFORMATION PANEL
        # ====================================================

        pygame.draw.rect(
            screen,
            PANEL,
            (30, 625, 940, 110),
            border_radius=15
        )

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        self.draw_text(
            f"Goats: "
            f"{self.state.goats_placed}/"
            f"{TOTAL_GOATS}",
            (50, 640),
            FONT
        )

        self.draw_text(
            f"Captured: "
            f"{self.state.goats_captured}/"
            f"{TIGER_WIN_CAPTURE_COUNT}",
            (50, 675),
            SMALL_FONT
        )

        # ----------------------------------------------------
        # Turn
        # ----------------------------------------------------

        turn_text = (
            "YOUR TURN"
            if self.state.turn == PLAYER_TURN
            else "TIGER THINKING..."
        )

        self.draw_text(
            turn_text,
            (350, 640),
            FONT
        )

        # ----------------------------------------------------
        # Phase
        # ----------------------------------------------------

        phase_text = (
            "PLACE GOATS"
            if self.state.phase == PLACEMENT_PHASE
            else "GAME PLAY"
        )

        self.draw_text(
            phase_text,
            (700, 640),
            FONT
        )

        # ----------------------------------------------------
        # Message
        # ----------------------------------------------------

        self.draw_text(
            self.message,
            (350, 675),
            SMALL_FONT
        )

        # ----------------------------------------------------
        # Game over
        # ----------------------------------------------------

        if self.state.status == GAME_OVER:

            self.draw_game_over()

    # ========================================================
    # GAME OVER SCREEN
    # ========================================================

    def draw_game_over(self):

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 165)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        # Determine winner
        if (
            self.state.goats_captured
            >= TIGER_WIN_CAPTURE_COUNT
        ):

            result = "TIGERS WIN!"

        else:

            result = "GOATS WIN!"

        title = TITLE_FONT.render(
            result,
            True,
            WHITE
        )

        screen.blit(
            title,
            (
                WIDTH // 2
                - title.get_width() // 2,
                HEIGHT // 2 - 60
            )
        )

        info = FONT.render(
            f"Goats captured: "
            f"{self.state.goats_captured}",
            True,
            WHITE
        )

        screen.blit(
            info,
            (
                WIDTH // 2
                - info.get_width() // 2,
                HEIGHT // 2
            )
        )

        restart = SMALL_FONT.render(
            "Press R to play again",
            True,
            WHITE
        )

        screen.blit(
            restart,
            (
                WIDTH // 2
                - restart.get_width() // 2,
                HEIGHT // 2 + 45
            )
        )


# ============================================================
# 10. MAIN PROGRAM
# ============================================================

def main():

    game = AaduPuliAattam()

    running = True

    while running:

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            # ------------------------------------------------
            # Close window
            # ------------------------------------------------

            if event.type == pygame.QUIT:

                running = False

            # ------------------------------------------------
            # Keyboard
            # ------------------------------------------------

            elif event.type == pygame.KEYDOWN:

                # Restart
                if event.key == pygame.K_r:

                    game.reset()

                # Exit
                elif event.key == pygame.K_ESCAPE:

                    running = False

            # ------------------------------------------------
            # Mouse
            # ------------------------------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    game.handle_click(
                        event.pos
                    )

        # ====================================================
        # UPDATE
        # ====================================================

        game.update()

        # ====================================================
        # DRAW
        # ====================================================

        game.draw_board()

        pygame.display.flip()

        clock.tick(FPS)

    # ========================================================
    # EXIT
    # ========================================================

    pygame.quit()
    sys.exit()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()