from pandac.PandaModules import *

class Room:
	def __init__(self):
                self.room = loader.loadModel("Models2/room.bam")
                self.room.reparentTo(render)
                self.room.setCollideMask(1)

                self.desk = loader.loadModel("Models/desk.bam")
                self.desk.reparentTo(render)
                self.desk.setCollideMask(1)

                self.screen_cd = loader.loadModel("Models/lcd_cd.bam")
                self.screen_cd.reparentTo(render)
                self.screen_cd.setCollideMask(1)

                self.screen_cu = loader.loadModel("Models/lcd_cu.bam")
                self.screen_cu.reparentTo(render)
                self.screen_cu.setCollideMask(1)

                self.screen_ld = loader.loadModel("Models/lcd_ld.bam")
                self.screen_ld.reparentTo(render)
                self.screen_ld.setCollideMask(1)

                self.screen_lu = loader.loadModel("Models/lcd_lu.bam")
                self.screen_lu.reparentTo(render)
                self.screen_lu.setCollideMask(1)

                self.screen_rd = loader.loadModel("Models/lcd_rd.bam")
                self.screen_rd.reparentTo(render)
                self.screen_rd.setCollideMask(1)

                self.screen_ru = loader.loadModel("Models/lcd_ru.bam")
                self.screen_ru.reparentTo(render)
                self.screen_ru.setCollideMask(1)

                self.setupCollisions()
                self.setupLights()


        def setupLights(self):
                ambient = AmbientLight('ambient')
                ambient.setColor(Vec4(0.300000011921,0.300000011921,0.176470592618,1.0))
                ambientNP = self.room.attachNewNode(ambient)
                #self.room.setLightOff()
                render.setLight(ambientNP)

                dlight1 = DirectionalLight('directional_2')
                dlight1.setColor(VBase4(1.0,1.0,1.0,1.0))
                dlight1.setSpecularColor(Vec4(1.0,1.0,1.0,1.0))
                self.directional_1= render.attachNewNode(dlight1)
                self.directional_1.setPos(Point3(51.0968856812,-69.1772079468,72.9400558472))
                self.directional_1.setHpr(Vec3(29.6146221161,-20.9541759491,-4.57117522501e-007))
                render.setLight(self.directional_1)

                dlight2 = DirectionalLight('directional_2')
                dlight2.setColor(VBase4(0.300000011921,0.300000011921,0.627451002598,1.0))
                dlight2.setSpecularColor(Vec4(1.0,1.0,1.0,1.0))
                self.directional_2= render.attachNewNode(dlight2)
                self.directional_2.setPos(Point3(-1.84763646126,-89.902671814,74.0891876221))
                self.directional_2.setHpr(Vec3(-10.8245697021,-15.4137153625,-3.1849167347))
                render.setLight(self.directional_2)        

        def setupCollisions(self):
                mask = BitMask32.bit(2)

                self.screen_luSphere = CollisionNode("screen_LUCSphere")
                self.screen_luSphere.addSolid( CollisionSphere(-26.445, 6, 68.046, 17) )
                self.screen_luNP = self.screen_cu.attachNewNode(self.screen_luSphere)
                self.screen_lu.setCollideMask(mask)

                self.screen_rdSphere = CollisionNode("screen_RDCSphere")
                self.screen_rdSphere.addSolid( CollisionSphere(25.58, 40.8, 48.06, 17) )
                self.screen_rdNP = self.screen_cu.attachNewNode(self.screen_rdSphere)
                self.screen_rd.setCollideMask(mask)

                self.screen_ruSphere = CollisionNode("screen_RUCSphere")
                self.screen_ruSphere.addSolid( CollisionSphere(24.837, 42, 68.021, 17) )
                self.screen_ruNP = self.screen_cu.attachNewNode(self.screen_ruSphere)
                self.screen_ru.setCollideMask(mask)

                self.screen_cdSphere = CollisionNode("screen_CDCSphere")
                self.screen_cdSphere.addSolid( CollisionSphere(-1.171, 24.532, 48.056, 17) )
                self.screen_cdNP = self.screen_cd.attachNewNode(self.screen_cdSphere)
                self.screen_cd.setCollideMask(mask)

                self.screen_cuSphere = CollisionNode("screen_CUCSphere")
                self.screen_cuSphere.addSolid( CollisionSphere(-2.11, 25.75, 68.02, 17) )
                self.screen_cuNP = self.screen_cu.attachNewNode(self.screen_cuSphere)
                self.screen_cu.setCollideMask(mask)

                self.screen_ldSphere = CollisionNode("screen_LDCSphere")
                self.screen_ldSphere.addSolid( CollisionSphere(-25.323, 4.88, 48.081, 17) )
                self.screen_ldNP = self.screen_ld.attachNewNode(self.screen_ldSphere)
                self.screen_ld.setCollideMask(mask)


               