from game.models.Model import Model
from functions import roundPos


class Entity:
    def __init__(self, gl):
        self.shift = 0
        self.bInAir = None
        self.canShake = None
        self.hp = 20
        self.dy = 0
        print("doing some buggy things in the Entity class...")
        self.position = [0, 100, 0]
        self.rotation = [0, 0, 0]
        self.gravity = 5.8
        self.gl = gl
        self.tVel = 50
        self.lastPlayerPosOnGround = [0, 0, 0]
        self.playerFallY = 0
        self.kW, self.kS, self.kA, self.kD = 0, 0, 0, 0
        self.gl.allowEvents["collisions"] = True
        self.speed = 0.02
        self.model = Model(gl)

    def update(self):
        self.model.drawModel(self.position, self.rotation)
        self.update_pos()

    def update_pos(self):
        DX, DY, DZ = 0, 0, 0
        dt = self.speed
        self.position = [self.position[0] + DX, self.position[1] + DY, self.position[2] + DZ]
        if dt < 0.2:
            dt /= 10
            DX /= 10
            DY /= 10
            DZ /= 10
            for i in range(10):
                self.move(dt, DX, DY, DZ)

    def move(self, dt, dx, dy, dz):
        self.dy -= dt * self.gravity
        self.dy = max(self.dy, -self.tVel)
        dy += self.dy * dt

        if self.dy > 19.8:
            self.dy = 19.8

        x, y, z = self.position
        col = self.collide((x + dx, y + dy, z + dz))
        col2 = roundPos((col[0], col[1] - 2, col[2]))
        self.canShake = self.position[1] == col[1]
        if self.position[0] != col[0] or self.position[2] != col[2]:
            if col2 in self.gl.cubes.cubes and self.shift <= 0:
                self.gl.blockSound.playStepSound(self.gl.cubes.cubes[col2].name)
        if not self.bInAir:
            for i in range(1, 6):
                col21 = roundPos((col[0], col[1] - i, col[2]))
                if col21 not in self.gl.cubes.cubes:
                    self.bInAir = True
                    if self.playerFallY < col[1]:
                        self.playerFallY = round(col[1] - self.lastPlayerPosOnGround[1])
                else:
                    self.bInAir = False
                    break
        else:
            self.lastPlayerPosOnGround = col

        if self.bInAir and col2 in self.gl.cubes.cubes:
            hp = self.hp
        self.position = col

    def collide(self, pos):
        p = list(pos)
        np = roundPos(pos)
        for face in ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)):
            for i in (0, 1, 2):
                if not face[i]:
                    continue
                d = (p[i] - np[i]) * face[i]
                pad = 0.25
                if d < pad:
                    continue
                for dy in (0, 1):
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) in self.gl.cubes.collidable:
                        p[i] -= (d - pad) * face[i]
                        if face[1]:
                            self.dy = 0
                        break
        return tuple(p)
