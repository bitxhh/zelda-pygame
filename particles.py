import pygame
from support import *
from random import choice


def reflect_images(frames):
    new_frames = []

    for image in frames:
        new_frames.append(pygame.transform.flip(image, True, False))

    return new_frames


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_sorted_folder('graphics/particles/flame/frames'),
            'aura': import_sorted_folder('graphics/particles/aura'),
            'heal': import_sorted_folder('graphics/particles/heal/frames'),

            # attacks
            'claw': import_sorted_folder('graphics/particles/claw'),
            'slash': import_sorted_folder('graphics/particles/slash'),
            'sparkle': import_sorted_folder('graphics/particles/sparkle'),
            'leaf_attack': import_sorted_folder('graphics/particles/leaf_attack'),
            'thunder': import_sorted_folder('graphics/particles/thunder'),

            # monster deaths
            'squid': (import_sorted_folder('graphics/particles/smoke_orange'),
                      import_sorted_folder('graphics/particles/smoke'),
                      import_sorted_folder('graphics/particles/smoke2')
                      ),
            'raccoon': import_sorted_folder('graphics/particles/raccoon'),
            'spirit': import_sorted_folder('graphics/particles/nova'),
            'bamboo': import_sorted_folder('graphics/particles/bamboo'),

            # leafs
            'leaf': (
                import_sorted_folder('graphics/particles/leaf1'),
                import_sorted_folder('graphics/particles/leaf2'),
                import_sorted_folder('graphics/particles/leaf3'),
                import_sorted_folder('graphics/particles/leaf4'),
                import_sorted_folder('graphics/particles/leaf5'),
                import_sorted_folder('graphics/particles/leaf6'),
                reflect_images(import_sorted_folder('graphics/particles/leaf1')),
                reflect_images(import_sorted_folder('graphics/particles/leaf2')),
                reflect_images(import_sorted_folder('graphics/particles/leaf3')),
                reflect_images(import_sorted_folder('graphics/particles/leaf4')),
                reflect_images(import_sorted_folder('graphics/particles/leaf5')),
                reflect_images(import_sorted_folder('graphics/particles/leaf6'))
            )
        }

    def create_grass_particles(self, pos, sprite_type, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups, sprite_type)

    def create_particles(self, animation_type, pos, sprite_type, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups, sprite_type)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups, sprite_type):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = choice(animation_frames) if sprite_type == 'squid' else animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index <= len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

    def update(self):
        self.animate()
