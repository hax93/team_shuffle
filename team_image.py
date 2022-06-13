import os

from PIL import Image, ImageDraw, ImageFont


def add_players(name): 
    coordinates_x = {0: 70, 1: 350, 2: 450, 3: 600, 'set': 100}
    coordinates_y = {0: 90, 1: 240, 2: 450, 3: 620}
    if len(name) < 2:
        print("Nie możesz grać sam!")
    else:
        fonts_folder = r'C:\Windows\Fonts'
        img_football = Image.open(r'src\football_field.png')
        players_outfit = Image.open(r'src\outfit.png')
        outfit_width ,outfit_height = 220, 150
        field_width, field_height = img_football.size
        
        football_field = img_football.copy()
    
        fonts = ImageFont.truetype(os.path.join(fonts_folder, 'arialbd.ttf'), 32)

        x = coordinates_y.get(0)
        y = coordinates_y.get(0)
        standard = 100
        for i, players in enumerate(name):
            if len(name) > 10:
                standard =  0
            if (i+1) is (len(name) // 3 or len(name) // 3 + (1) or len(name) // 3 + (2)):
                x = coordinates_x.get(i - i) + standard
                y = coordinates_y.get(1)  
                          
            if i is (len(name) // 2 or len(name) // 2 + 1 or len(name) // 2 + 2):
                x = coordinates_x.get(i - i)
                y = coordinates_y.get(3)
                
            if i is (len(name) - 3 or len(name) - 2 or len(name) - 1):
                x = coordinates_x.get(i - i) + standard
                y = coordinates_y.get(2)     
                        
            try:
                outfit = players_outfit.copy()
                draw = ImageDraw.Draw(outfit)  

                draw.text((250,220), players.upper(), fill='black', font=fonts)
                outfit_final = outfit.resize((outfit_width, outfit_height))
                #draw.text((330,270), name[i].upper(), fill='black', font=fonts)
                football_field.paste(outfit_final, (x, y), outfit_final)
                x += 220
            except:
                continue      
                
        football_field.save(r'src\game_play.png')
