######################################################
#                                                    #
#       relval_simulation_module                     #
#                                                    #  
#  This module is a collection of the simulation     # 
#  procedues. The random number service is built     #
#  by the function random_generator_service(energy)  #
#                                                    #
######################################################

import FWCore.ParameterSet.Config as cms
import relval_common_module as common

from math import pi as PI
import os
import sys

#---------------------------------------------------
# This just simplifies the use of the logger
mod_id="["+os.path.basename(sys._getframe().f_code.co_filename)[:-3]+"]"

#----------------------------
# Some useful constants:
ETA_MAX=2.5
ETA_MIN=-2.5

def simulate(step, evt_type, energy, evtnumber):
    """
    This function calls all the other functions specific for
    an event evt_type.
    """
   
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ")
    
    # Build the switch cases:
    
    # QED
    if evt_type in ("MU+","MU-","E+","E-","GAMMA") or\
       evt_type[:2]== "10":
       source=_simulate_QED\
         (step, evt_type, energy, evtnumber)
     
    elif evt_type in ("HZZMUMUMUMU", "HZZEEEE", "HZZTTTT", "HZZLLLL"):
       source=_simulate_HZZllll\
         (step, evt_type, energy, evtnumber)
     
    elif evt_type in ("B_JETS", "C_JETS", "UDS_JETS"):
       source=_simulate_udscb_jets\
         (step, evt_type, energy, evtnumber)        
    
    elif evt_type in ("QCD","TAU","SINGLE_TAU","TTBAR","ZPJJ","BSJPSIPHI","MINBIAS"):
        source=eval("_simulate_"+evt_type+"(step, evt_type, energy, evtnumber)") 
    
    elif evt_type in ("ZEE","ZTT","ZMUMU"):
        source=_simulate_Zll\
         (step, evt_type, energy, evtnumber)
    
    else:
      raise "Event type","Type not yet implemented."
             
    common.log( func_id+" Returning Source")
    
    return source

#------------------------------       

def _simulate_QED(step, evt_type, energy, evtnumber):
    """
    Here the settings for the simple generation of a muon, electron or gamma
    are stated.
    """
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ")

   # pythia ID: configure the ID of the particle through a dictionary
    py_id_dict = {"MU-":13, "MU+":-13,
                  "E-" :11, "E+" :-11,
                  "GAMMA":22}
    
    # Energy boundaries are now set:      
    lower_energy = ""
    upper_energy = ""
    
    # Build the id string of the event name:
    id_string = evt_type+" pt"+energy+" nevts "+ str(evtnumber)

    # Build the partID string
    part_id = cms.untracked.vint32 ()

    is_single = False
    # 10 Leptons
    if evt_type[:2]=="10":
        for i in range(10):
            part_id.append(py_id_dict[evt_type[2:]])
        lower_energy,upper_energy=energy_split(energy) 
      
    # Single lepton
    else:
        is_single = True
        part_id.append(py_id_dict[evt_type])
        epsilon= 0.001
        lower_energy = str ( int(energy) - epsilon) # We want a calculation and
        upper_energy = str ( int(energy) + epsilon) # the result as a string   
   
    # Build the process source
    if is_single and py_id_dict[evt_type]!="GAMMA":
        # Add the corresponding opposite sign particle.IE if e+ add e-.
        part_id.append(-1*part_id[0])
        
    source = cms.Source("FlatRandomPtGunSource",
                        psethack = cms.string(id_string),
                        firstRun = cms.untracked.uint32(1),
                        PGunParameters = cms.untracked.PSet\
                              (PartID = part_id,
                               MinEta = cms.untracked.double(ETA_MAX),
                               MaxEta = cms.untracked.double(ETA_MIN),
                               MinPhi = cms.untracked.double(-PI),
                               MaxPhi = cms.untracked.double(PI),
                               MinPt  = cms.untracked.double(lower_energy),
                               MaxPt  = cms.untracked.double(upper_energy) 
                              ),
                        Verbosity = cms.untracked.int32(0)
                       )
 
    common.log( func_id+" Returning source...")
        
    return source 
   
#---------------------------
    
def _simulate_QCD(step, evt_type, energy, evtnumber):
    """
    Here the settings for the generation of QCD events 
    """
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ")   
        
    # Recover the energies from the string:
    upper_energy, lower_energy = energy_split(energy)
    
    # Build the process source   
    source = cms.Source("PythiaSource",
                        pythiaPylistVerbosity = cms.untracked.int32(0),
                        pythiaHepMCVerbosity =cms.untracked.bool(False),
                        maxEventsToPrint = cms.untracked.int32(0),
                        PythiaParameters = cms.PSet\
                        (parameterSets = cms.vstring\
                                            ("pythiaUESettings",
                                            "processParameters"),
                            pythiaUESettings = user_pythia_ue_settings(),
                            processParameters = cms.vstring("MSEL=1",
                                                "CKIN(3)="+upper_energy,
                                                "CKIN(4)="+lower_energy))
                        )
     
    common.log( func_id+" Returning Source...")                 
    return source
 
#---------------------------------

def _simulate_MINBIAS(step, evt_type, energy, evtnumber):
    """
    Settings for MINBIAS events generation
    """
    
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ")     
    
    # Build the process source   
    source = cms.Source("PythiaSource",
                        pythiaPylistVerbosity = cms.untracked.int32(0),
                        pythiaHepMCVerbosity =cms.untracked.bool(False),
                        maxEventsToPrint = cms.untracked.int32(0),
                        PythiaParameters = cms.PSet\
                        (parameterSets = cms.vstring\
                                            ("pythiaUESettings",
                                             "processParameters"),
                            pythiaUESettings = user_pythia_ue_settings(),
                            processParameters = cms.vstring(
                                                "MSEL=0",
                                                "MSUB(11)=1",
                                                "MSUB(12)=1",
                                                "MSUB(13)=1",
                                                "MSUB(28)=1",
                                                "MSUB(53)=1",
                                                "MSUB(68)=1",
                                                "MSUB(92)=1",
                                                "MSUB(93)=1",
                                                "MSUB(94)=1",
                                                "MSUB(95)=1"))
                        )
    common.log( func_id+" Returning Source...")                 
    
    return source   
    
#-------------    
            
def _simulate_TAU(step, evt_type, energy, evtnumber):
    """    
    Here the settings for the generation of Tau events 
    """
     
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ")      
    
    # Recover the energies from the string:
    upper_energy, lower_energy = energy_split(energy)
      
    # Build the process source
    source=cms.Source("PythiaSource",
                      ParticleID = cms.untracked.int32 (-15),
                      DoubleParticle = cms.untracked.bool (True),
                      pythiaVerbosity =cms.untracked.bool(False),
                      Ptmin = cms.untracked.double (lower_energy),
                      Ptmax = cms.untracked.double (upper_energy),
                      Etamin = cms.untracked.double (ETA_MIN),
                      Etamax = cms.untracked.double(ETA_MAX),
                      Phimin = cms.untracked.double(0),
                      Phimax = cms.untracked.double(360),
                      PythiaParameters = cms.PSet\
                                 (parameterSets = cms.vstring\
                                                   ("pythiaUESettings",
                                                    "pythiaTauJets"),
                      pythiaUESettings = user_pythia_ue_settings(),
                      # Tau jets (config by A. Nikitenko)
                      # No tau -> electron
                      # No tau -> muon
                      pythiaTauJets = cms.vstring("MDME(89,1)=0", "MDME(90,1)=0"))
                      )   
    
    common.log( func_id+" Returning Source...")
     
    return source    
    
#---------------------------------

def _simulate_SINGLE_TAU(step,evt_type, energy, evtnumber):

    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ")
    
    # Energy boundaries are now set:      
    lower_energy = ""
    upper_energy = ""
    
    lower_energy,upper_energy = energy_split (energy) 
    
    source = cms.Source("FlatRandomPtGunSource",
                        psethack = cms.string(evt_type),
                        firstRun = cms.untracked.uint32(1),
                        PGunParameters = cms.untracked.PSet\
                              (PartID = (15,-15),
                               MinEta = cms.untracked.double(ETA_MAX),
                               MaxEta = cms.untracked.double(ETA_MIN),
                               MinPhi = cms.untracked.double(-PI),
                               MaxPhi = cms.untracked.double(PI),
                               MinPt  = cms.untracked.double(lower_energy),
                               MaxPt  = cms.untracked.double(upper_energy) 
                              ),
                        Verbosity = cms.untracked.int32(0)
                       )
 
    common.log( func_id+" Returning source...")
        
    return source 
#---------------------------------

def _simulate_HZZllll(step, evt_type, energy, evtnumber):
    """    
    Here the settings for the generation of Higgs->ZZ->ll events 
    The energy parameter is not used. According to the evt_type ("HZZMUMUMUMU" 
    or "HZZEEEE") the final state is chosen.
    """
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ")      
    
    # Choose between muon, tau or electron decay of the Z
    user_param_sets = "HZZllll"
    electron_flag = "0"
    muon_flag = "0"
    tau_flag = "0"
    if evt_type == "HZZEEEE":
        electron_flag = "1"
    elif evt_type == "HZZMUMUMUMU":
        muon_flag = "1"    
    elif evt_type == "HZZTTTT":
        tau_flag = "1"
    else:
        electron_flag=muon_flag=tau_flag= "1"
   
    # Prepare The Pythia params  
    params = cms.vstring(
        "PMAS(25,1)=190.0",      #mass of Higgs",
        "MSEL=0",                  
        #(D=1) to select between full user control
        #(0, then use MSUB) and some preprogrammed alternative: QCD hight pT
        #processes (1, then ISUB=11, 12, 13, 28, 53, 68), QCD low pT processes
        #(2, then ISUB=11, #12, 13, 28, 53, 68, 91, 92, 94, 95)",
        "MSTJ(11)=3",              #Choice of the fragmentation function",
        "MSTJ(41)=1",              #Switch off Pythia QED bremsshtrahlung",
        "MSTP(51)=7",             #structure function chosen",
        "MSTP(61)=0",              # no initial-state showers", 
        "MSTP(71)=0",              # no final-state showers", 
        "MSTP(81)=0",              # no multiple interactions", 
        "MSTP(111)=0",             # no hadronization", 
        "MSTU(21)=1",              
        #Check on possible errors during program
        #execution",
        "MSUB(102)=1",             #ggH",
        "MSUB(123)=1",             #ZZ fusion to H",
        "MSUB(124)=1",             #WW fusion to H",
        "PARP(82)=1.9",            #pt cutoff for multiparton interactions",
        "PARP(83)=0.5",            
        #Multiple interactions: matter distrbn parameter Registered by
        #Chris.Seez@cern.ch",
        "PARP(84)=0.4",            
        #Multiple interactions: matter distribution parameter Registered
        #by Chris.Seez@cern.ch",
        "PARP(90)=0.16",           
        #Multiple interactions: rescaling power
        #Registered by Chris.Seez@cern.ch",
        "CKIN(45)=5.",             
        #high mass cut on m2 in 2 to 2 process
        #Registered by Chris.Seez@cern.ch",
        "MSTP(25)=2",              
        #Angular decay correlations in
        #H->ZZ->4fermions Registered by Alexandre.Nikitenko@cern.ch",
        "CKIN(46)=150.",           
        #high mass cut on secondary resonance m1 in
        #2->1->2 process Registered by Alexandre.Nikitenko@cern.ch",
        "CKIN(47)=5.",             
        #low mass cut on secondary resonance m2 in
        #2->1->2 process Registered by Alexandre.Nikitenko@cern.ch",
        "CKIN(48)=150.",           
        #high mass cut on secondary resonance m2 in
        #2->1->2 process Registered by Alexandre.Nikitenko@cern.ch",
        "MDME(174,1)=0",           #Z decay into d dbar",        
        "MDME(175,1)=0",          #Z decay into u ubar",
        "MDME(176,1)=0",           #Z decay into s sbar",
        "MDME(177,1)=0",           #Z decay into c cbar",
        "MDME(178,1)=0",           #Z decay into b bbar",
        "MDME(179,1)=0",           #Z decay into t tbar",
        "MDME(182,1)=%s" %electron_flag,#Z decay into e- e+",
        "MDME(183,1)=0",           #Z decay into nu_e nu_ebar",
        "MDME(184,1)=%s" %muon_flag,#Z decay into mu- mu+",
        "MDME(185,1)=0",           #Z decay into nu_mu nu_mubar",
        "MDME(186,1)=%s" %tau_flag,#Z decay into tau- tau+",
        "MDME(187,1)=0",          #Z decay into nu_tau nu_taubar",
        "MDME(210,1)=0",           #Higgs decay into dd",
        "MDME(211,1)=0",           #Higgs decay into uu",
        "MDME(212,1)=0",           #Higgs decay into ss",
        "MDME(213,1)=0",           #Higgs decay into cc",
        "MDME(214,1)=0",           #Higgs decay into bb",
        "MDME(215,1)=0",           #Higgs decay into tt",
        "MDME(216,1)=0",           #Higgs decay into",
        "MDME(217,1)=0",           #Higgs decay into Higgs decay",
        "MDME(218,1)=0",           #Higgs decay into e nu e",
        "MDME(219,1)=0",           #Higgs decay into mu nu mu",
        "MDME(220,1)=0",           #Higgs decay into tau nu tau",
        "MDME(221,1)=0",           #Higgs decay into Higgs decay",
        "MDME(222,1)=0",           #Higgs decay into g g",
        "MDME(223,1)=0",           #Higgs decay into gam gam",
        "MDME(224,1)=0",           #Higgs decay into gam Z",
        "MDME(225,1)=1",           #Higgs decay into Z Z",
        "MDME(226,1)=0",           #Higgs decay into W W"
        ) 

    # Build the process source   
    source=cms.Source('PythiaSource',
#                       maxEvents = cms.untracked.int32\
#                                      (int(evtnumber)),
                      pythiaVerbosity =cms.untracked.bool(False),
                      PythiaParameters = cms.PSet\
                       (parameterSets = cms.vstring(user_param_sets),
                        pythiaHZZllll = params
                       )     
                     )

    common.log( func_id+" Returning Source...")
     
    return source      

#---------------------------------

def _simulate_udscb_jets\
        (step, evt_type, energy, evtnumber):
    """
    Here the settings necessary to udscb jets generation are added. According
    to the flavour the Pythia parameters are changed slightly.
    For the time being the energy parameter is not used.
    """
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ")
    
    # Recover the energies from the string:
    upper_energy, lower_energy = energy_split(energy)
   
    # According to the evt_type build the Pythia settings:
    pythia_jet_settings=cms.vstring("MSEL=0")  # User defined process
    if evt_type == "UDS_JETS":
        pythia_jet_settings+=cms.vstring("MSUB(11)=1") #qq->qq'
        common.log( func_id+" Including settings for uds jets")
    else:
        pythia_jet_settings+=cms.vstring("MSUB(81)=1", #qq->QQ massive
                                         "MSUB(82)=1") #gg->QQ massive
        if evt_type == "C_JETS":
             pythia_jet_settings+=cms.vstring("MSTP(7)=4") #ccbar
             common.log( func_id+" Including settings for c jets")
        else:
             pythia_jet_settings+=cms.vstring("MSTP(7)=5") #bbbar
             common.log( func_id+" Including settings for b jets")
             
    # Common part to all cases         
    pythia_common=cms.vstring("CKIN(3)="+upper_energy,  # Pt low cut 
                              "CKIN(4)="+lower_energy,  # Pt high cut
                              "CKIN(13)=0.",            # eta min            
                              "CKIN(14)=2.5",           # etamax           
                              "CKIN(15)=-2.5",          # -etamin 
                              "CKIN(16)=0"              # -etamax
                              )
    pythia_jet_settings+=pythia_common
    
    # Build the process source
    source=cms.Source('PythiaSource',
                      pythiaVerbosity =cms.untracked.bool(True),
                      PythiaParameters = cms.PSet\
                               (parameterSets = cms.vstring\
                                                   ("pythiaUESettings","pythiaJets"),
                                pythiaUESettings = user_pythia_ue_settings(),
                                pythiaJets = pythia_jet_settings
                               )
                     )                       
   
    common.log(func_id+" Returning Source...")
     
    return source

#-----------------------------------
    
def _simulate_TTBAR(step, evt_type, energy, evtnumber):
    """
    Here the settings for the ttbar pairs are added to the process.
    """
      
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log(func_id+" Entering... ")      
    
    # Build the process source    
    source=cms.Source('PythiaSource',
#                       maxEvents = cms.untracked.int32\
#                                         (int(evtnumber)),
                      pythiaPylistVerbosity=cms.untracked.int32(0),
                      pythiaHepMCVerbosity=cms.untracked.bool(False),
                      maxEventsToPrint = cms.untracked.int32(0),                       
                      PythiaParameters = cms.PSet\
                                (parameterSets = cms.vstring\
                                                   ("pythiaUESettings",
                                                    "processParameters"),
                                pythiaUESettings = user_pythia_ue_settings(),
                                # Tau jets (config by A. Nikitenko)
                                # No tau -> electron
                                # No tau -> muon
                                processParameters =cms.vstring\
                                    ("MSEL=0",       # userdef process
                                     "MSUB(81)=1",   # qqbar->QQbar
                                     "MSUB(82)=1",   # gg to QQbar
                                     "MSTP(7)=6",    # flavour top
                                     "PMAS(6,1)=175" # top mass
                                     )
                                ) 
                      )  

    common.log(func_id+" Returning Source...")
     
    return source   
 
#---------------------------------

def _simulate_Zll(step, evt_type, energy, evtnumber):
    """
    Here the settings for the Z ee simulation are added to the process.
    Energy parameter is not used.
    """
      
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ")      

    # Choose between muon or electron decay of the Z
    user_param_sets = "pythiaZll"
    electron_flag = "0"
    muon_flag = "0"
    tau_flag = "0"
    if evt_type == "ZEE":
        electron_flag = "1"
    elif evt_type == "ZMUMU":
        muon_flag = "1"    
    elif evt_type == "ZTT":
        tau_flag = "1"
    else:
        electron_flag=muon_flag=tau_flag= "1"    
    
    pythia_param_sets = cms.vstring(
                 "MSEL = 11 ",           
                 "MDME( 174,1) = 0",            #Z decay into d dbar",
                 "MDME( 175,1) = 0",            #Z decay into u ubar",
                 "MDME( 176,1) = 0",            #Z decay into s sbar",
                 "MDME( 177,1) = 0",            #Z decay into c cbar",
                 "MDME( 178,1) = 0",            #Z decay into b bbar",
                 "MDME( 179,1) = 0",            #Z decay into t tbar",
                 "MDME( 182,1) = %s" %electron_flag,#Z decay into e- e+",
                 "MDME( 183,1) = 0",            #Z decay into nu_e nu_ebar",
                 "MDME( 184,1) = %s" %muon_flag,#Z decay into mu- mu+",
                 "MDME( 185,1) = 0",            #Z decay into nu_mu nu_mubar",
                 "MDME( 186,1) = %s" %tau_flag, #Z decay into tau- tau+",
                 "MDME( 187,1) = 0",            #Z decay into nu_tau nu_taubar",
                 "MSTJ( 11) = 3",    #Choice of the fragmentation function",
                 "MSTP( 2) = 1",            #which order running alphaS",
                 "MSTP( 33) = 0",            #(D=0) ",
                 "MSTP( 51) = 7",            #structure function chosen",
                 "MSTP( 81) = 1",            #multiple parton interactions 1 is
                                             #Pythia default,
                 "MSTP( 82) = 4",            #Defines the multi-parton model",
                 "PARJ( 71) = 10.",            #for which ctau  10 mm",
                 "PARP( 82) = 1.9",   #pt cutoff for multiparton interactions",
                 "PARP( 89) = 1000.", #sqrts for which PARP82 is set",
                 "PARP( 83) = 0.5", #Multiple interactions: matter distrbn
                                    #parameter Registered byChris.Seez@cern.ch
                 "PARP( 84) = 0.4",   #Multiple interactions: matterdistribution
                                  #parameter Registered by Chris.Seez@cern.ch
                 "PARP( 90) = 0.16",  #Multiple interactions:rescaling power
                                      #Registered by Chris.Seez@cern.ch
                 "CKIN( 1) = 40.",            #(D=2. GeV)
                 "CKIN( 2) = -1.",            #(D=-1. GeV)      \
                 )     
                 
    # Build the process source
    source=cms.Source('PythiaSource', 
                      PythiaParameters = cms.PSet\
                               (parameterSets = cms.vstring(user_param_sets),
                                pythiaZll=pythia_param_sets )
                     )

    common.log(func_id+" Returning Source...")
     
    return source   
    
#---------------------------------

def _simulate_BSJPSIPHI(step, evt_type, energy, evtnumber):
    """
    Here the settings for the Bs ->J Phi decay simulation of the are added to
    the process. 
    """
       
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log(func_id+" Entering... ")                    

    myParameters = cms.vstring(
        # MSEL=1 is best, but MSEL=5 is faster, so handy for debugging.
        'MSEL=5', #  Heavy quark 
        #  'MSEL=1',

        # B decays
        'MDME(953,1)=0',
        'MDME(954,1)=0',
        'MDME(955,1)=0',
        'MDME(956,1)=0',
        'MDME(957,1)=0',
        'MDME(958,1)=0',
        'MDME(959,1)=0',
        'MDME(960,1)=0',
        'MDME(961,1)=0',
        'MDME(962,1)=0',
        'MDME(963,1)=0',
        'MDME(964,1)=0',
        'MDME(965,1)=0',
        'MDME(966,1)=0',
        'MDME(967,1)=0',
        'MDME(968,1)=0',
        'MDME(969,1)=0',
        'MDME(970,1)=0',
        'MDME(971,1)=0',
        'MDME(972,1)=0',
        'MDME(973,1)=0',
        'MDME(974,1)=0',
        'MDME(975,1)=0',
        'MDME(976,1)=0',
        'MDME(977,1)=0',
        'MDME(978,1)=0',
        'MDME(979,1)=0',
        'MDME(980,1)=0',
        'MDME(981,1)=0',
        'MDME(982,1)=1', # Bs->J/psi+phi',
        'MDME(983,1)=0',
        'MDME(984,1)=0',
        'MDME(985,1)=0',
        'MDME(986,1)=0',
        'MDME(987,1)=0',
        'MDME(988,1)=0',
        'MDME(989,1)=0',
        'MDME(990,1)=0',
        'MDME(991,1)=0',
 
        # J/psi decays
        'MDME(858,1)=0', # J/psi->e+e-',
        'MDME(859,1)=1', # J/psi->mumu',
        'MDME(860,1)=0',

        'MDME(656,1)=1', # Bs->J/psi+phi',
        'MDME(657,1)=0',
        'MDME(658,1)=0',
        'MDME(659,1)=0',
        'MDME(660,1)=0',
        'MDME(661,1)=0',
        'MDME(662,1)=0',
        'MDME(663,1)=0',
        'MDME(664,1)=0',
        'MDME(665,1)=0',
        'MDME(666,1)=0') # phi->K+K-
    
    # Build the process source    
    source=cms.Source('PythiaSource',
#                       maxEvents = cms.untracked.int32\
#                                         (int(evtnumber)),
                      pythiaPylistVerbosity=cms.untracked.int32(1),
                      pythiaHepMCVerbosity=cms.untracked.bool(False),
                      maxEventsToPrint = cms.untracked.int32(0), 
                      PythiaParameters = cms.PSet\
                            (parameterSets = cms.vstring\
                                            ("pythiaUESettings",
                                             "processParameters"),
                             pythiaUESettings = user_pythia_ue_settings(),
                             processParameters =  myParameters)
                     )
            
    common.log( func_id+" Returning Source...")
     
    return source                        
              
#---------------------------------

def _simulate_ZPJJ(step, evt_type, energy, evtnumber):
    """
    Here the settings for the Zprime to JJ simulation are added to the
    process. 
    """
    
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log(func_id+" Entering... ")       
    
    user_param_sets=cms.vstring(
	    'PMAS(32,1)= 700.',            # mass of Zprime',
	    'MSEL=0',          # (D=1) to select between full user
                            # control (0, then use MSUB) and some
                            # preprogrammed alternative',
        'MSTP(44) = 3',                # only select the Z process',
        'MSUB(141) = 1',               # ff  gamma z0 Z0',

        'MSTJ(11)=3',           # Choice of the fragmentation function',
        'MSTJ(22)=2',                 # Decay those unstable particles',
        'MSTP(2)=1',                  # which order running alphaS',
        'MSTP(33)=0',                 # (D=0) inclusion of K factors in (=0:
                                        # none, i.e. K=1)',
        'MSTP(51)=7',                 # structure function chosen',
        'MSTP(81)=1',                 # multiple parton interactions 1 is
                                        # Pythia default',
        'MSTP(82)=4',                 # Defines the multi-parton model',
        'MSTU(21)=1',                 # Check on possible errors during
                                        # program execution',
        'PARJ(71)=10.',               # for which ctau  10 mm',
        'PARP(82)=1.9',               # pt cutoff for multiparton
                                        # interactions',
        'PARP(89)=1000.',             # sqrts for which PARP82 is set',
        'PARP(84)=0.4',               # Multiple interactions: matter
                                        # distribution Registered by
                                        # Chris.Seez@cern.ch',
        'PARP(90)=0.16',              # Multiple interactions: rescaling
                                        # power Registered by
                                        # Chris.Seez@cern.ch',
        'PMAS(5,1)=4.2',              # mass of b quark',
        'PMAS(6,1)=175.',             # mass of top quark',
        'PMAS(23,1)=91.187',          # mass of Z',
        'PMAS(24,1)=80.22',           # mass of W',

   	    'MDME(289,1)= 1',            # d dbar',
   	    'MDME(290,1)= 1',            # u ubar',
   	    'MDME(291,1)= 1',            # s sbar',
   	    'MDME(292,1)= 1',            # c cbar',
   	    'MDME(293,1)= 0',            # b bar',
   	    'MDME(294,1)= 0',            # t tbar',
   	    'MDME(295,1)= 0',            # 4th gen Q Qbar',
   	    'MDME(296,1)= 0',            # 4th gen Q Qbar',
   	    'MDME(297,1)= 0',            # e e',
   	    'MDME(298,1)= 0',            # neutrino e e',
   	    'MDME(299,1)= 0',            # mu mu',
   	    'MDME(300,1)= 0',            # neutrino mu mu',
   	    'MDME(301,1)= 0',            # tau tau',
   	    'MDME(302,1)= 0',            # neutrino tau tau',
   	    'MDME(303,1)= 0',            # 4th generation lepton',
   	    'MDME(304,1)= 0',            # 4th generation neutrino',
   	    'MDME(305,1)= 0',            # W W',
   	    'MDME(306,1)= 0',            # H  charged higgs',
   	    'MDME(307,1)= 0',            # Z ',
   	    'MDME(308,1)= 0',            # Z',
   	    'MDME(309,1)= 0',            # sm higgs',
   	    'MDME(310,1)= 0',            # weird neutral higgs HA'
    )
    
    # Build the process source
    source=cms.Source('PythiaSource',
#                       maxEvents = cms.untracked.int32\
#                                           (int(evtnumber)),
                      pythiaVerbosity = cms.untracked.bool (False),
                      PythiaParameters = cms.PSet\
                           (parameterSets = cms.vstring("pythiaDefault",
                                                        "myParameters"),
                            pythiaDefault= cms.vstring \
                               ("PMAS(5,1)=4.8" ,# b quark mass
                                "PMAS(6,1)=172.3" ), #t quark mass
                            myParameters = user_param_sets)
                     )
                               
    common.log( func_id+" Returning Source...")
     
    return source                                                
                                                   
#-----------------------------------

def energy_split(energy):
    """
    Extract from a string of the form "lowenergy*highenergy" two 
    bounds. It checks on its consistency. If the format is unknown 
    the program stops.
    """
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ") 
    
    separator_list = ["-", #fault tolerance is good
                      "_",
                      "*",
                      "/",
                      ";",
                      ","]
    for separator in separator_list:
        if energy.count(separator)==1:
            common.log( func_id+" Found separator in energy string...") 
            low,high = energy.split(separator)
            if float(high) > float(low):
                common.log(func_id+" Returning Energy...")
                return (low,high)
    
    raise "Energy Format: ","Unrecognised energy format."

#-----------------------------------

def build_filter(evt_type):
    """
    Builds the filter for "BSJPSIPHI" and "UDS_JETS" and returns the
    EDFilter.
    """
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log( func_id+" Entering... ") 

    if evt_type=="BSJPSIPHI":
        bsfilter=cms.EDFilter("BsJpsiPhiFilter",
                              leptonType=cms.int32(13),
                              leptonEtaMin=cms.double(-2.4),
                              leptonEtaMax=cms.double(+2.4),
                              leptonPtMin=cms.double(2.0),
                              hadronType=cms.int32(321),
                              hadronEtaMin=cms.double(-2.4),
                              hadronEtaMax=cms.double(+2.4),
                              hadronPtMin=cms.double(0.8)
                             )
        common.log(func_id+" Returning BsJpsiPhiFilter...")
        return bsfilter
    elif evt_type=="UDS_JETS":
        udsfilter=cms.EDFilter("JetFlavourFilter", jetType = cms.int32(1) )
        
        common.log(func_id+" Returning JetFlavourFilter...")
        return udsfilter
            
#-----------------------------------

def user_pythia_ue_settings():
    """
    The function simply returns a cms.vstring which is a summary of the 
    Pythia settings for the event generation
    """
    func_id=mod_id+"["+sys._getframe().f_code.co_name+"]"
    common.log(func_id+" Returning PythiaUE settings...")    
    return cms.vstring(
          'MSTJ(11)=3',                                    
          'MSTJ(22)=2',     # Decay those unstable particles
          'PARJ(71)=10.',   # forwhich ctau  10 mm
          'MSTP(2)=1',      # which order running alphaS
          'MSTP(33)=0',     # no Kfactors in hard cross sections
          'MSTP(51)=7',     # structure function chosen
          'MSTP(81)=1',     # multiple parton interactions 1 is Pythia default
          'MSTP(82)=4',     # Defines the multi-parton model
          'MSTU(21)=1',     # Check on possible errors during program exec
          'PARP(82)=1.9409',# ptcutoff for multiparton interactions
          'PARP(89)=1960.', # sqrts for which PARP82 is set
          'PARP(83)=0.5',   # Multiple interactions: matter distrbn parameter
          'PARP(84)=0.4',   # Multiple interactions: matter distribution param
          'PARP(90)=0.16',  # Multiple interactions: rescaling power
          'PARP(67)=2.5',   # amount of initial-state radiation
          'PARP(85)=1.0',   # gluon prod. mechanism in MI
          'PARP(86)=1.0',   # gluonprod. mechanism in MI
          'PARP(62)=1.25',  
          'PARP(64)=0.2',   
          'MSTP(91)=1',     
          'PARP(91)=2.1',   # ktdistribution
          'PARP(93)=15.0')
