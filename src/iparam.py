# Parameters Initialization

import common as comm
import math
import numpy as np
import ERRCODE

class Parameters:
    ix = [0] * 1025
    wl0 = 0.0  # Default target wavelength(micron)
    wls = 0.0  # Default start point of wavelength integration
    nwl = 0  # Default sampling number of the wavelength
    taur = 0.0  # default AOT(tau at 550 nm)
    ctaur = 0.0  # default COT(tau at 550 nm)
    d = 0.0  # default scale height(m)
    atmType = 0  # default atmospheric type
    aerosolType = 0  # default aerosol type
    cloudType = 0
    nkd = 0  # of subbands for the k-distribution
    th0 = 0.0  # solar zenith angle in degree
    ph0 = 0.0  # solar azimuth angle in degree
    tm = 0.0  # atmopsheric transmittance
    hfov = 0.0  # detector half widt of the field of view
    cflg = 0  # cflg = 0 -> cloud - free, cflg = 1 -> cloud
    tflx = 0.0  # Total downward flux at top of canopy
    bflx = 0.0  # Beam downward flux at TOC
    dflx = 0.0  # Diffuse downward flux at TOC
    obflx = 0.0  # Beam downawr flux at TOC(observed)
    odflx = 0.0  # Diffuse downward flux at TOC(observed)
    rflx = 0.0  # total reflcted irradiaice
    rbflx = 0.0  # beam reflected irradiance
    rdflx = 0.0  # diffuse reflected irradiance
    tpfd = 0.0  # Total downward PFD at top of canopy
    bpfd = 0.0  # Beam downward PFD at top of canopy
    dpfd = 0.0  # Diffuse downward PDF at top of canopy
    obpfd = 0.0  # Beam downawr PFD at TOC(observed)
    odpfd = 0.0  # Diffuse downward PFD at TOC(observed)
    cbnz = 0  # Number of cloud bottom layer
    ctnz = 0  # Number of cloud top layer
    RF = 0.0  # incident irradiance and photon flux density at TOA
    RQ = 0.0  # incident irradiance and photon flux density at TOC
    fpc = 0.0  # fpar for canopy floor
    fpf = 0.0  # fpar for forest floor
    span = [0] * 101  # Wavelength span
    Nprocess = 1  # number of processor
    nPhotonProcess = 1

    # read parameters
    nPhoton = nmix = AtmMode = imode = cmode = surfaceType = 0
    diffuse = phi = th = ph = tgx = tgy = 0.0
    wq = sinf0 = cosf0 = cosq0 = sinq0 = 0

    npl = [0] * 200
    alb = [0.0] * 100
    spcf = [0.0] * 400
    spcq = [0.0] * 400
    ulr = [0.0] * 100
    ult = [0.0] * 100
    sor = [0.0] * 100
    tlr = [0.0] * 5
    tlt = [0.0] * 5
    tstr = [0.0] * 5

    lr = np.zeros(5 * 100, dtype=float).reshape(5, 100)
    lt = np.zeros(5 * 100, dtype=float).reshape(5, 100)
    str = np.zeros(5 * 100, dtype=float).reshape(5, 100)

    fname = []
    rfname = ""

    nts = 0  # group of tree species
    bound = 1

    # for math
    T_SIN = [0.0] * comm.ANGLE_SHIFT * 2
    T_COS = [1.0] * comm.ANGLE_SHIFT * 2
    T_ACOS = [0.0] * comm.ACOOS_SHIFT * 2
    T_EXP = [0.0] * comm.ACOOS_SHIFT
    DLT = np.zeros((6 + 1) * (6 + 1), dtype=float).reshape((6 + 1), (6 + 1))

    def __init__(self):
        self.initParameters()

    def initParameters(self):
        comm.N_Z = 12  # of layers
        comm.X_MAX = comm.Y_MAX = 30.0  # X domain size (m), Y domain size (m)
        comm.RES = comm.SIZE / comm.X_MAX  # inverse of the spatial resolution
        comm.WRR = 0.1  # ideal weight (used for Russian roulette in atm.

        # branch portion in region 1(outer canopy) and 2(internal canopy)
        # 1.0 = 100 % branch, 0.0: 100 % leaf
        comm.bp1 = 0.0
        comm.bp2 = 1.0

        # leaf angle distribution of canopy, branches, and floor
        comm.M_C = comm.M_B = comm.M_F = 1

        # #   ---  local parameters ---
        self.wl0 = 0.55  # Default target wavelength(micron)
        self.wls = 0.3  # Default start point of wavelength integration
        self.nwl = 75  # Default sampling number of the wavelength
        self.taur = 0.3  # default AOT(tau at 550 nm)
        self.ctaur = 0.00  # default COT(tau at 550 nm)
        self.d = 8000.0  # default scale height(m)
        self.atmType = 1  # default atmospheric and aerosol type
        self.aerosolType = 2
        self.nkd = 3  # of subbands for the k-distribution
        self.th0 = 10.0  # solar zenith angle in degree
        self.ph0 = 0.0  # solar azimuth angle in degree
        self.tm = 1.0  # atmopsheric transmittance
        self.hfov = 1.0  # detector half widt of the field of view
        self.hfov = math.radians(self.hfov)
        self.hfov = math.cos(self.hfov)
        self.cflg = 0  # cflg = 0 -> cloud - free, cflg = 1 -> cloud

        self.span[1: 20] = [0.02] * 20  # Wavelength span (0.3-0.7 micron)
        self.span[21: 100] = [0.1] * 80  # Wavelength span (0.7- micron)

        #     Irradiance
        self.tflx = 0.0  # Total downward flux at top of canopy
        self.bflx = 0.0  # Beam downward flux at TOC
        self.dflx = 0.0  # Diffuse downward flux at TOC
        self.obflx = 0.0  # Beam downawr flux at TOC(observed)
        self.odflx = 0.0  # Diffuse downward flux at TOC(observed)

        #     reflected radiance from canopy
        self.rflx = 0.0  # total reflcted irradiaice
        self.rbflx = 0.0  # beam reflected irradiance
        self.rdflx = 0.0  # diffuse reflected irradiance

        #     Photon flux density
        self.tpfd = 0.0  # Total downward PFD at top of canopy
        self.bpfd = 0.0  # Beam downward PFD at top of canopy
        self.dpfd = 0.0  # Diffuse downward PDF at top of canopy
        self.obpfd = 0.0  # Beam downawr PFD at TOC(observed)
        self.odpfd = 0.0  # Diffuse downward PFD at TOC(observed)

        #     Number of cloud bottom and top layer
        self.cbnz = 0
        self.ctnz = 1

        #     incident irradiance and photon flux density at TOA or TOC
        self.RF = 0.0
        self.RQ = 0.0

        self.ix = [0, 715327539,474399417,182768403,
       780769431,576730197,937392842,445151859,688527083,160158012,
       750394380,704034435,445074075,668471240,896236437,567474752,
       686366724,313996988,336207690,785978227,778020274,918287307,
       165417294,345438969,907890635,347416159,564662778,423338472,
       322334997,537865632,861550217,847868806,131114898,991933631,
       711366790,789845275,154507895,445727944,529958587,952987849,
       941223627,914187765,387129643,731071531,106928367,428804814,
       339530062,987977910,349373608,666589081,249856479,762473708,
       492770269,984295237,762602078,309875385,181659605,554070627,
       544579014,145075585,518001246,574235904,470872688,375689646,
       919288736,793184089,576772630,583573585,630078959,718095433,
       922435718,260494938,899714994,845035588,550636380,614489316,
       129748380,342385542,752870810,561946344,901663726,773463362,
       291476356,142718061,857835626,599125462,822165143,148115470,
       102699640,719609755,114280930,315919730,632002210,662364387,
       475737383,521125644,473855143,713211613,581004834,124188662,
       385785588,212828838,395410802,861018067,166374165,861383384,
       600531530,232779699,631097769,686852794,999512106,415913715,
       881422436,984974586,539663088,857359588,472863933,448952791,
       946881961,785362821,238347978,227637797,822765690,738837653,
       262806318,959824693,686128383,326913756,243790771,282925300,
       347129324,483847659,666342264,911506146,217384530,323057584,
       898291599,182956265,233336405,245978702,227818927,221598428,
       509776547,447233226,214040942,414571726,517627480,507070145,
       293723551,952738082,125537664,628467971,608408802,524136102,
       279781483,918029707,548632100,640354341,235301552,938506978,
       780259168,659470605,956230694,325113028,469281736,218069674,
       669464838,897083532,428805136,686481469,360384586,358491134,
       472625645,958973413,731986004,450382757,828050124,528788635,
       516020488,711633133,549766916,820648300,744078099,756772887,
       181891301,327751624,988430935,213427722,866142696,964985638,
       496034786,735881912,572488659,743238997,879294425,713844186,
       767544317,516990455,924970513,495397278,293978777,835805356,
       387324693,959867930,279599267,563193517,901016831,583683180,
       467890018,888909125,290367062,825984930,897427982,667439448,
       193090536,669374716,796016824,842227637,893353706,100791099,
       874773830,225275495,700911164,505312681,384159177,495752993,
       185093925,754601478,990426230,540048843,117183163,284735697,
       654715317,720082843,589553463,999204993,292192117,956943678,
       520778593,787604343,475951343,238244029,738028538,450868237,
       882337337,852777892,714244800,845837140,319648818,163957206,
       158674488,640909075,952790546,799179255,480213829,353940284,
       619044995,555360287,428642246,562991225,297469578,458329311,
       272641456,355631524,310239267,815292841,100535538,449940916,
       726618528,110184604,638394987,845519244,222809445,274570728,
       777646374,989143276,722952055,386900100,173563846,259192337,
       804837858,150796596,944107592,241958057,536792668,172954717,
       245518931,765096962,292466963,598520195,342293274,742080068,
       732690459,332958489,487763014,331451785,453715831,304306945,
       670086896,387259837,228740735,573510956,726406580,433203637,
       671245718,170436887,221798990,328530055,528306588,384406611,
       432767805,562542760,704605746,837753498,786313664,629190021,
       191473640,666614669,755747532,379664975,702568554,695219945,
       570526945,565430802,113455511,729851019,708613234,846314841,
       461649617,449048089,973078024,396699738,389404076,724621301,
       591522955,566275215,346788763,514627617,805478692,874203109,
       984912198,859577828,624179011,987852382,776539105,645075726,
       205693244,235354499,950277531,601152193,119875329,678681015,
       703088581,926062923,501421090,737043684,835391223,339952000,
       736254954,626308470,726111215,589620465,246772944,575693416,
       244674022,664175254,804692804,492974600,502179351,105707521,
       912971061,712505763,772011214,409435805,514390751,434718710,
       568864083,693147993,108412769,717491453,163571384,748691016,
       193417558,103828531,244246532,738387846,294243296,629307234,
       450758266,322059829,351363754,160164791,367319893,587539178,
       447192484,850313907,566630554,149750910,831939166,588153833,
       151727745,870573383,992379736,351560574,619998413,357348138,
       398057472,510176438,798292303,778476464,269448219,235280376,
       546121954,946146821,171925198,713047999,751387333,145542333,
       540686538,213339531,646850329,254061029,567989629,101491674,
       511445713,976020085,765062844,854291462,126419931,320127592,
       726073664,501840615,784555584,416186872,298616638,204913941,
       530023872,333112770,711398977,421232482,105471433,698953098,
       718673020,211273633,639423400,481902280,834338939,337258231,
       174255883,958625638,597575950,439795354,988194686,725370764,
       288606071,652712941,172317773,325139743,940627425,492783117,
       544820171,488717451,606341838,582640069,792202669,592277354,
       302321077,258376838,831743204,792493635,310322348,249334776,
       769693785,506666097,202308101,126671762,852585899,243781933,
       212450419,658941084,781093174,142874742,976827108,774326443,
       954241406,423692041,437779057,549959793,687359732,584795171,
       687710458,396150502,210256204,749684453,794749748,148324950,
       497469338,535762405,520967233,329461720,307514692,695794153,
       976011556,567257386,908122807,379152056,132028931,968366134,
       158820642,132730855,394504806,284807178,713499200,565936505,
       857418435,116150068,922622507,299500587,244074843,634191107,
       434319168,498511296,211463896,254241408,509565162,174777144,
       619098263,461522963,979462164,194666354,479420781,654949367,
       546923801,163301688,194472229,701938289,729811966,704713141,
       172904969,337296640,573704075,450154206,821816778,352260041,
       542208772,740407979,513786503,360789814,481501424,877278476,
       618555653,294747538,852938073,941717422,425875252,316396425,
       585554182,501336869,220635233,326374846,482671993,951440107,
       742191863,967128026,140806645,884695804,254039706,525141957,
       268142265,567372882,102905902,645042306,319375286,843252885,
       412742513,558692395,284106625,157423258,815817373,698219943,
       309580288,735815125,137278393,790358489,945752859,237983600,
       396490848,782421189,500067272,753798800,435267785,335600680,
       821875894,309346842,522548636,936234825,363221210,816270077,
       582875460,850904583,545167812,463222974,339507237,308870281,
       487556564,668586951,768946576,840601950,380444666,970218682,
       130818789,979514467,574695205,740414148,875068712,155558241,
       950725245,243294508,298463980,521267265,632429379,645401185,
       729721897,136967290,199017487,444539350,997838729,839200335,
       587381196,880762827,409252047,128474914,763457381,833866065,
       703891903,492486625,938723272,988592243,272785383,440529581,
       120519592,180093396,280580070,786109495,777856391,936727976,
       123705718,169591884,630828422,871188521,159661253,927312511,
       555372625,239872492,571394586,245277479,566895931,616924226,
       641473895,565217298,578284591,411284571,396620988,226639439,
       978504025,722013819,707072252,627414184,728702336,629999244,
       236095204,545612818,233551371,128490893,929005736,541735309,
       146455038,388578063,701168870,497181886,605335366,593862646,
       649999511,700344359,596646457,941726326,131553557,196462468,
       728614306,552047276,187689284,466783955,250581520,345926004,
       675570994,721695333,538164564,320628093,120164535,848130375,
       442103126,742325812,733032494,804702085,865477508,751452833,
       299490810,944428598,186884447,739405047,928227144,685114991,
       352093368,644984370,794827264,487401399,580778777,538013046,
       577440607,531804564,556137967,210654774,909569001,431705918,
       649663913,347817739,942342323,686363077,104334047,311862446,
       307242770,404658630,444671663,637728619,189879047,492842099,
       351035720,497138702,637451654,536757424,474827873,203027128,
       282233773,932952767,410118830,789557313,872889310,839059573,
       472144806,824421149,713342022,561833637,732224237,326279896,
       976913100,614424353,758227449,574671709,377494746,615525883,
       927542752,151950633,727296161,154128218,822941052,471023160,
       481720185,882544672,442547461,615864646,615197741,573103207,
       793041825,521291270,878148531,450254708,830705833,349478349,
       832974821,895334196,196964927,245983436,348982274,768813431,
       911096143,891245651,180867790,567402976,478034266,628175771,
       945884341,229315733,569857144,186785695,165582142,475116720,
       707223582,686165130,367357766,253716620,739102226,569993185,
       792424112,621876281,606350421,228971847,890372592,244926230,
       444357630,404276227,150045567,875459617,892705684,314217399,
       397682526,665889990,201763533,671684849,485985970,890571665,
       426160129,234326247,737729150,718820112,939559102,128263398,
       713078951,537823629,430655351,549691599,975228619,907891225,
       505661314,774230527,423441469,467359691,535485547,314569331,
       873291748,917821514,231576071,766682898,216533385,431382417,
       276676692,243621818,451869961,978292721,966844195,831742131,
       747027510,444085198,995860546,728259825,370109578,439736077,
       814043951,270593723,233908681,640119379,542656674,618111264,
       529876700,421904590,486525496,405207249,814850115,681845700,
       548767498,400876072,362372827,531800755,383228987,229728204,
       819131296,700170713,172289831,906871557,850126636,864350444,
       627107125,450550422,675152140,868928599,211951635,166159857,
       337720108,891153866,361899819,642024445,439627662,143827704,
       199016615,240285606,443759444,359789028,815392673,564878320,
       209565602,388550195,928746581,489589545,230407714,563131290,
       518506333,278271935,680408090,512241283,480297219,282204416,
       855593729,850283330,630477321,671157473,363739091,857839488,
       432136413,724229806,108647099,781859052,169139583,780270111,
       773479938,837574487,465207675,747239726,194121423,436023390,
       145433472,474004194,421773108,983829176,436824458,275210985,
       940699148,166465293,877754408,439134913,850040054,698777306,
       410009986,570765233,848371505,693898797,757403367,623156607,
       516752839,263076202,703176987,697732532,349000808,699375867,
       956577932,462465894,851222318,581388550,957187867,852737927,
       399635469,145038761,117024413,636334460,604822957,573563528,
       414576151,678724038,665047293,898052990,110377544,318905645,
       496241262,498133292,660918354,947286063,582360690,637050825,
       704483383,474406659,929325616,747815275,391085982,936901086,
       708458739,204045931,692734181,129042436,696603751,869574207,
       853373664,836296576,153963825,433753517,322276310,642164617,
       700613063,695282870,907520276,246662250,926170587,616911351,
       882269155,618787074,538490641,105029377,852397340,770021498,
       665877866,276560163,350916147,205514039,416253310,498361334,
       854810738,282842473,952407902,452399832,966281896,295668850,
       871440219,612405884,906151652,634743267,182620781,631412714,
       345198562]

        # initialization of random number generator
        # self.flg = frndi(ix(Nid + 1)) move to the Random.py _init_()
        self.flg = 0

        self.initMathparameters()

        return ERRCODE.SUCCESS

    def initMathparameters(self):
        for i in range(0, 62832 * 2):
            self.T_SIN[i] = math.sin(float(i - 62832) * 0.0001)
            self.T_COS[i] = math.cos(float(i - 62832) * 0.0001)

        for i in range(0, comm.ACOOS_SHIFT * 2):
            self.T_ACOS[i] = math.acos(float(i - comm.ACOOS_SHIFT) * 0.0001)

        for i in range(1, 6):
            comm.DLT[i, i] = 1.0

        return ERRCODE.SUCCESS

    def getInputLR_LT_ULR_ULT(self, i):
        for j in range(self.nts):
            self.lr[j, i] = float(input())
        for j in range(self.nts):
            self.lt[j, i] = float(input())
        self.ulr[i] = float(input())
        self.ult[i] = float(input())
        for j in range(self.nts):
            self.str[j] = float(input())
        self.sor[i] = float(input())
        return ERRCODE.SUCCESS

    def process100(self):

        if (self.cloudType >= 2):
            comm.N_ANG_C = 1
            comm.UX_RC[0] = 0.0
            comm.UY_RC[0] = 0.0
            comm.UZ_RC[0] = 1.0

        self.process201()

        return ERRCODE.SUCCESS

    def process202(self):
        umax = 0.0

        print("u: leaf area density 1,2,3...# tree species")
        # for i in range(self.nts):
        #     comm.U[i] = float(input())
        # debug
        comm.U[1] = 1

        if (not((self.nPhoton == -4) or (self.nPhoton == -5))):
            comm.G_LAI = float(input("gLAI: forest floor LAI\n"))

        print("BAD: branch area density 1,2,3... # of tree species")
        # for i in range(self.nts):
        #     comm.BAD[i] = float(input())
        # debug
        comm.BAD[1] = 1

        for i in range(self.nts):
            if ((comm.U[i] < 0.0) or (comm.U[i] > 8.0)):
                print(str(i) + "th leaf area density " + str(comm.U[i]) + " should be set in the range (0.0-8.0)")
                print("EXIT")
                return ERRCODE.INPUT_ERROR

        if ((comm.G_LAI < 0.0) or (comm.G_LAI > 8.0)):
            print(str(comm.G_LAI) + " should be set in the range (0.0-8.0)")
            print("EXIT")
            return ERRCODE.INPUT_ERROR

        if (self.nPhoton == -5):
            print("sbar: Spherical ave. shoot silhouette to total needle area ratio")
            print("1,2,3... # of tree species (0.0-0.25)")
            print("For broadleaves, please input 0.25")
            # for i in range(self.nts):
            #     comm.S_BAR[i] = float(input())
            # debug
            comm.S_BAR[1] = 0.25

        umax = comm.U[0]
        for i in range(1, self.nts):
            if (umax < comm.U[i]):
                umax = comm.U[i]

        if (umax > 1.0):
            comm.FE = 1.0
        elif (umax <= 0.01):
            comm.FE = 0.01
        else:
            comm.FE = umax

        # canopy object parameters
        # object id initialization
        comm.I_OBJ = [1] * 6000

        # input obj_nt
        result = ''
        with open("../data/crowndata.txt", "r") as file:
            comm.N_OBJ = int(file.readline())

            if (comm.N_OBJ == 0):
                comm.N_OBJ = comm.T_OBJ = 1
                comm.OBJ[0, 0] = 0.01
                comm.OBJ[0, 1] = 0.01
                comm.OBJ[0, 2] = 0.01
                comm.OBJ[0, 3] = 1E-5
                comm.OBJ[0, 4] = 1E-5
            else:
                result = file.readlines()
                result = np.loadtxt(result)
        file.close()

        obj_nt = comm.N_OBJ
        for i in range(len(result)):
            comm.T_OBJ[i] = int(result[i][0])
            comm.OBJ[i][0:5] = result[i][1: 6]
            comm.I_OBJ[i] = int(result[i][6])
            if (result[i][0] != 4):
                if ((result[i][4] < 0.01) or (result[i][5] < 0.01)):
                    print(str(i + 1) + "th canopy neglected!")
                    obj_nt -= 1

        comm.N_OBJ = obj_nt

        # check the obj id range
        for i in range(obj_nt):
            if ((comm.I_OBJ[i] <= 0) or (comm.I_OBJ[i] > self.nts)):
                print("species id should be the range betweem 0-" + str(self.nts))
                return ERRCODE.OUT_OF_RANGE

        print("Total Object is " + str(obj_nt))

        # change from height to radius
        for i in range(obj_nt):
            if (comm.T_OBJ[i] == 3):
                comm.OBJ[i, 3] /= 2

        # in case periodic boundary
        # add objects that are partially in the outside from the simulation scene
        a = [1.0, 1.0, 0.0, 0.0]
        b = [0.0, 0.0, 1.0, 1.0]
        # preparation of the i-th grid for space divided method
        c = [0.0, comm.X_MAX, 0.0, comm.Y_MAX]
        cc = [0.0, 1.0, 0.0, 1.0]
        iMin = 0.0
        iMax = comm.X_MAX

        if (self.bound == 1):
            # set distance calculation parameters
            kobj = comm.N_OBJ

            # definition of rectangular of the i-th object
            for j in range(kobj):
                xr = comm.OBJ[j, 0]
                yr = comm.OBJ[j, 1]

                # check the intersection on the x - y plane
                for k in range(4):
                    d = abs(xr * a[k] + yr * b[k] - c[k])

                    if (d <= comm.OBJ[j, 4]):   # partially in the out of range
                        dd = math.sqrt(comm.OBJ[j, 4] * comm.OBJ[j, 4] - d * d)
                        p1 = b[k] * xr + a[k] * yr - dd
                        p2 = b[k] * xr + a[k] * yr + dd

                        if (((iMin < p1) and (iMax > p1)) or
                                ((iMin < p2) and (iMax > p2))):

                            comm.N_OBJ += 1

                            n = comm.N_OBJ
                            comm.OBJ[n, 0] = comm.OBJ[j, 0] + a[k] * comm.X_MAX * (1.0 - 2.0 * cc[k])
                            comm.OBJ[n, 1] = comm.OBJ[j, 1] + a[k] * comm.Y_MAX * (1.0 - 2.0 * cc[k])
                            comm.OBJ[n, 2] = comm.OBJ[j, 2]
                            comm.OBJ[n, 3] = comm.OBJ[j, 3]
                            comm.OBJ[n, 4] = comm.OBJ[j, 4]

                            comm.T_OBJ[n] = comm.T_OBJ[j]
                            comm.I_OBJ[n] = comm.I_OBJ[j]

                for k in range(2):
                    for l in range(2):
                        rx = xr - c[k]
                        ry = yr - c[l + 2]
                        rr = math.sqrt(rx * rx + ry * ry)

                        if (rr <= comm.OBJ[j, 4]):

                            comm.N_OBJ += 1

                            n = comm.N_OBJ
                            comm.OBJ[n, 0] = comm.OBJ[j, 0] + comm.X_MAX - 2.0 * cc[k]
                            comm.OBJ[n, 1] = comm.OBJ[j, 1] + comm.Y_MAX - 2.0 * cc[l + 2]
                            comm.OBJ[n, 2] = comm.OBJ[j, 2]
                            comm.OBJ[n, 3] = comm.OBJ[j, 3]
                            comm.OBJ[n, 4] = comm.OBJ[j, 4]

                            comm.T_OBJ[n] = comm.T_OBJ[j]
                            comm.I_OBJ[n] = comm.I_OBJ[j]

            # determination of the epsi(epsiron) that is used to perform the
            # Russian Roulette
            # epsi is setted to be c * (leaf_r + leaf_t)
            if (self.nPhoton == -4):
                avelr = 0.0
                avelt = 0.0

                for i in range(self.nwl):
                    for j in range(self.nts):
                        avelr += self.lr[j, i]
                        avelt += self.lt[j, i]

                avelr /= float(self.nwl * self.nts)
                avelt /= float(self.nwl * self.nts)

        return ERRCODE.SUCCESS

    def process201(self):
        ispc = 0
        # get the number of forest species
        #self.nts = int(input("nts: # of group of tree species\n"))
        # debug
        self.nts = 1
        if ((self.nPhoton == -4) or (self.nPhoton == -5)):
            return self.process202()

        comm.U[5] = float(self.nts)

        # currently max nts should be less than 5
        if ((self.nts <= 0) or (self.nts >= 5)):
            print("Error # of tree species")
            print("tree species should be 1-5")
            return ERRCODE.INPUT_ERROR

        # read leaf reflectance/transmittance
        ramda = self.wls
        if(self.nPhoton == -4):
            self.nwl = 1

        for i in range(self.nwl + 1):
            if (self.nwl == 1):
                print("Input surface optical properties")
            else:
                print("Input surface optical properties in")
                if (i <= 20):
                    print(str(ramda) + " and " + str(ramda + self.span[1]))
                else:
                    print(str(ramda) + " and " + str(ramda + 5 * self.span[1]))

            print("lr1 lr2.. lt1 lt2.. ulr ult str1 str2.. sor")
            print("(lr, lt:leaf refl. & leaf transm.")
            print("ulr,ult:understory leaf refl. & transm.")
            print("stmr: stem refl., soilr: soil refl.)")

            if (self.nwl == 1):
                self.getInputLR_LT_ULR_ULT(i)

            else:
                if (i == 1):
                    print("Input PAR average values:")
                    self.getInputLR_LT_ULR_ULT(i)
                    ispc = i

                elif (i == 21):
                    print("Input NIR average values")
                    self.getInputLR_LT_ULR_ULT(i)
                    ispc = i

                else:
                    for j in range(self.nts):
                        self.lr[j, i] = self.lr[j, ispc]
                        self.lt[j, i] = self.lt[j, ispc]
                        self.str[j, i] = self.str[j, ispc]

                    self.ulr[i] = self.ult[ispc]
                    self.ult[i] = self.ult[ispc]
                    self.sor[i] = self.sor[ispc]

            # check the parameter range
            for j in range(self.nts):
                if (self.lr[j,i] + self.lt[j,i] > 0.99):
                    print("canopy leaf reflectance+transmittance is too large, exit!")
                    return ERRCODE.OUT_OF_RANGE

                if (self.lr[j, i] + self.lt[j, i] < 0.0001):
                    self.lr[j,i] = 0.0001
                    self.lt[j,i] = 0.0001

            if (self.ulr[i] + self.ult[i] > 0.99):
                print("floor leaf reflectance+transmittance is too large, exit!")
                return ERRCODE.OUT_OF_RANGE

            if (self.ulr[i] + self.ult[i] < 0.0001):
                self.ulr[i] = 0.0001
                self.ult[i] = 0.0001

            for j in range(self.nts):
                if (self.str[j, i] > 1.00):
                    print("stem reflectance is too large, exit!")
                    return ERRCODE.OUT_OF_RANGE

                if (self.str[j, i] < 0.0001):
                    self.str[j, i] = 0.0001

            if (self.sor[i] > 1.0):
                print("soil reflectance is too large, exit!")
                return ERRCODE.OUT_OF_RANGE

            if (self.nwl <= 20):
                ramda += self.span[1]
            else:
                ramda += 5 * self.span[i]

        self.process202()

        return ERRCODE.SUCCESS

    def readVegParameters(self):

        if ((self.nPhoton == -4) or (self.nPhoton == -5)):
            return self.process201()

        # input output mode
        print("cmode: calculation mode")
        #self.cloudType = int(input("1: BRF only 2: BRF Nadir Image 3: 3D APAR\n"))
        # debug
        self.cloudType = 3

        if ((self.cloudType <= 0) or (self.cloudType >= 4)):
            print("Bad mode selection exit")
            return ERRCODE.INPUT_ERROR

        # read the condition file
        if ((self.bound != 1) and (self.bound != 2)):
            print("boundary condition should be 1 or 2.")
            print("  1: Periodic  2: Non-periodic")
            return ERRCODE.INPUT_ERROR

        if (self.cloudType != 1):
            self.process100()

        print("nth, angt: # of angle anfinished process 201 200d zenith angle(max 18)for BRF")
        print("eg. 5 10. 20. 45. 50. 70.")
        for i in range(comm.N_TH):
            comm.ANG_T[i] = float(input())

        print("nph, angp:# of angle and azimuth angle(max 36)for BRF")
        print("eg. 3 0. 90. 180.")
        for i in range(comm.N_TH):
            comm.ANG_P[i] = float(input())

        if (comm.N_TH * comm.N_PH > 700):
            print("The number of sampling angles are too huge! It should be theta*phi<348")
            return ERRCODE.INPUT_ERROR

        if (comm.N_TH > 18):
            print("The number of sampling theta are too huge! It should be theta*phi<100")
            return ERRCODE.INPUT_ERROR

        if (comm.N_PH > 36):
            print("The number of sampling phi are too huge! It should be theta*phi<100")
            return ERRCODE.INPUT_ERROR

        k = 0

        for i in range(comm.N_PH):
            for j in range(comm.N_TH):
                if (comm.ANG_T[j] > 80.0):
                    print("Zenith angle should be less than 80")
                    print(str(comm.ANG_T[j]) + " is ignored !")
                else:
                    comm.UX_RC[k] = math.sin(math.radians(comm.ANG_T[j])) * math.cos(math.radians(comm.ANG_P[i]))
                    comm.UY_RC[k] = math.sin(math.radians(comm.ANG_T[j])) * math.sin(math.radians(comm.ANG_P[i]))
                    comm.UZ_RC[k] = math.cos(math.radians(comm.ANG_T[j]))

                    k += 1

        comm.N_ANG_C = k

        self.process100()

        return ERRCODE.SUCCESS

    def readGeoParameters(self):

        f0 = q0 = 0.0
        ntha = npha = 0
        th = [0] * 18
        ph = [0] * 36

        # solar zenith angle
        # debug
        self.th0 = 60.0
        #self.th0 = float(input("the0: Solar zenith angle(degree)\n"))
        q0 = math.pi - math.radians(self.th0)

        if (self.ph0 <= math.pi):
            f0 = math.radians(self.ph0) + math.pi
        else:
            f0 = math.radians(self.ph0) - math.pi

        sin_q0 = math.sin(q0)
        cos_q0 = math.cos(q0)
        sin_fo = math.sin(f0)
        cos_fo = math.cos(f0)

        if (self.AtmMode == 2):
            return

        # radiance smapling angle
        print("Radiance at the bottom atmospheric boundary")
        print("ntha, th: # of angle and zenith angle(degree,max 18)")
        print("ex. 5 100. 120. 140. 160. 170.")
        # debug
        ntha = 1
        th[1] = 1
        # ntha = int(input())
        # for i in range(ntha):
        #     th[i] = int(input())

        print("npha, ph: # of angle and azimuth angle(degree,max 36)")
        print("ex. 3 0. 90. 180.")
        # debug
        npha = 1
        ph[1] = 1
        # npha = int(input())
        # for i in range(npha):
        #     ph[i] = int(input())

        k = 0
        for i in range(1,npha):
            for j in range(1, ntha):
                if (th[j] < 91):
                    print("Zenith angle should be greater than 91")
                    print(str(th[j]) + " is ignored !")
                else:
                    k = k + 1
                    comm.UX_RTAB[k] = math.sin(math.radians(th[j])) * math.cos(math.radians(ph[i]))
                    comm.UY_RTAB[k] = math.sin(math.radians(th[j])) * math.sin(math.radians(ph[i]))
                    comm.UX_RTAB[k] = math.cos(math.radians(th[j]))

        comm.N_RDC = k
        return ERRCODE.SUCCESS

    def readAtmParameters(self):
        imode = nspc = 0
        ctop = cbot = 0.0
        parF = 531.2593
        parQ = 2423.93994
        swF = 1351.81531
        swQ = 10213.1367

        spcf = [0.0] * 400
        spcq = [0.0] * 400
        npl = [0] * 200
        wl0d = []
        spcdf = []
        spcdq = []

        ch = ["", "hi", "lo", "lo"]

        if (self.AtmMode == 2):
            # "Only monochro wavelength calculation!"
            imode = 1
            self.RF = 1000.0
            self.RQ = 1000.0
            self.wq = 1.0
            self.nwl = 1

        else:
            # debug
            imode = 2
            #imode = int(input("imode: Integration mode 1:Monochro 2:PAR 3:Snow\n"))
            if ((imode < 0) or (imode > 4)):
                print("Mode ERR: number should less than 4 and larger than 0.")
                return ERRCODE.INPUT_ERROR

            elif (imode == 1):
                self.wl0 = float(input("wl0:wavelength (micron ex 0.55)\n"))
                self.wls = 0.2
                self.nwl = int(round((4.0 - 0.3) / self.span[1]))
                npl[1] = self.nPhotonProcess

            elif (imode == 2):
                self.wls = 0.4
                self.nwl = int(round((0.7 - 0.4) / self.span[1]))
                self.RF = parF
                self.RQ = parQ

            elif (imode == 3):
                self.wls = 0.3
                self.nwl = int(round((0.7 - 0.3) / self.span[1]))
                self.nwl += int((4.0 - 0.7) / (5.0 * self.span[1]))
                self.RF = swF
                self.RQ = swQ

            # read solar radiation
            contentFile = np.loadtxt("..\data\solar_rad")
            nspc = len(contentFile)
            for i in range(nspc):
                wl0d.append(contentFile[i][0])
                spcdf.append(contentFile[i][1])
                spcdq.append(contentFile[i][2])

            # search a spectral irradiance data in monochromatic calculation
            j = 1
            wlsd = self.wls + 0.0005

            if (imode == 1):
                for i in range(nspc):
                    if ((wlsd > self.wl0 - 0.0025) and (wlsd < self.wl0 + 0.0025)):
                        self.RF = (wl0d[i + 1] * spcdf[i] + wl0d[i] * spcdf[i + 1]) / (wl0d[i] + wl0d[i + 1])
                        self.RQ = (wl0d[i + 1] * spcdq[i] + wl0d[i] * spcdq[i + 1]) / (wl0d[i] + wl0d[i + 1])
                        spcf[j] = self.RF
                        spcq[j] = self.RQ
                        self.wq = 1.0
                        self.nwl = 1
                        break
                    wlsd += 0.001

            elif (imode == 2):
                for i in range(nspc):
                    if (abs(wl0d[i] - wlsd) < 1.0E-4):
                        for k in range(20):
                            spcf[j] += spcdf[i + k]
                            spcq[j] += spcdq[i + k]

                        spcf[j] /= self.span[1] * 1000.0
                        spcq[j] /= self.span[1] * 1000.0
                        j += 1

                        if (j> self.nwl):
                            break
                        wlsd += self.span[1]

            elif (imode == 3):
                for i in range(nspc):
                    if (abs(wl0d[i] - wlsd) < 1.0E-4):
                        if (wlsd < 0.7):
                            for k in range(20):
                                spcf[j] += spcdf[i + k]
                                spcq[j] += spcdq[i + k]

                            spcf[j] /= self.span[1] * 1000
                            spcq[j] /= self.span[1] * 1000

                        else:
                            for k in range(100):
                                spcf[j] += spcdf[i + k]
                                spcq[j] += spcdq[i + k]

                            spcf[j] /= self.span[1] * 5000
                            spcq[j] /= self.span[1] * 5000

                        j += 1
                        if (j > self.nwl):
                            break

                        if (wlsd < 0.7):
                            wlsd += self.span[1]
                        else:
                            wlsd += 5.0 * self.span[1]

            # make input photon weight for each wavelength
            sum = 0.0

            for i in range(self.nwl + 1):
                if (i < 20):
                    sum += spcf[i]
                else:
                    sum += spcf[i] * 5.0

            for i in range(self.nwl):
                if (i < 20):
                    npl[i] = round(float(self.nPhotonProcess) * spcf[i] / sum)
                else:
                    npl[i] = round(float(self.nPhotonProcess) * 5.0 * spcf[i] / sum)

            sum = 0.0

            for i in range(self.nwl):
                sum += npl[i]

            self.nPhotonProcess = int(sum)
            self.nPhoton = self.nPhotonProcess * self.Nprocess
            print("Actural number of photon is: " + str(self.nPhoton))

            # with/without atmospheric
            if (self.AtmMode == 2):
                self.atmType = 0
                self.aerosolType = 0
                self.taur = 0.0
                ctype = 0

            else:
                # read z profile
                comm.Z_GRD = np.loadtxt("..\data\zgrd")
                print("atmType: Atmospheric profile")
                print(" 1: Tropical")
                print(" 2: Mid latitude summer")
                print(" 3: Mid latitude winter")
                print(" 4: High latitude summer")
                print(" 5: High latitude winter")
                print(" 6: US standard atm.")
                self.atmType = int(input())

                if (self.atmType == 1):
                    self.rfname = "Data/gas_TR_" + ch[imode]
                elif (self.atmType == 2):
                    self.rfname = "Data/gas_TMS_" + ch[imode]
                elif (self.atmType == 3):
                    self.rfname = "Data/gas_MW_" + ch[imode]
                elif (self.atmType == 4):
                    self.rfname = "Data/gas_HS_" + ch[imode]
                elif (self.atmType == 5):
                    self.rfname = "Data/gas_HW_" + ch[imode]
                elif (self.atmType == 6):
                    self.rfname = "Data/gas_US_" + ch[imode]
                else:
                    print("Input error!")
                    return ERRCODE.INPUT_ERROR

                # read the aerosol data
                print("aerosolType: aerosol type")
                print(" 1:  Continental clean")
                print(" 2:  Continental average")
                print(" 3:  Continental polluted")
                print(" 4:  Urban")
                print(" 5:  Desert")
                print(" 6:  Maritime clean")
                print(" 7:  Maritime polluted")
                print(" 8:  Maritime Tropical")
                print(" 9:  Arctic")
                print("10:  Antactic")
                print("11:  Smoke")
                self.aerosolType = int(input())

                #AOT
                taur = int(input("tauref: AOT at 0.550 micron\n"))
                print(" - this version uses a extinction with RH=70% -")

                #current version uses a mixed extinction coef. by Iwabushi san
                self.nmix = 2

                if (self.aerosolType == 1):
                    self.fname.append("../data/opt_type1_rh0.70_" + ch[imode])
                    self.d = 8000.0     # scale height (m)
                elif (self.aerosolType == 2):
                    self.fname.append("../data/opt_type2_rh0.70_" + ch[imode])
                    self.d = 8000.0  # scale height (m)
                elif (self.aerosolType == 3):
                    self.fname.append("../data/opt_type3_rh0.70_" + ch[imode])
                    self.d = 8000.0  # scale height (m)
                elif (self.aerosolType == 4):
                    self.fname.append("../data/opt_type4_rh0.70_" + ch[imode])
                    self.d = 8000.0  # scale height (m)
                elif (self.aerosolType == 5):
                    self.fname.append("../data/opt_type5_rh0.70_" + ch[imode])
                    self.d = 2000.0  # scale height (m)
                elif ((self.aerosolType == 6) or (self.aerosolType == 8)):
                    self.fname.append("../data/opt_type6_rh0.70_" + ch[imode])
                    self.d = 1000.0  # scale height (m)
                elif (self.aerosolType == 7):
                    self.fname.append("../data/opt_type7_rh0.70_" + ch[imode])
                    self.d = 1000.0  # scale height (m)
                elif (self.aerosolType == 8):
                    self.fname.append("../data/opt_type8_rh0.70_" + ch[imode])
                    self.d = 1000.0  # scale height (m)
                elif (self.aerosolType == 9):
                    self.fname.append("../data/opt_type9_rh0.70_" + ch[imode])
                    self.d = 99000.0  # scale height (m)
                elif (self.aerosolType == 10):
                    self.fname.append("../data/opt_type10_rh0.70_" + ch[imode])
                    self.d = 99000.0  # scale height (m)
                elif (self.aerosolType == 11):
                    print("smoke aerosol under construction !!")
                    self.d = 8000.0  # scale height (m)
                    return ERRCODE.INPUT_ERROR
                else:
                    print("Input error !!")
                    return ERRCODE.INPUT_ERROR

                # read cloud data
                print("ctype: cloud type")
                print(" 0:  Cloud-free")
                print(" 1:  Stratus continental")
                print(" 2:  Stratus maritime")
                print(" 3:  Cumulus continental clean")
                print(" 4:  Culumus continental pulluted")
                print(" 5:  Culumus maritime")
                print(" 6:  Fog")
                print(" 7:  Cirrus 1 (-25degC)")
                print(" 8:  Cirrus 2 (-50 degC)")
                print(" 9:  Cirrus 3 (-50 degC + small particles)")

                self.cloudType = int(input())

                if (self.cloudType != 0):
                    self.ctaur = float(input("ctauref:COT at 0.55 micron\n" ))
                    ctop = float(input("cloud top height (m)\n"))
                    cbot = float(input("cloud bottom height (m)\n"))

                    self.cflg = 1

                    if (ctop < cbot):
                        print("cloud top should be greater than cloud bottom")
                        return ERRCODE.INPUT_ERROR

                    if (self.cloudType == 1):
                        self.fname.append("../data/opt_type101_" + ch[imode])
                    elif (self.cloudType == 2):
                        self.fname.append("../data/opt_type102_" + ch[imode])
                    elif (self.cloudType == 3):
                        self.fname.append("../data/opt_type103_" + ch[imode])
                    elif (self.cloudType == 4):
                        self.fname.append("../data/opt_type104_" + ch[imode])
                    elif (self.cloudType == 5):
                        self.fname.append("../data/opt_type105_" + ch[imode])
                    elif (self.cloudType == 6):
                        self.fname.append("../data/opt_type106_" + ch[imode])
                    elif (self.cloudType == 7):
                        self.fname.append("../data/opt_type107_" + ch[imode])
                    elif (self.cloudType == 8):
                        self.fname.append("../data/opt_type108_" + ch[imode])
                    elif (self.cloudType == 9):
                        self.fname.append("../data/opt_type109_" + ch[imode])
                    else:
                        print("Input error !!")
                        return ERRCODE.INPUT_ERROR

                    for i in range(comm.N_Z):
                        if (comm.Z_GRD[i] < cbot):
                            self.cbnz = i
                        if (comm.Z_GRD[i] > ctop):
                            self.ctnz = i
                            break

                    print(comm.Z_GRD[self.cbnz], comm.Z_GRD[self.ctnz])
                    print("clouds are located between " + str(self.ctnz) + " and " + str(self.cbnz))
        return ERRCODE.SUCCESS

    def readParameters(self):
        #self.nPhoton = int(input("np: Input number of photon\n"))
        # debug
        self.nPhoton = 10

        # fish eye simulation mode
        if (self.nPhoton == -4):
            if (self.Nprocess > 1):
                print("fish eye mode cannot work with multi-processors")
                print("please execute under single processor")
                return ERRCODE.INPUT_ERROR

            print("fish eye mode - selected")
            self.readVegParameters()
            self.surfaceType = 2
            return ERRCODE.SUCCESS

        # LAI calculation mode
        if (self.nPhoton == -5):
            if (self.Nprocess > 1):
                print("LAI mode cannot work with multi-processors")
                print("please execute under single processor")
                return ERRCODE.INPUT_ERROR

            print("LAI calculation mode - selected")
            self.readVegParameters()
            self.surfaceType = 2
            return ERRCODE.SUCCESS

        self.nPhotonProcess = int(self.nPhoton / self.Nprocess)

        # Atmospheric mode
        # debug
        self.AtmMode = 1
        #self.AtmMode = int(input("AtmMode: 1:atmospheric mode, 2: without atmospheric\n"))

        if (self.AtmMode == 2):
            self.diffuse = int(input("diffuse: Input frac. of diffuse radiation (0-1)\n"))
            if ((self.diffuse < 0.0) or (self.diffuse > 1.0)):
                print("fraction of diffuse should be 0.0-1.0... exit ")
                return ERRCODE.INPUT_ERROR

        # Get geometrical parameters
        self.readGeoParameters()

        # Get atmospheric parameters
        self.readAtmParameters()

        # vegetation parameters read / initialize
        self.surfaceType = int(input("stye: Surface mode 1: Lambertian, 2: 3-D Vegetation\n"))
        if (self.surfaceType == 1):
            for iwl in range(1, self.nwl):
                if (self.imode == 1):
                    print("Input albedo")
                else:
                    if (iwl <= 20):
                        ab1 = self.wls + self.span[iwl] * float(iwl -1)
                        ab2 = self.wls + self.span[iwl] * float(iwl)
                    else:
                        ab1 = 0.7 + self.span[iwl] * float(iwl - 21)
                        ab2 = 0.7 + self.span[iwl] * float(iwl - 20)
                    print("Input albedo: " + str(ab1) + " and " + str(ab2))
                self.alb[iwl] = float(input())

        elif (self.surfaceType == 2):
            self.readVegParameters()

        else:
            print("Bad surface type selection exit")
            return ERRCODE.INPUT_ERROR

        return ERRCODE.SUCCESS
