import pygame
import sys
from tkinter import messagebox

pygame.display.set_caption("Path finder visualiser using Dijkstra's algorithm")
pygame.init()

# -Colors-
GREY = (190, 190, 190)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)
ORANGE = (255,69,0)
PURPLE = (160, 32, 240)
BLUE = (0, 0, 255)

# -Dimensions-
WIDTH, HEIGHT = 500,500
ROWS, COLUMNS = 50, 50
MARGIN = 2
BLOCK_WIDTH = WIDTH // ROWS
BLOCK_HEIGHT = HEIGHT // COLUMNS
screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
  
class Block():

    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.end = False
        self.wall = False
        self.queued = False
        self.visited = False
        self.previous = None
        self.neighbours = []

    def draw_grid(self, screen, color):
        pygame.draw.rect(screen, color, (self.x*BLOCK_WIDTH, self.y*BLOCK_HEIGHT, BLOCK_WIDTH-MARGIN, BLOCK_HEIGHT-MARGIN))     
    
    def update_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x-1][self.y])
        if self.x < COLUMNS-1:
            self.neighbours.append(grid[self.x+1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y-1])
        if self.y < ROWS-1:
            self.neighbours.append(grid[self.x][self.y+1])
    
     
# -Create the grid with boxes-
grid = []
for i in range(ROWS):
    arr = []
    for j in range(COLUMNS):
        arr.append(Block(i,j))
    grid.append(arr)

# -Set neighbours-
queue = []
path = []
for i in range(ROWS):
    for j in range(COLUMNS):
        grid[i][j].update_neighbours()

def main(): 

    instructions = True
    start_search = False
    searching = True
    start_block_placed = False
    end_block_placed = False
    end_block = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == pygame.MOUSEMOTION: #Can drag the click to place multiple blocks at once
                x = pygame.mouse.get_pos()[0] #gets position in x grid coordinate format
                y = pygame.mouse.get_pos()[1] #gets position in y grid coordinate format

                # -Draw wall-
                if event.buttons[2]: #Right click
                    i = x // BLOCK_WIDTH
                    j = y // BLOCK_HEIGHT
                    grid[i][j].wall = True
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                x = pygame.mouse.get_pos()[0] 
                y = pygame.mouse.get_pos()[1] 

                i = x // BLOCK_WIDTH
                j = y // BLOCK_HEIGHT

                # -Draw start node-
                if pygame.mouse.get_pressed()[0] and not start_block_placed: #Left click and no end block placed
                    i = x // BLOCK_WIDTH
                    j = y // BLOCK_HEIGHT
                    start_block = grid[i][j]
                    start_block.start = True 
                    start_block_placed = True
                    queue.append(start_block)

                # -Draw end target-
                elif pygame.mouse.get_pressed()[0] and not end_block_placed and start_block_placed: #Left click and no end block placed
                    i = x // BLOCK_WIDTH
                    j = y // BLOCK_HEIGHT
                    end_block = grid[i][j]
                    end_block.end = True 
                    end_block_placed = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and end_block_placed:
                    start_search = True

                if event.key == pygame.K_c:
                    for i in range(ROWS):
                        for j in range(COLUMNS):
                            block = grid[i][j]
                            block.visited = False
                            block.wall = False
                            block.queued = False
                            block.start = False
                            block.end = False
                            start_block_placed = False
                            end_block_placed = False
                            searching = True
                            start_search = False
                            for node in path:
                                path.pop()
                            for node in queue:
                                queue.pop()
        if start_search:
            if len(queue)>0 and searching:
                current_node = queue.pop(0)
                current_node.visited = True
                if current_node == end_block:
                    searching = False
                                                
                    while current_node.previous != start_block:
                        path.append(current_node.previous)
                        current_node = current_node.previous

                else:
                    for node in current_node.neighbours:
                        if not node.queued and not node.wall:
                            node.queued = True
                            node.previous = current_node
                            queue.append(node)
                            
            
            else:
                if searching:
                    messagebox.showerror("showerror", "Cannot reach the target block!")
                    searching = False
                      

        # -Margin color-
        screen.fill(GREY)

        # -Draw grid-
        for i in range(ROWS):
            for j in range(COLUMNS):
                block = grid[i][j]
                block.draw_grid(screen, WHITE)
                if block.queued:
                    block.draw_grid(screen, RED)    
                if block.visited:
                    block.draw_grid(screen, GREEN)
                if block in path:
                    block.draw_grid(screen, BLUE)
                if block.start:
                    block.draw_grid(screen, PURPLE)
                if block.end:
                    block.draw_grid(screen, ORANGE)
                if block.wall:
                    block.draw_grid(screen, BLACK)
        
        # -Instructions message box-
        if instructions:
            messagebox.showinfo('showinfo', 'Left click to place start block and end block\n\nDrag right click to place wall\n\nPress space to start search\n\nPress c to clear grid')
            instructions = False

        # -Update-
        pygame.display.flip()

        
        
if __name__ == '__main__':
    main()