# -*- coding: utf-8 -*-

import json
import codecs
import os
import cocos
import pyglet
import random

ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')

spritesheet = random.choice([
    u"Blood.json",
    u"Sparks1.json",
    u"Sparks2.json",
    u"SoldierRun.json",
    u"SoldierShoot.json",
    u"Explosion.json",
])

spritesheet = os.path.join(ASSET_DIR, spritesheet)
meta = None
frames = None
with codecs.open(spritesheet, 'r', 'utf16') as sf:
    data = json.load(sf)
    meta = data["meta"]
    frames = data["frames"]

image_file = os.path.join(os.path.dirname(spritesheet), meta["image"])

cocos.director.director.init()
layer = cocos.layer.Layer()
scene = cocos.scene.Scene(layer)

img = pyglet.image.load(image_file)
animation_frames = []
for name in sorted(frames.keys()):
    info = frames[name]
    frame_src = img.get_region(
        info["frame"]["x"],
        img.height - info["frame"]["y"] - info["frame"]["h"],
        info["frame"]["w"],
        info["frame"]["h"]
    )

    frame = pyglet.image.create(
        info["spriteSourceSize"]["w"],
        info["spriteSourceSize"]["h"]
    )
    frame = frame.get_texture()
    frame.blit_into(frame_src,
        info["spriteSourceSize"]["x"],
        frame.height - info["spriteSourceSize"]["y"] - info["frame"]["h"],
        0
    )
    animation_frames.append(pyglet.image.AnimationFrame(frame, 1.0/24.0))
#animation_frames[-1].duration = None
animation = pyglet.image.Animation(animation_frames)
sprite = cocos.sprite.Sprite(animation)
layer.add(sprite)
c = (255,255,255,128)
sprite.x = frame.width / 2
sprite.y = frame.height / 2




cocos.director.director.run(scene)
