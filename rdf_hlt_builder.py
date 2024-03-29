import pathlib
from os import uname

import ROOT as rt

OUT_DIR = "reports/weekly/2023-09-14"
T2_OUT_DIR = "/storage/af/user/psimmerl/LLP/mdc_analysis"  # os.getcwd()
LOCAL_OUT_DIR = "/home/psimmerl/LLP/mdc_analysis"  # os.getcwd()

DATA_VERSION = "6"

T2_DATA_DIR = "/storage/cms/store/user/christiw/displacedJetMuonAnalyzer/Run3/V1p19"
LOCAL_DATA_DIR = "/home/psimmerl/LLP/mdc_analysis/data/raw"  # os.getcwd() + "/data/raw"
DATA_DIR = "TIER2" if "caltech" in uname()[1] else "LOCAL"

FN_MC = "ggH_HToSSTobbbb_MH-125_MS-15_CTau1000_13p6TeV_1pb_weighted"
FN_R3 = "DisplacedJet-EXOCSCCluster_Run2022EFG-PromptReco-v1_goodLumi"

# **************************** #
if "TIER2" in DATA_DIR:
    OUT_DIR = f"{T2_OUT_DIR}/{OUT_DIR}"
    FN_MC = f"{T2_DATA_DIR}/MC_Summer22EE/v1/sixie/v{DATA_VERSION}/normalized/{FN_MC}.root"
    FN_R3 = f"{T2_DATA_DIR}/Data2022/v{DATA_VERSION}/normalized/{FN_R3}.root"
else:
    OUT_DIR = f"{LOCAL_OUT_DIR}/{OUT_DIR}"
    FN_MC = f"{LOCAL_DATA_DIR}/{FN_MC}_v{DATA_VERSION}.root"
    FN_R3 = f"{LOCAL_DATA_DIR}/{FN_R3}_v{DATA_VERSION}.root"
# pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
# **************************** #

rt.EnableImplicitMT(4)
print('Enabled ROOT\'s implicit multithreading (sometimes causes a crash)')

print('')

tag = 'pedro'
FN_MC = "/home/psimmerl/mds_analysis/data/processed/mc_pedro.root"
FN_R3 = "/home/psimmerl/mds_analysis/data/processed/data_pedro.root"

for rdfn in ("mc", "r3"):
    rdf = rt.RDataFrame("MuonSystem", FN_MC if rdfn == "mc" else FN_R3)
    count_raw, wtsum_raw = rdf.Count(), rdf.Sum("weight") 

    print(f"loaded rdf {rdfn}")
    columns = [n for n in rdf.GetColumnNames()]
    columns.remove("HLTDecision")


    # CSC-CSC Category, CscCluster_Loose
    rdf566 = rdf.Filter("HLTDecision[566] && (nCscRechitClusters > 1)") # At least 2 CSC clusters

    fn_out = f"data/processed/{rdfn}_{tag}_hlt566.root"
    print(f"snapshotting rdf {rdfn} with HLT_CscClusterLoose (CSC-CSC)")
    print(f"    {fn_out}")
    rdf566 = rdf566.Snapshot("MuonSystem", fn_out, columns)

    count_cut, wtsum_cut = rdf566.Count(), rdf566.Sum("weight") 
    print(f"  Count  Raw = {count_raw.GetValue():,.0f}")
    print(f"  Count  Cut = {count_cut.GetValue():,.0f}")
    print(f"  Weight Raw = {wtsum_raw.GetValue():,.3f}")
    print(f"  Weight Cut = {wtsum_cut.GetValue():,.3f}")


    # CSC-DT Category, HLT_L1CSCCluster_DTCluster50
    rdf569 = rdf.Filter("HLTDecision[569] && ( (nCscRechitClusters > 0) && (nDtRechitClusters > 0) )") # At least 1 CSC and 1 DT

    fn_out = f"data/processed/{rdfn}_{tag}_hlt569.root"
    print(f"snapshotting rdf {rdfn} with HLT_L1CSCCluster_DTCluster50 (CSC-DT)")
    print(f"    {fn_out}")
    rdf569 = rdf569.Snapshot("MuonSystem", fn_out, columns)

    count_cut, wtsum_cut = rdf569.Count(), rdf569.Sum("weight") 
    print(f"  Count  Raw = {count_raw.GetValue():,.0f}")
    print(f"  Count  Cut = {count_cut.GetValue():,.0f}")
    print(f"  Weight Raw = {wtsum_raw.GetValue():,.3f}")
    print(f"  Weight Cut = {wtsum_cut.GetValue():,.3f}")


    # done
    print(f"finished rdf {rdfn}\n")
