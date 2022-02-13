import os
folder="Spiderman"

images=os.listdir(folder)

with open(folder + '/Authors.txt','w') as f:
    for image in images:
        f.write(image + ' : Manvith : SpriteSpawnGaming\n')
