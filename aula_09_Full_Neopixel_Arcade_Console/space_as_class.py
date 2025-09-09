"""
    Space Invaders

    Developed for the "Recriating Arcade Classics with Circuitpython and Neopixels" 
    Workshop At SESC São Paulo (24 de Maio) - Between May 10 and July 4, 2024
    
    Depends:
    displayio, asyncio, simpleio, adafruit_imageload, adafruit_rtttl
    adafruit_ht16k33, adafruit_pixelbuf, neopixel and custom tilegrid and tilebuf
    (only if using 8x32 panels)
    
    Tested in Seeed Xiao RP2040
    
    Thanks to Ronaldo Gonçalves Alves for the pacience, support and ideas at workshop
"""

import random, time, gc


class Invader:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 2
        self.height = 2
        self.color = color
        
class PlayerShip:
    def __init__(self):
        self.x = 7
        self.y = 27
        self.lives = 3
        self.exploding = False
        self.explode_timer = 0

class Projectile:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class SpaceInvaders:
    def __init__(self, hardware):
        gc.collect()
        # Init Hardware
        self.hardware = hardware        
        self.hardware.screen.fill(0)
        #self.hardware.screen.rotation = 1
        self.hardware.screen.display()
        
        # por causa da rotação
        self.screen_width = self.hardware.screen.height
        self.screen_height = self.hardware.screen.width
        
        self.colors = [
            0x000000,  # Black
            0xFF0000,  # Red
            0xFF7F00,  # Orange
            0xFFFF00,  # Yellow
            0x00FF00,  # Green
            0x0000FF,  # Blue
            0x4B0082,  # Indigo
            0x8B00FF   # Violet
        ]
                
        #print ("Screen Dimensions w,h " , self.screen_width, self.screen_height)
        
        self.invaders = []
        self.player_ship = PlayerShip()
        self.projectiles = []
        self.enemy_projectiles = []
        self.score = 0
        
        self.hardware.display.print('{0:04}'.format(self.score))
        self.level = 1
        
        self.invader_move_direction = 1
        self.invader_speed = 0.1
        self.game_over = False
        self.reverse = False
        self.resetinvaders()
        self.gamedraw()
        self.galaga_sound()
    
    # Game Sounds
    def shoot_sound(self):
        self.hardware.play_rtttl("shoot:d=4,o=5,b=880:8c6")
        
    def xevious_sound(self):
        self.hardware.play_rtttl("Xevious:d=4,o=5,b=160:16c,16c6,16b,16c6,16e6,16c6,16b,16c6,16c,16c6,16a#,16c6,16e6,16c6,16a#,16c6,16c,16c6,16a,16c6,16e6,16c6,16a,16c6,16c,16c6,16g#,16c6,16e6,16c6,16g#,16c6")

    def galaga_sound(self):
        self.hardware.play_rtttl("Galaga:d=4,o=5,b=125:8g4,32c,32p,8d,32f,32p,8e,32c,32p,8d,32a,32p,8g,32c,32p,8d,32f,32p,8e,32c,32p,8g,32b,32p,8c6,32a#,32p,8g#,32g,32p,8f,32d#,32p,8d,32a#4,32p,8a#,32c6,32p,8a#,32g,32p,16a,16f,16d,16g,16e,16d")

    def resetinvaders(self):
        self.invaders = []
        for i in range(4):
            for j in range(4):
                self.invaders.append(Invader(i * 4, j * 4, random.choice(self.colors[1:])))

    def gamedraw(self):
        gc.collect()
        self.hardware.screen.fill(0)
        
        for invader in self.invaders:
            self.draw_invader(invader)
            
        self.draw_player_ship()
        self.draw_lives()
        
        for projectile in self.projectiles:
            self.draw_projectile(projectile)
            
        for projectile in self.enemy_projectiles:
            self.draw_projectile(projectile)
            
        if self.game_over:
            self.hardware.screen.fill(0)
            self.hardware.display.marquee('Game Over   ', loop=False)
            self.xevious_sound()
            
        self.hardware.screen.display()

    def draw_invader(self, invader):
        gc.collect()
        for i in range(invader.width):
            for j in range(invader.height):
                self.hardware.screen.pixel(invader.x + i, invader.y + j, invader.color)

    def move_invader(self, invader, dx, dy):
        invader.x += dx
        invader.y += dy
        if invader.x < 0 or invader.x >= self.screen_height - 1:
            invader.x = -1

    def shoot_invader(self, invader):
        return Projectile(invader.x + 1, invader.y + 2, self.colors[1])

    def draw_player_ship(self):
        gc.collect()
        ship = self.player_ship
        if ship.exploding:
            self.draw_explosion()
        else:
            self.hardware.screen.pixel(ship.x, ship.y, self.colors[5])
            self.hardware.screen.pixel(ship.x + 1, ship.y, self.colors[5])
            self.hardware.screen.pixel(ship.x + 1, ship.y - 1, self.colors[5])
            self.hardware.screen.pixel(ship.x + 2, ship.y, self.colors[5])

    def draw_explosion(self):
        ship = self.player_ship
        for i in range (3):
            self.hardware.screen.pixel(ship.x, ship.y, self.colors[1])
            self.hardware.screen.pixel(ship.x + 1, ship.y, self.colors[1])
            self.hardware.screen.pixel(ship.x + 1, ship.y - 1, self.colors[1])
            self.hardware.screen.pixel(ship.x + 2, ship.y, self.colors[1])
            self.hardware.screen.display()
            time.sleep(.02)
            self.hardware.screen.pixel(ship.x, ship.y, self.colors[5])
            self.hardware.screen.pixel(ship.x + 1, ship.y, self.colors[5])
            self.hardware.screen.pixel(ship.x + 1, ship.y - 1, self.colors[5])
            self.hardware.screen.pixel(ship.x + 2, ship.y, self.colors[5])
            self.hardware.screen.display()
            time.sleep(.02)
        self.player_ship.exploding = False

    def draw_lives(self):
        ship = self.player_ship
        total_width = ship.lives * 2 + (ship.lives - 1) * 1
        start_x = (self.screen_width - total_width) // 2
        for i in range(ship.lives):
            x_offset = start_x + i * 3
            for dx in range(2):
                for dy in range(2):
                    self.hardware.screen.pixel(x_offset + dx, 29 + dy, self.colors[5])

    def move_player_ship(self, dx):
        ship = self.player_ship
        ship.x += dx
        if ship.x < 0 or ship.x >= self.screen_width - 3:
            ship.x = max(0, min(self.screen_width - 3, ship.x))

    def explode_player_ship(self):
        ship = self.player_ship
        ship.exploding = True
        ship.explode_timer = time.monotonic()

    def draw_projectile(self, projectile):
        self.hardware.screen.pixel(projectile.x, projectile.y, projectile.color)

    def move_projectile(self, projectile, dy):
        projectile.y += dy
        if projectile.y < 0 or projectile.y >= self.screen_height:
            projectile.y = -1

    def update(self, dt):
        gc.collect()
        dx, dy = self.hardware.get_direction()
        self.move_player_ship(dy)
        
        if not self.hardware.trigger.value:
            print ("Shoot")
            self.projectiles.append(Projectile(self.player_ship.x + 1, self.player_ship.y - 1, self.colors[7]))
            time.sleep(0.2)

        # Move player projectiles
        for projectile in self.projectiles[:]:
            self.move_projectile(projectile, -1)
            if projectile.y == -1:
                self.projectiles.remove(projectile)

            # Check for collision from projectile with invaders
            for invader in self.invaders[:]:
                if invader.x <= projectile.x < invader.x + 2 and invader.y <= projectile.y < invader.y + 2:
                    self.invaders.remove(invader)
                    self.shoot_sound()
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    self.score += 10
                    self.hardware.display.print('{0:04}'.format(self.score))
                    if self.score % 1000 == 0:
                        self.player_ship.lives += 1
                    break

            # Check for collision with enemy projectiles
            for enemy_projectile in self.enemy_projectiles[:]:
                if projectile.x == enemy_projectile.x and projectile.y == enemy_projectile.y:
                    self.enemy_projectiles.remove(enemy_projectile)
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break

        # Move enemy projectiles
        for projectile in self.enemy_projectiles[:]:
            self.move_projectile(projectile, 1)
            if projectile.y == -1:
                self.enemy_projectiles.remove(projectile)

            # Check for collision with player ship
            ship = self.player_ship
            if ship.x <= projectile.x < ship.x + 3 and ship.y <= projectile.y < ship.y + 3:
                ship.lives -= 1
                self.explode_player_ship()
                self.enemy_projectiles.remove(projectile)
                if ship.lives <= 0:
                    self.game_over = True

        # Move invaders
        for invader in self.invaders[:]:
            self.move_invader(invader, self.invader_move_direction, 0)

            # Check collision between invaders and player ship
            ship = self.player_ship
            
            if invader.x <= ship.x - 2 < invader.x + invader.width and invader.y <= ship.y -2 < invader.y + invader.height:
                ship.lives -= 1
                self.invaders.remove(invader)
                self.explode_player_ship()
                
                if ship.lives <= 0:
                    self.game_over = True

        # Check for invader edge collision
        if any(invader.x >= (self.screen_width - 1 // 2) - 2 or invader.x <= 0 for invader in self.invaders):
            self.invader_move_direction *= -1
            for invader in self.invaders:
                if not self.reverse:
                    self.move_invader(invader, 0, 1)
                else:
                    self.move_invader(invader, 0, -1)

        # Check if invader is near player ship
        if any(invader.y >= self.player_ship.y - 1 for invader in self.invaders):
            self.reverse = True
        if any(invader.y <= 0 for invader in self.invaders):
            self.reverse = False

        # Enemy shooting
        if len(self.invaders) <= 3 and random.random() < 0.03:
            shooter = random.choice(self.invaders)
            self.enemy_projectiles.append(self.shoot_invader(shooter))

        if not self.invaders:
            self.hardware.screen.fill(0)
            self.hardware.screen.display()
            self.projectiles[:] = []
            self.enemy_projectiles[:] = []
            self.resetinvaders()
            self.xevious_sound()

    def play(self):
        gc.collect()
        self.last_update_time = time.monotonic()
        while not self.game_over:
            current_time = time.monotonic()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time
            self.update(dt)
            self.gamedraw()
            time.sleep(0.02)

