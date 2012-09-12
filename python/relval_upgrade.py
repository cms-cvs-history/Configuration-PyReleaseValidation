
# import the definition of the steps and input files:
from  Configuration.PyReleaseValidation.relval_steps import *

# here only define the workflows as a combination of the steps defined above:
workflows = {}

# each workflow defines a name and a list of steps to be done. 
# if no explicit name/label given for the workflow (first arg),
# the name of step1 will be used

workflows[3000] = ['', ['SingleMuPt10_UPGstd','STD','HARVESTUPSTD']]
workflows[3001] = ['', ['SingleMuPt100_UPGstd','STD','HARVESTUPSTD']]
workflows[3002] = ['', ['SingleMuPt1000_UPGstd','STD','HARVESTUPSTD']]
workflows[3003] = ['', ['SingleElectronPt10_UPGstd','STD','HARVESTUPSTD']]
workflows[3004] = ['', ['SingleElectronPt35_UPGstd','STD','HARVESTUPSTD']]
workflows[3005] = ['', ['SingleGammaPt10_UPGstd','STD','HARVESTUPSTD']]
workflows[3006] = ['', ['SingleGammaPt35_UPGstd','STD','HARVESTUPSTD']]

workflows[3007] = ['', ['FourMuPt1_200_UPGstd','STD','HARVESTUPSTD']]
workflows[3008] = ['', ['FourTauPt1_200_UPGstd','STD','HARVESTUPSTD']]
workflows[3009] = ['', ['FourElectronPt1_50_UPGstd','STD','HARVESTUPSTD']]
workflows[3010] = ['', ['FourGammaPt1_50_UPGstd','STD','HARVESTUPSTD']]
workflows[3011] = ['', ['FourPiPt1_50_UPGstd','STD','HARVESTUPSTD']]

workflows[3012] = ['', ['H120_bbar_Zll_UPGstd14','STD','HARVESTUPSTD']]#fragment in SLHCUpgradeSimulations/Configuration/python/
workflows[3013] = ['', ['H120_bbar_Zmm_UPGstd14','STD','HARVESTUPSTD']]#fragment in SLHCUpgradeSimulations/Configuration/python/
workflows[3014] = ['', ['ZZ_MMorBB_UPGstd14','STD','HARVESTUPSTD']]#fragment in SLHCUpgradeSimulations/Configuration/python/

workflows[3015] = ['', ['H130GGgluonfusion_UPGstd14','STD','HARVESTUPSTD']]
workflows[3016] = ['', ['H130GGgluonfusion_UPGstd8','STD','HARVESTUPSTD']]

workflows[3017] = ['', ['H200chargedTaus_Tauola_UPGstd14','STD','HARVESTUPSTD']]
workflows[3018] = ['', ['H200chargedTaus_Tauola_UPGstd8','STD','HARVESTUPSTD']]

workflows[3019] = ['', ['JpsiMM_UPGstd14','STD','HARVESTUPSTD']]
workflows[3020] = ['', ['JpsiMM_UPGstd8','STD','HARVESTUPSTD']]


workflows[3021] = ['', ['LM1_sfts_UPGstd14','STD','HARVESTUPSTD']]
workflows[3022] = ['', ['LM1_sfts_UPGstd8','STD','HARVESTUPSTD']]

workflows[3023] = ['', ['MinBias_UPGstd8','STD','HARVESTUPSTD']]
workflows[3024] = ['', ['MinBias_UPGstd14','STD','HARVESTUPSTD']]

workflows[3025] = ['', ['PhotonJet_Pt10_UPGstd14','STD','HARVESTUPSTD']]
workflows[3026] = ['', ['PhotonJet_Pt10_UPGstd8','STD','HARVESTUPSTD']]

workflows[3027] = ['', ['QCDForPF_UPGstd14','STD','HARVESTUPSTD']]
workflows[3028] = ['', ['QCDForPF_UPGstd8','STD','HARVESTUPSTD']]

workflows[3029] = ['', ['QCD_Pt_3000_3500_UPGstd14','STD','HARVESTUPSTD']]
workflows[3030] = ['', ['QCD_Pt_3000_3500_UPGstd8','STD','HARVESTUPSTD']]

workflows[3031] = ['', ['QCD_Pt_80_120_UPGstd14','STD','HARVESTUPSTD']]
workflows[3032] = ['', ['QCD_Pt_80_120_UPGstd8','STD','HARVESTUPSTD']]

workflows[3033] = ['', ['QQH1352T_Tauola_UPGstd14','STD','HARVESTUPSTD']]
workflows[3034] = ['', ['QQH1352T_Tauola_UPGstd8','STD','HARVESTUPSTD']]

workflows[3035] = ['', ['TTbar_Tauola_UPGstd14','STD','HARVESTUPSTD']]
workflows[3036] = ['', ['TTbar_Tauola_UPGstd8','STD','HARVESTUPSTD']]

workflows[3037] = ['', ['WE_UPGstd14','STD','HARVESTUPSTD']]
workflows[3038] = ['', ['WE_UPGstd8','STD','HARVESTUPSTD']]

workflows[3039] = ['', ['WM_UPGstd14','STD','HARVESTUPSTD']]
workflows[3040] = ['', ['WM_UPGstd8','STD','HARVESTUPSTD']]

workflows[3041] = ['', ['WJet_Pt_3000_3500_UPGstd14','STD','HARVESTUPSTD']]
workflows[3042] = ['', ['WJet_Pt_3000_3500_UPGstd8','STD','HARVESTUPSTD']]

workflows[3043] = ['', ['WJet_Pt_80_120_UPGstd14','STD','HARVESTUPSTD']]
workflows[3044] = ['', ['WJet_Pt_80_120_UPGstd8','STD','HARVESTUPSTD']]

workflows[3045] = ['', ['ZEE_UPGstd14','STD','HARVESTUPSTD']]
workflows[3046] = ['', ['ZEE_UPGstd8','STD','HARVESTUPSTD']]

workflows[3047] = ['', ['ZMM_UPGstd14','STD','HARVESTUPSTD']]
workflows[3048] = ['', ['ZMM_UPGstd8','STD','HARVESTUPSTD']]

workflows[3049] = ['', ['ZTT_UPGstd14','STD','HARVESTUPSTD']]
workflows[3050] = ['', ['ZTT_UPGstd8','STD','HARVESTUPSTD']]

workflows[3100] = ['', ['SingleMuPt10_UPGphase1','PHASE1','HARVESTUPPH1']]
workflows[3101] = ['', ['SingleMuPt100_UPGphase1','PHASE1','HARVESTUPPH1']]
workflows[3102] = ['', ['SingleMuPt1000_UPGphase1','PHASE1','HARVESTUPPH1']]
workflows[3103] = ['', ['SingleElectronPt10_UPGphase1','PHASE1','HARVESTUPPH1']]
workflows[3104] = ['', ['SingleElectronPt35_UPGphase1','PHASE1','HARVESTUPPH1']]
workflows[3105] = ['', ['SingleGammaPt10_UPGphase1','PHASE1','HARVESTUPPH1']]
workflows[3106] = ['', ['SingleGammaPt35_UPGphase1','PHASE1','HARVESTUPPH1']]

workflows[3107] = ['', ['FourMuPt1_200_UPGphase1','PHASE1','HARVESTUPPH1']]
workflows[3108] = ['', ['FourTauPt1_200_UPGphase1','PHASE1','HARVESTUPPH1']]
workflows[3109] = ['', ['FourElectronPt1_50_UPGphase1','PHASE1','HARVESTUPPH1']]
workflows[3110] = ['', ['FourGammaPt1_50_UPGphase1','PHASE1','HARVESTUPPH1']]
workflows[3111] = ['', ['FourPiPt1_50_UPGphase1','PHASE1','HARVESTUPPH1']]

workflows[3112] = ['', ['H120_bbar_Zll_UPGphase1_14','PHASE1','HARVESTUPPH1']]#fragment in SLHCUPGphase1_radeSimulations/Configuration/python/
workflows[3113] = ['', ['H120_bbar_Zmm_UPGphase1_14','PHASE1','HARVESTUPPH1']]#fragment in SLHCUPGphase1_radeSimulations/Configuration/python/
workflows[3114] = ['', ['ZZ_MMorBB_UPGphase1_14','PHASE1','HARVESTUPPH1']]#fragment in SLHCUPGphase1_radeSimulations/Configuration/python/

workflows[3115] = ['', ['H130GGgluonfusion_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3116] = ['', ['H130GGgluonfusion_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3117] = ['', ['H200chargedTaus_Tauola_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3118] = ['', ['H200chargedTaus_Tauola_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3119] = ['', ['JpsiMM_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3120] = ['', ['JpsiMM_UPGphase1_8','PHASE1','HARVESTUPPH1']]


workflows[3121] = ['', ['LM1_sfts_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3122] = ['', ['LM1_sfts_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3123] = ['', ['MinBias_UPGphase1_8','PHASE1','HARVESTUPPH1']]
workflows[3124] = ['', ['MinBias_UPGphase1_14','PHASE1','HARVESTUPPH1']]

workflows[3125] = ['', ['PhotonJet_Pt10_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3126] = ['', ['PhotonJet_Pt10_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3127] = ['', ['QCDForPF_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3128] = ['', ['QCDForPF_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3129] = ['', ['QCD_Pt_3000_3500_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3130] = ['', ['QCD_Pt_3000_3500_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3131] = ['', ['QCD_Pt_80_120_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3132] = ['', ['QCD_Pt_80_120_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3133] = ['', ['QQH1352T_Tauola_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3134] = ['', ['QQH1352T_Tauola_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3135] = ['', ['TTbar_Tauola_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3136] = ['', ['TTbar_Tauola_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3137] = ['', ['WE_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3138] = ['', ['WE_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3139] = ['', ['WM_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3140] = ['', ['WM_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3141] = ['', ['WJet_Pt_3000_3500_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3142] = ['', ['WJet_Pt_3000_3500_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3143] = ['', ['WJet_Pt_80_120_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3144] = ['', ['WJet_Pt_80_120_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3145] = ['', ['ZEE_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3146] = ['', ['ZEE_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3147] = ['', ['ZMM_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3148] = ['', ['ZMM_UPGphase1_8','PHASE1','HARVESTUPPH1']]

workflows[3149] = ['', ['ZTT_UPGphase1_14','PHASE1','HARVESTUPPH1']]
workflows[3150] = ['', ['ZTT_UPGphase1_8','PHASE1','HARVESTUPPH1']]
