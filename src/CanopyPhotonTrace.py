import ERRCODE
import common as comm
from math import *
from Planes import Planes
from TreeBoundary import TreeBoundary
from G_Function import G_Function
from MonteCarlo import MonteCarlo
from Position import Position
from iparam import Parameters

# ##################################################
# Simulator for forest light environment
# start MC simulation
#
# by H. Kobayashi
# modified 08/03/26
# ##################################################


class CanopyPhotonTrace:

    def __init__(self):
        self.sFlag = 1
        self.tau = 0.0
        self.weight = 0.0
        self.cNscat = 0
        self.cIchi = 0
        self.cIkd = 0

    def save(self, w, nscat):
        self.weight = w
        self.cNscat = nscat
        # self.cIchi = ichi
        # self.cIkd = ikd

        return ERRCODE.SUCCESS

    def trace(self, phoCoord, vectCoord, w, wq, nscat, ichi, ikd, truncRef, SO_R, lr, lt, ulr, ult):

        iVOX = 0
        distancePho = 0.0

        MIN_VALUE = 1.0e-8  # weight minimum limit
        distanceObj = 1.0e5    # initial distance from object
        intv = [50.0 / comm.RES] * 4
        tObj = [0.0] * 6
        face = 0

        # marginal value
        MGN = 1.0e-2

        phoCoord.z = comm.Z_MAX - MGN
        objCoord = Position()

        planes = Planes()
        treeBoundary = TreeBoundary()
        gFunction = G_Function()
        gFunction.igtbl()
        mcSimulation = MonteCarlo()

        # do wile photon exit from canopy space
        while (1):
            # determinatin of first input voxel
            phoCoord.x = min(phoCoord.x, comm.X_MAX)
            phoCoord.x = max(phoCoord.x, 0.0)
            phoCoord.y = min(phoCoord.y, comm.Y_MAX)
            phoCoord.y = max(phoCoord.y, 0.0)
            phoCoord.z = min(phoCoord.z, comm.Z_MAX)

            objCoord.setPosition(trunc(phoCoord.x / intv[1]),
                                 trunc(phoCoord.y / intv[2]),
                                 trunc(phoCoord.z / intv[3]))

            iVOX = comm.IX_MAX * comm.IY_MAX * int(objCoord.z)
            iVOX += int(objCoord.y) * comm.IY_MAX
            iVOX += int(objCoord.x) + 1

            objCoord.x *= intv[1]
            objCoord.y *= intv[2]
            objCoord.z *= intv[3]

            io = 1
            iNobj = -1
            index = -1
            distanceObj = 1.0e5
            
            # check the photon intersection with big-voxel walls
            errCode = planes.calPlanes(phoCoord, vectCoord, objCoord, intv)
            distancePho = planes.distance
            if (errCode == ERRCODE.CANNOT_FIND):
                # update the x, y, z
                phoCoord.x = planes.x
                phoCoord.y = planes.y
                phoCoord.z = planes.z

            # check the photon intersection with objects
            if (comm.N_DIVS[iVOX] != 0):

                distanceObj = 1.0e5
                for idiv in range(1, comm.N_DIVS[iVOX]):

                    index = comm.DIVS[iVOX][idiv]

                    tObj[1:6] = comm.OBJ[index][0:5]

                    treeBoundary.dealTreeType(comm.T_OBJ[index], phoCoord, vectCoord, tObj)

                    tempDistance = treeBoundary.distance
                    tempIO = treeBoundary.io
                    face = treeBoundary.face

                    if (tempDistance < distanceObj):
                        distanceObj = tempDistance
                        iNobj = index
                        io = tempIO

                    if (io == 0):
                        break

            # canopy interaction
            if ((distanceObj < distancePho) or (io == 0)):

                # stem interaction
                if (comm.T_OBJ[iNobj] == 4):
                    # if the photon is in the stem object by mistake, exit from stem
                    # in other case, photon go to the stem surface
                    phoCoord.x += vectCoord.x * distanceObj
                    phoCoord.y += vectCoord.y * distanceObj
                    phoCoord.z += vectCoord.z * distanceObj

                    tObj[1:6] = comm.OBJ[iNobj][0:5]

                    mcSimulation.stem(w, wq, phoCoord, vectCoord, nscat,
                                      tObj, face, truncRef, ichi, ikd)
                    # load changes
                    nscat = mcSimulation.cNscat
                    w = mcSimulation.weight

                    if (w < MIN_VALUE):
                        self.save(w, nscat)
                        return ERRCODE.LOW_WEIGHT

                    phoCoord.x += MGN * vectCoord.x
                    phoCoord.y += MGN * vectCoord.y
                    phoCoord.z += MGN * vectCoord.z
                # canopy interaction [Monte Carlo in canopy media]
                else:
                    phoCoord.x += ((distanceObj + MGN) * vectCoord.x) * float(io)
                    phoCoord.y += ((distanceObj + MGN) * vectCoord.y) * float(io)
                    phoCoord.z += ((distanceObj + MGN) * vectCoord.z) * float(io)

                    index = comm.I_OBJ[iNobj]
                    mcSimulation.canopy(w, wq, phoCoord, vectCoord, nscat, tObj, iNobj,
                                        truncRef, ichi, ikd, lr[index], lt[index])
                    # load changes
                    nscat = mcSimulation.cNscat
                    w = mcSimulation.weight
                    if (w < MIN_VALUE):
                        self.save(w, nscat)
                        return ERRCODE.LOW_WEIGHT

                    phoCoord.movePosition(distancePho, vectCoord, comm.X_MAX, comm.Y_MAX)

            # big-voxel wall interaction
            else:
                phoCoord.movePosition(distancePho, vectCoord, comm.X_MAX, comm.Y_MAX)

                # Monte Carlo in forest floor
                # forest floor downward flux
                if(phoCoord.z <= 0.0):
                    ix = int(phoCoord.x * comm.RES) + 1
                    iy = int(phoCoord.y * comm.RES) + 1
                    ix = min(ix, comm.SIZE)
                    iy = min(iy, comm.SIZE)

                    comm.FF_DIR[ix, iy] += w * wq * (1.0 - min(nscat, 1))
                    comm.FF_DIF[ix, iy] += w * wq * min(nscat, 1)

                    mcSimulation.floor(w, wq, phoCoord, vectCoord, nscat, ulr, ult, SO_R, ichi, ikd)

                    # load changes
                    nscat = mcSimulation.cNscat
                    w = mcSimulation.weight
                    if (w < MIN_VALUE):
                        self.save(w, nscat)
                        return ERRCODE.LOW_WEIGHT

                    phoCoord.x += MGN * vectCoord.x
                    phoCoord.y += MGN * vectCoord.y
                    phoCoord.z += MGN * vectCoord.z

                # sky (exit from canopy space)
                elif(phoCoord.z >= comm.Z_MAX):
                    self.save(w, nscat)
                    return ERRCODE.OUTSIDE

                # refresh the x, y position using the boundary condition
                else:
                    phoCoord.x -= (trunc(phoCoord.x / comm.X_MAX) - 0.5 + copysign(0.5, phoCoord.x)) * comm.X_MAX
                    phoCoord.y -= (trunc(phoCoord.y / comm.Y_MAX) - 0.5 + copysign(0.5, phoCoord.y)) * comm.Y_MAX

        self.save(w, nscat)

        return ERRCODE.SUCCESS
