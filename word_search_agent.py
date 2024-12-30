from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


class WordSearchAgent:
    def __init__(self, driver, grid_size):
        self.driver = driver
        self.grid_size = grid_size
        self.grid = [[''] * grid_size[1] for _ in range(grid_size[0])]
        self.words = set()

        self.colors = ["#FF6347", "#4682B4", "#32CD32", "#FFD700", "#8A2BE2", "#D2691E", "#FF4500", "#20B2AA", "#FFD700", "#FF1493"]
        self.found_words = set()

    def read_grid(self):
        n, m = self.grid_size
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Grid_gridCell__1L1O2"]'))
            )

            for i in range(n):
                for j in range(m):
                    cell = self.driver.find_element(by=By.XPATH, value=f'//div[@class="Grid_gridCell__1L1O2" and @row="{i}" and @col="{j}"]')
                    self.grid[i][j] = cell.text
        except Exception as e:
            print(f"Error while reading grid: {e}")

    def read_words(self):
        word_list = self.driver.find_element(by=By.XPATH, value='//div[@class="WordList_wordList__3da04"]')
        self.words = set([word.text for word in word_list.find_elements(by=By.XPATH, value='//a')])

    def agent(self, i, j, word):
        n, m = self.grid_size
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)] 
        for dx, dy in directions:
            positions = []
            x, y = i, j

            for k in range(len(word)):
                if 0 <= x < n and 0 <= y < m and self.grid[x][y] == word[k]:
                    positions.append((x, y))
                else:
                    break
                x += dx
                y += dy

            if len(positions) == len(word):
                print(f"Word found: {word}")
                print(f"Positions: {positions}")  
                color = self.get_random_color()  
                self.highlight_word(positions, color)  
                self.strike_word(word)  
                self.found_words.add(word)  
                return True
        return False

    def get_random_color(self):
        return random.choice(self.colors)

    def highlight_word(self, positions, color):
        for pos in positions:
            row, col = pos
            try:
                cell = self.driver.find_element(by=By.XPATH, value=f'//div[@class="Grid_gridCell__1L1O2" and @row="{row}" and @col="{col}"]')
                self.driver.execute_script(f"arguments[0].style.backgroundColor = '{color}';", cell)
            except Exception as e:
                print(f"Error while highlighting word at position {pos}: {e}")

    def strike_word(self, word):
        try:
            word_elements = self.driver.find_elements(by=By.XPATH, value=f'//a[text()="{word}"]')
            for element in word_elements:
                self.driver.execute_script("arguments[0].style.textDecoration = 'line-through';", element)
        except Exception as e:
            print(f"Error while striking through word {word}: {e}")

    def solve(self):
        start_time = time.time()

        
        n, m = self.grid_size

        for i in range(n):
            for j in range(m):
               
                if i < n and j < m and self.grid[i][j]:
                    for word in self.words:
                        if not word:  
                            continue
                        if word in self.found_words:
                            continue
                        if self.grid[i][j] == word[0]:  
                            self.bfs(i, j, word) 

        
        print(f"Found words: {self.found_words}")
        end_time = time.time()
        duration = end_time - start_time
        print(f"Time taken to solve the puzzle: {duration:.2f} seconds")



driver = webdriver.Chrome() 
driver.maximize_window()
driver.get('https://wordsearch.samsonn.com/') 

grid_size = (15, 15)

agent = WordSearchAgent(driver, grid_size)

while True:
    time.sleep(3)  
    agent.read_grid()
    agent.read_words()
    agent.solve()  
    time.sleep(2)  

    try:
        driver.switch_to.alert.accept()
    except:
        print("No alert found. Exiting.")
        break
