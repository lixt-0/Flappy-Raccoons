import pygame
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
screen_width = 768
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Raccoons")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Kuş ayarları (boyutları büyütüyoruz)
bird_width = 85  # Yeni genişlik
bird_height = 85  # Yeni yükseklik
bird_x = 100
bird_y = screen_height // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -12  # Zıplama gücünü de biraz artırdık

# Boru ayarları (boyutları büyütüyoruz)
pipe_width = 80  # Yeni boru genişliği
pipe_gap = 275  # Borular arasındaki boşluğu daha fazla arttırdık (300)
pipe_velocity = 4  # Boru hızını da orantılı şekilde artırıyoruz
pipes = []

# Skor
score = 0
font = pygame.font.SysFont('Arial', 30)

# Saat ayarı
clock = pygame.time.Clock()

# Kuş görselini yükleyin
bird_image = pygame.image.load('bird.png')
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))  # Görseli uygun boyutlara ölçeklendir

# Kuşı hareket ettiren fonksiyon
def draw_bird(y):
    screen.blit(bird_image, (bird_x, y))

# Boruları çizme fonksiyonu
def draw_pipes():
    global pipes
    for pipe in pipes:
        pygame.draw.rect(screen, BLACK, pipe['top_rect'])  # Boruları siyah renkte çiz
        pygame.draw.rect(screen, BLACK, pipe['bottom_rect'])  # Boruları siyah renkte çiz

# Yeni boru ekleme fonksiyonu
def add_pipe():
    pipe_height = random.randint(150, screen_height - pipe_gap - 150)  # Boru yüksekliğini de büyütüyoruz
    top_rect = pygame.Rect(screen_width, 0, pipe_width, pipe_height)
    bottom_rect = pygame.Rect(screen_width, pipe_height + pipe_gap, pipe_width, screen_height - pipe_height - pipe_gap)
    pipes.append({'top_rect': top_rect, 'bottom_rect': bottom_rect})

# Boruları hareket ettirme fonksiyonu
def move_pipes():
    global pipes, score
    for pipe in pipes:
        pipe['top_rect'].x -= pipe_velocity
        pipe['bottom_rect'].x -= pipe_velocity

    # Boruları kaldırma
    pipes = [pipe for pipe in pipes if pipe['top_rect'].x + pipe_width > 0]

    # Skoru arttırma
    for pipe in pipes:
        if pipe['top_rect'].x + pipe_width < bird_x and not pipe.get('scored', False):
            score += 1
            pipe['scored'] = True

    return pipes

# Oyun sona erme kontrolü
def check_collision():
    global bird_y, pipes
    # Kuşun ekran dışına çıkması
    if bird_y <= 0 or bird_y + bird_height >= screen_height:
        return True

    # Borularla çarpışma
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    for pipe in pipes:
        if bird_rect.colliderect(pipe['top_rect']) or bird_rect.colliderect(pipe['bottom_rect']):
            return True

    return False

# Buton sınıfı
class Button:
    def __init__(self, x, y, width, height, color, text, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont('Arial', 30)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2, 
                                  self.rect.y + (self.rect.height - text_surface.get_height()) // 2))
    
    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

# Yeniden başlatma fonksiyonu
def restart_game():
    global bird_y, bird_velocity, pipes, score
    bird_y = screen_height // 2
    bird_velocity = 0
    pipes = []
    score = 0
    add_pipe()

# Oyun bittiğinde çıkan mesaj ve buton
def game_over_message():
    screen.fill(BLACK)  # Ekran arka planını siyah yapıyoruz

    # Logo2 görselini yükleyin
    logo2_image = pygame.image.load('logo2.png')  # Logo2 dosyasının yolunu buraya yazın
    logo2_width, logo2_height = logo2_image.get_size()
    logo2_image = pygame.transform.scale(logo2_image, (int(logo2_width * 0.2), int(logo2_height * 0.2)))  # Boyutlandırma (isteğe bağlı)

    # Logo2'yi ekrana yerleştirin
    logo2_x = (screen_width - logo2_image.get_width()) // 2  # Yatayda ortalama
    logo2_y = (screen_height // 3) - logo2_image.get_height() - 10  # Game Over mesajından önceki pozisyon
    screen.blit(logo2_image, (logo2_x, logo2_y))  # Logo2'yi ekranda göster

    # Game Over mesajı
    game_over_font = pygame.font.SysFont('Arial', 50)
    message = game_over_font.render("Game Over!", True, RED)
    screen.blit(message, (screen_width // 3.2, screen_height // 3))

    # Yeni mesaj "Try your luck again to get WL"
    try_luck_font = pygame.font.SysFont('Arial', 30)
    try_luck_message = try_luck_font.render("Try your luck again to get WL", True, WHITE)  # Yazıyı beyaz yapıyoruz
    screen.blit(try_luck_message, (screen_width // 4, screen_height // 3 + 100))  # Game Over mesajının altına 100px boşluk bıraktık

    # Yeniden başlatma butonu
    restart_button = Button(screen_width // 2.5, screen_height // 2 + 40, 150, 50, RED, "Try Again", WHITE)  # Butonu kırmızı yapıyoruz
    restart_button.draw(screen)

    # 'Product by Lixt' mesajını ekleyin
    product_font = pygame.font.SysFont('Arial', 20)
    product_text = product_font.render("Product by lixt__", True, WHITE)
    product_width, product_height = product_text.get_size()
    product_x = (screen_width - product_width) // 2  # Yatayda ortalama
    product_y = screen_height - product_height - 25  # Ekranın en alt kısmına yerleştiriyoruz
    screen.blit(product_text, (product_x, product_y))

    pygame.display.update()

    return restart_button




# Başlangıç ekranı
def start_screen():
    start_button = Button(screen_width // 2.6, screen_height // 2, 150, 50, WHITE, "Start", BLACK)  # Siyah arka plan ve beyaz yazı

    # Logo görselini yükleyin
    logo_image = pygame.image.load('logo.png')  # Logo dosyanızın yolunu buraya yazın
    logo_width, logo_height = logo_image.get_size()
    logo_image = pygame.transform.scale(logo_image, (int(logo_width * 0.5), int(logo_height * 0.5)))  # Boyutlandırma (isteğe bağlı)

    # Başlık ve buton pozisyonlarını ortalamak için hesaplama
    while True:
        screen.fill(BLACK)

        # Logoyu ekrana yerleştirin
        logo_x = (screen_width - logo_image.get_width()) // 2  # Yatayda ortalama
        logo_y = (screen_height // 3) - logo_image.get_height() - 30  # Başlığın üstünde 10px boşluk bırakmak
        screen.blit(logo_image, (logo_x, logo_y))

        # Başlangıç ekranı mesajı
        start_font = pygame.font.SysFont('Arial', 50)
        title = start_font.render("Flappy Raccoons", True, WHITE)
        title_width, title_height = title.get_size()
        title_x = (screen_width - title_width) // 2  # Başlığın yatayda ortalanması
        title_y = (screen_height // 3 - title_height)  # Başlığın dikeyde konumlandırılması
        screen.blit(title, (title_x, title_y))

        # Yeni mesaj (SPACE tuşu ile oyun oynanır)
        instruction_font = pygame.font.SysFont('Arial', 30)
        instruction_text = instruction_font.render("The game is played with the SPACE key.", True, WHITE)
        instruction_width, instruction_height = instruction_text.get_size()
        instruction_x = (screen_width - instruction_width) // 2  # Mesajı yatayda ortalamak
        instruction_y = title_y + title_height + 50  # Başlığın altına 20px mesafe bırakmak
        screen.blit(instruction_text, (instruction_x, instruction_y))

        # 'Product by Lixt' mesajını ekleyin
        product_font = pygame.font.SysFont('Arial', 20)
        product_text = product_font.render("Product by lixt__", True, WHITE)
        product_width, product_height = product_text.get_size()
        product_x = (screen_width - product_width) // 2  # Yatayda ortalama
        product_y = screen_height - product_height - 25  # Ekranın en alt kısmına yerleştiriyoruz
        screen.blit(product_text, (product_x, product_y))

        start_button.draw(screen)

        pygame.display.update()


        # Butona tıklama kontrolü
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    return  # Start butonuna tıklanınca oyun başlasın


# Ana oyun fonksiyonu
def game_loop():
    global bird_y, bird_velocity, pipes, score

    running = True
    bird_y = screen_height // 2
    bird_velocity = 0
    pipes = []
    score = 0
    add_pipe()

    while running:
        screen.fill(WHITE)

        # Olayları kontrol et
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Boşluk tuşuna basıldığında kuş zıplar
                    bird_velocity = jump_strength

        # Kuşun hareketini hesapla
        bird_velocity += gravity
        bird_y += bird_velocity

        # Boruları ekle ve hareket ettir
        if len(pipes) == 0 or pipes[-1]['top_rect'].x < screen_width - 275:
            add_pipe()
        pipes = move_pipes()

        # Çarpışma kontrolü
        if check_collision():
            restart_button = game_over_message()

            # Yeniden başlama butonuna tıklama kontrolü
            restart = False
            while not restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        restart = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if restart_button.is_clicked(event.pos):
                            restart_game()
                            restart = True

        # Kuşu ve boruları çiz
        draw_bird(bird_y)
        draw_pipes()

        # Skoru ekrana yazdır
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (15, 15))

        pygame.display.update()
        clock.tick(60)  # FPS (Frames Per Second)

    pygame.quit()

# Oyun başlatma
start_screen()  # İlk önce başlangıç ekranı gösterilecek
game_loop()
