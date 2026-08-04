const STORAGE_KEY = "islet-cell-state-model-v2";
const LEGACY_STORAGE_KEY = "beta-cell-state-model-v1";

const GITHUB_OWNER = "kjgaulton";
const GITHUB_REPO = "cell-state-browser";
const GITHUB_BRANCH = "main";
const GITHUB_TOKEN_KEY = "github-pat-cell-state-browser";

const ACTIVITY_LEVELS = [
  { value: -2, label: "down" },
  { value: -1, label: "low" },
  { value: 0, label: "baseline" },
  { value: 1, label: "up" },
  { value: 2, label: "high" },
  { value: 3, label: "very high" }
];

const seedCellTypes = [
  {
    id: "beta-cell",
    name: "Beta cell",
    programs: [
      {
        id: "identity",
        name: "Beta-cell identity",
        category: "Core identity",
        function: "Mature beta-cell transcriptional identity",
        genes: ["INS", "IAPP", "PDX1", "NKX6-1", "MAFA", "UCN3", "PCSK1", "SLC30A8"]
      },
      {
        id: "insulin",
        name: "Insulin biosynthesis",
        category: "Secretion",
        function: "Production and processing of insulin",
        genes: ["INS", "PCSK1", "PCSK2", "CPE", "PAM", "IAPP"]
      },
      {
        id: "secretion",
        name: "Stimulus-secretion coupling",
        category: "Secretion",
        function: "Glucose sensing and insulin release",
        genes: ["GCK", "KCNJ11", "ABCC8", "CACNA1A", "CACNA1D", "SNAP25", "STX1A", "SYT7"]
      },
      {
        id: "granule",
        name: "Secretory granule biology",
        category: "Secretion",
        function: "Granule formation, trafficking, and docking",
        genes: ["CHGA", "CHGB", "SCG2", "SCGN", "VAMP2", "RAB3A", "RPH3AL"]
      },
      {
        id: "metabolism",
        name: "Oxidative metabolism",
        category: "Metabolism",
        function: "ATP production and glucose oxidation",
        genes: ["IDH3A", "SDHB", "NDUFA", "COX", "ATP5"]
      },
      {
        id: "mito-qc",
        name: "Mitochondrial quality control",
        category: "Metabolism",
        function: "Mitochondrial maintenance",
        genes: ["PINK1", "PRKN", "OPA1", "MFN2", "BNIP3"]
      },
      {
        id: "er-folding",
        name: "ER protein folding",
        category: "Protein homeostasis",
        function: "Folding of secreted proteins",
        genes: ["HSPA5", "PDIA4", "PDIA6", "CALR", "CANX"]
      },
      {
        id: "upr",
        name: "Unfolded protein response",
        category: "Protein homeostasis",
        function: "Adaptive ER stress",
        genes: ["XBP1", "ATF6", "EIF2AK3", "DDIT3", "HERPUD1", "DNAJB9", "ATF4"]
      },
      {
        id: "oxidative-stress",
        name: "Oxidative stress response",
        category: "Stress response",
        function: "Detoxification of reactive oxygen species",
        genes: ["TXN", "TXNIP", "PRDX1", "PRDX4", "GPX1", "SOD2"]
      },
      {
        id: "autophagy",
        name: "Autophagy / lysosome",
        category: "Protein homeostasis",
        function: "Recycling damaged proteins and organelles",
        genes: ["SQSTM1", "MAP1LC3B", "ATG", "CTSB", "CTSD"]
      },
      {
        id: "proteasome",
        name: "Proteasome",
        category: "Protein homeostasis",
        function: "Protein degradation",
        genes: ["PSMA", "PSMB", "PSMC"]
      },
      {
        id: "cell-cycle",
        name: "Cell cycle",
        category: "Cell fate",
        function: "Cell proliferation",
        genes: ["MKI67", "TOP2A", "CCNB1", "CDK1"]
      },
      {
        id: "dna-damage",
        name: "DNA damage",
        category: "Cell fate",
        function: "DNA repair and damage response",
        genes: ["GADD45A", "CDKN1A", "ATM", "BRCA1"]
      },
      {
        id: "hypoxia",
        name: "Hypoxia",
        category: "Stress response",
        function: "Oxygen response",
        genes: ["VEGFA", "EGLN3", "HIF1A targets"]
      },
      {
        id: "interferon",
        name: "Interferon response",
        category: "Immune response",
        function: "Antiviral and inflammatory signaling",
        genes: ["STAT1", "IFIT1", "IFIT3", "IFI44L", "MX1", "ISG15"]
      },
      {
        id: "antigen",
        name: "Antigen presentation",
        category: "Immune response",
        function: "Immune visibility",
        genes: ["B2M", "HLA-A", "HLA-B", "HLA-C", "TAP1", "TAP2"]
      },
      {
        id: "cytokine",
        name: "Cytokine signaling",
        category: "Immune response",
        function: "TNF, IL1, and JAK-STAT signaling",
        genes: ["SOCS1", "NFKBIA", "CCL2", "CXCL10"]
      },
      {
        id: "dediff",
        name: "Dedifferentiation",
        category: "Cell fate",
        function: "Loss of mature identity",
        genes: ["ALDH1A3", "SOX9", "NEUROG3", "FOSL1"]
      },
      {
        id: "development",
        name: "Developmental plasticity",
        category: "Cell fate",
        function: "Progenitor-like programs",
        genes: ["PAX4", "NKX2-2", "ISL1", "HES1"]
      },
      {
        id: "transdiff",
        name: "Beta-to-alpha transdifferentiation",
        category: "Cell fate",
        function: "Ectopic activation of alpha-cell lineage genes with loss of beta-cell identity",
        genes: ["ARX", "MAFB", "GCG", "IRX2"]
      },
      {
        id: "senescence",
        name: "Senescence",
        category: "Cell fate",
        function: "Stable stress and cell-cycle arrest",
        genes: ["CDKN2A", "CDKN1A", "GDF15", "SERPINE1"]
      },
      {
        id: "apoptosis",
        name: "Apoptosis",
        category: "Cell fate",
        function: "Programmed cell death",
        genes: ["BAX", "BBC3", "PMAIP1", "CASP3"]
      },
      {
        id: "survival",
        name: "Survival",
        category: "Cell fate",
        function: "Anti-apoptotic programs",
        genes: ["BCL2L1", "MCL1", "MANF"]
      },
      {
        id: "zinc",
        name: "Zinc homeostasis",
        category: "Structural maintenance",
        function: "Insulin crystallization",
        genes: ["SLC30A8", "MT1X", "MT2A"]
      },
      {
        id: "calcium",
        name: "Calcium homeostasis",
        category: "Structural maintenance",
        function: "Calcium handling",
        genes: ["ATP2A2", "RYR2", "ITPR3", "CALM"]
      },
      {
        id: "cytoskeleton",
        name: "Cytoskeleton",
        category: "Structural maintenance",
        function: "Vesicle movement",
        genes: ["ACTB", "TUBA1B", "MYH9"]
      },
      {
        id: "ecm",
        name: "ECM interaction",
        category: "Structural maintenance",
        function: "Adhesion and matrix sensing",
        genes: ["ITGA6", "ITGB1", "LAMB1", "COL4A1"]
      },
      {
        id: "lipid-handling",
        name: "Lipid uptake and handling",
        category: "Metabolism",
        function: "Fatty acid uptake, intracellular lipid trafficking, and lipid droplet buffering",
        genes: ["CD36", "FABP3", "FABP5", "PLIN2", "DGAT1", "DGAT2"]
      },
      {
        id: "fatty-acid-oxidation",
        name: "Fatty acid oxidation",
        category: "Metabolism",
        function: "Mitochondrial beta-oxidation and lipid-derived energy metabolism",
        genes: ["CPT1A", "CPT2", "ACADVL", "ACADM", "HADHA", "PPARA"]
      },
      {
        id: "lipotoxic-stress",
        name: "Lipotoxic stress",
        category: "Stress response",
        function: "Cellular stress from excess saturated fatty acids and toxic lipid intermediates",
        genes: ["SCD", "ELOVL6", "ACSL4", "CERS2", "CERS6", "DDIT3"]
      }
    ],
    states: [
      {
        id: "mature-functional",
        name: "Mature functional beta cell",
        phenotype: "Canonical healthy beta cell",
        genes: ["INS", "IAPP", "PDX1", "NKX6-1", "MAFA", "UCN3", "PCSK1", "SLC30A8", "GCK", "CHGA", "ABCC8", "KCNJ11"],
        notes: "Canonical mature beta-cell identity/function panel (transcription factors, hormone, prohormone convertase, glucose sensing, KATP channel); textbook/consensus markers used across human islet single-cell atlases (e.g., Segerstolpe et al. 2016 Cell Metab).",
        activities: {
          identity: 3, insulin: 3, secretion: 3, granule: 2, metabolism: 2,
          "er-folding": 0, proteasome: 1, upr: -1, interferon: -1,
          "cell-cycle": -1, senescence: -1, apoptosis: -1
        }
      },
      {
        id: "secretory-adapted",
        name: "Secretory-adapted beta cell",
        phenotype: "Prolonged insulin demand; compensation, obesity, or pregnancy",
        genes: ["INS", "IAPP", "HSPA5", "XBP1", "PDIA6", "CHGA", "SCGN", "CPE", "PCSK1", "PCSK2", "PAM", "VAMP2", "CALR"],
        notes: "Reflects physiological (adaptive, non-terminal) UPR activation and increased prohormone-processing/secretory-granule capacity that accompanies compensatory insulin demand in pregnancy/obesity, distinct from the maladaptive terminal UPR of the er-stressed state (Lipson et al. 2006; Scheuner & Kaufman 2008 Endocr Rev).",
        activities: {
          identity: 2, insulin: 3, secretion: 2, granule: 2, "er-folding": 2,
          upr: 1, metabolism: 2, autophagy: 1, "oxidative-stress": 1, apoptosis: -1
        }
      },
      {
        id: "er-stressed",
        name: "ER-stressed beta cell",
        phenotype: "Common across T2D, CFRD, and cytokine exposure",
        genes: ["DDIT3", "HSPA5", "HERPUD1", "DNAJB9", "PDIA4", "ATF4", "XBP1", "ATF6", "EIF2AK3", "TRIB3", "ATF3", "PPP1R15A", "CALR"],
        notes: "Terminal/maladaptive UPR signature (PERK-ATF4-CHOP and IRE1-XBP1 arms) documented in T1D/T2D/CFRD islets and cytokine-exposed beta cells (Marhfour et al. 2012 Diabetologia; Eizirik & Cnop reviews).",
        activities: {
          identity: -2, insulin: -2, "er-folding": 2, upr: 3,
          "oxidative-stress": 2, proteasome: 1, autophagy: 1, apoptosis: 1
        }
      },
      {
        id: "interferon-activated",
        name: "Inflammatory response beta cell",
        phenotype: "Typical of early T1D or cytokine-driven inflammatory exposure",
        genes: ["STAT1", "IFIT1", "IFI44L", "MX1", "ISG15", "HLA-A", "B2M", "CXCL10", "HLA-B", "TAP1", "IRF1", "OAS1", "PSMB9"],
        notes: "Type I/II interferon-stimulated gene and MHC-I hyperexpression signature described in early/insulitic T1D beta cells (Russell et al. 2019 Diabetes; Marroqui et al. 2017 studies of cytokine-exposed islets).",
        activities: {
          identity: -1, interferon: 3, antigen: 3, cytokine: 2,
          upr: 1, "oxidative-stress": 1
        }
      },
      {
        id: "glucolipotoxicity",
        name: "Glucolipotoxicity beta cell",
        phenotype: "Combined high glucose and elevated lipid exposure, often associated with metabolic stress in T2D",
        genes: ["TXNIP", "SCD", "CD36", "PLIN2", "DDIT3", "HSPA5", "SOD2", "CPT1A", "CXCL10", "ELOVL6", "ACSL4", "DGAT2", "CERS2"],
        notes: "Combined high glucose (TXNIP induction) and elevated free fatty acid signature (lipid droplet/ceramide/lipogenic and oxidative-stress genes) seen in glucolipotoxic beta-cell models relevant to T2D (Poitout & Robertson 2008 Endocr Rev; Cnop lab lipotoxicity/ceramide studies).",
        activities: {
          identity: -1, insulin: -1, secretion: -1, metabolism: 1,
          "mito-qc": 1, "er-folding": 2, upr: 2, "oxidative-stress": 3,
          autophagy: 1, proteasome: 1, cytokine: 1, dediff: 1,
          apoptosis: 1, "lipid-handling": 3, "fatty-acid-oxidation": 2,
          "lipotoxic-stress": 3
        }
      },
      {
        id: "dedifferentiated",
        name: "Dedifferentiated beta cell",
        phenotype: "Loss of mature beta-cell identity toward an ALDH1A3+ progenitor-like state, described in type 2 diabetes and aging",
        genes: ["ALDH1A3", "SOX9", "NEUROG3", "HES1", "GATA6", "MYCL", "SMOC1", "LDHA", "SLC16A1", "NKX2-2", "PDX1", "FOXO1"],
        notes: "Verified via WebSearch. Loss of mature identity toward a progenitor/multipotent-like and 'disallowed-gene'-expressing state: ALDH1A3/SOX9/NEUROG3/HES1/GATA6/FOXO1(nuclear exclusion) from Talchai et al. 2012 Cell and Cinti et al. 2016 JCEM (human T2D); LDHA/SLC16A1 are classic 'disallowed genes' re-expressed on identity loss (Pullen & Rutter 2013); SMOC1 is a newly identified (2025) alpha-lineage gene ectopically induced in dedifferentiating beta cells.",
        activities: {
          identity: -2, insulin: -2, secretion: -2, granule: -1,
          dediff: 3, development: 2, "cell-cycle": -1, senescence: 0,
          apoptosis: -1, survival: 1
        }
      },
      {
        id: "transdifferentiated",
        name: "Transdifferentiated beta cell",
        phenotype: "Beta-to-alpha lineage conversion with ectopic glucagon expression, an extreme form of beta-cell plasticity reported in longstanding diabetes",
        genes: ["ARX", "MAFB", "GCG", "ALDH1A3", "IRX2", "POU6F2", "FEV", "KCNJ3", "SV2B", "SMOC1"],
        notes: "Verified via WebSearch. Beta-to-alpha lineage conversion signature (ectopic acquisition of full alpha-cell transcriptional program) from human islet studies of longstanding diabetes (Spijker et al. 2015 Diabetes; SMOC1 trajectory-inference paper, Nat Commun 2025).",
        activities: {
          identity: -2, insulin: -2, secretion: -1, dediff: 2,
          development: 2, transdiff: 3, "cell-cycle": -1,
          apoptosis: -1, survival: 1
        }
      },
      {
        id: "proliferating",
        name: "Proliferating beta cell",
        phenotype: "Compensatory beta-cell replication seen in pregnancy, obesity, and early compensatory hyperplasia; identity is largely retained while cycling",
        genes: ["MKI67", "TOP2A", "CCNB1", "INS", "PDX1", "FOXM1", "CCND2", "CCND1", "PLK1", "CENPA", "BIRC5", "PCNA"],
        notes: "Verified via WebSearch. Compensatory replication signature retaining identity genes; FOXM1/CCND2/PLK1/CENPA axis and BIRC5 are established drivers of adaptive human beta-cell proliferation in obesity/pregnancy (Zhong lab FoxM1 studies; Aguayo-Mazzucato/Bonner-Weir compensatory expansion literature).",
        activities: {
          identity: 2, insulin: 2, secretion: 1, metabolism: 1,
          "cell-cycle": 3, "dna-damage": 1, senescence: -2,
          apoptosis: -1, survival: 2
        }
      },
      {
        id: "senescent",
        name: "Senescent beta cell",
        phenotype: "Cell-cycle-arrested, apoptosis-resistant beta cell with a senescence-associated secretory phenotype (SASP), implicated in aging and type 2 diabetes",
        genes: ["CDKN2A", "CDKN1A", "GDF15", "SERPINE1", "CCL2", "TP53", "B2M", "IL1B", "GLB1", "TNFRSF1B"],
        notes: "Verified via WebSearch. p16/CDKN2A (stable arrest) and p21/CDKN1A (early arrest) plus SASP factors (GDF15, SERPINE1/PAI-1, CCL2, IL1B) from Aguayo-Mazzucato et al. 2019 Cell Metab and Thompson et al. 2019 Cell Metab; B2M was used as a cell-surface sorting marker for senescent human beta cells in the same studies; GLB1 encodes SA-beta-galactosidase, the classical senescence enzyme marker.",
        activities: {
          identity: -1, insulin: -1, senescence: 3, "cell-cycle": -2,
          "oxidative-stress": 2, cytokine: 2, apoptosis: -1,
          survival: 1, upr: 1
        }
      }
    ]
  },
  {
    id: "alpha-cell",
    name: "Alpha cell",
    programs: [
      {
        id: "alpha-identity",
        name: "Alpha-cell identity",
        category: "Core identity",
        function: "Mature alpha-cell transcriptional identity",
        genes: ["GCG", "ARX", "MAFB", "IRX2", "IRX1", "TTR"]
      },
      {
        id: "glucagon",
        name: "Glucagon biosynthesis",
        category: "Secretion",
        function: "Production and processing of glucagon",
        genes: ["GCG", "PCSK2", "CPE", "PAM"]
      },
      {
        id: "alpha-secretion",
        name: "Stimulus-secretion coupling",
        category: "Secretion",
        function: "Low-glucose sensing and glucagon release",
        genes: ["KCNK16", "CACNA1A", "SCN9A", "SNAP25", "STX1A", "SYT7"]
      },
      {
        id: "alpha-granule",
        name: "Secretory granule biology",
        category: "Secretion",
        function: "Granule formation, trafficking, and docking",
        genes: ["CHGA", "CHGB", "SCG2", "RAB3A", "VAMP2"]
      },
      {
        id: "alpha-metabolism",
        name: "Oxidative metabolism",
        category: "Metabolism",
        function: "ATP production and glucose oxidation",
        genes: ["IDH3A", "SDHB", "NDUFA", "COX", "ATP5"]
      },
      {
        id: "alpha-er-folding",
        name: "ER protein folding",
        category: "Protein homeostasis",
        function: "Folding of secreted proteins",
        genes: ["HSPA5", "PDIA4", "PDIA6", "CALR", "CANX"]
      },
      {
        id: "alpha-upr",
        name: "Unfolded protein response",
        category: "Protein homeostasis",
        function: "Adaptive ER stress",
        genes: ["XBP1", "ATF6", "EIF2AK3", "DDIT3", "ATF4"]
      },
      {
        id: "alpha-oxidative-stress",
        name: "Oxidative stress response",
        category: "Stress response",
        function: "Detoxification of reactive oxygen species",
        genes: ["TXN", "PRDX1", "GPX1", "SOD2"]
      },
      {
        id: "alpha-interferon",
        name: "Interferon response",
        category: "Immune response",
        function: "Antiviral and inflammatory signaling",
        genes: ["STAT1", "IFIT1", "IFI44L", "MX1", "ISG15"]
      },
      {
        id: "alpha-antigen",
        name: "Antigen presentation",
        category: "Immune response",
        function: "Immune visibility",
        genes: ["B2M", "HLA-A", "HLA-B", "TAP1", "TAP2"]
      },
      {
        id: "alpha-dediff",
        name: "Dedifferentiation / transdifferentiation",
        category: "Cell fate",
        function: "Loss of alpha identity and drift toward a beta-like or progenitor state",
        genes: ["ARX", "PAX4", "MAFB", "SOX9"]
      },
      {
        id: "alpha-apoptosis",
        name: "Apoptosis",
        category: "Cell fate",
        function: "Programmed cell death",
        genes: ["BAX", "BBC3", "PMAIP1", "CASP3"]
      },
      {
        id: "alpha-survival",
        name: "Survival",
        category: "Cell fate",
        function: "Anti-apoptotic programs",
        genes: ["BCL2L1", "MCL1"]
      }
    ],
    states: [
      {
        id: "mature-functional-alpha",
        name: "Mature functional alpha cell",
        phenotype: "Canonical healthy alpha cell",
        genes: ["GCG", "ARX", "MAFB", "TTR", "IRX2", "IRX1", "PAX6", "FEV", "LOXL4", "CRYBA2", "GC", "SLC7A2"],
        notes: "Verified via WebSearch. Canonical alpha-cell identity/marker panel including transcription factors and human-alpha-enriched surface/secreted markers identified in single-cell islet atlases (LOXL4, CRYBA2, GC, SLC7A2 recur across human alpha-cell scRNA-seq studies; SLC7A2 confirmed functionally required for alpha-cell proliferation/secretion, JCI 2024).",
        activities: {
          "alpha-identity": 3, glucagon: 3, "alpha-secretion": 3, "alpha-granule": 2,
          "alpha-metabolism": 2, "alpha-upr": -1, "alpha-interferon": -1, "alpha-apoptosis": -1
        }
      },
      {
        id: "hyperglucagonemic",
        name: "Hyperglucagonemic alpha cell",
        phenotype: "Chronic hyperglycemia-driven overactivity seen in T2D",
        genes: ["GCG", "PCSK2", "CHGA", "SLC7A2", "SLC38A5", "ARX", "MAFB", "TTR", "TXNIP"],
        notes: "Verified via WebSearch; fewer than 10 genes because a distinct human single-cell transcriptomic signature for chronic hyperglucagonemia (as opposed to physiology) is not well established. SLC38A5/SLC7A2 amino-acid transporter induction is documented in the liver-alpha-cell axis literature on glucagon receptor resistance/hyperglucagonemia (Kim et al. 2017 Cell Metab; Dean lab SLC7A2 studies, JCI 2024); remaining genes reflect increased glucagon biosynthetic machinery.",
        activities: {
          "alpha-identity": 2, glucagon: 3, "alpha-secretion": 2, "alpha-granule": 2,
          "alpha-metabolism": 2, "alpha-er-folding": 1, "alpha-upr": 1, "alpha-oxidative-stress": 1
        }
      },
      {
        id: "alpha-dedifferentiated",
        name: "Dedifferentiated alpha cell",
        phenotype: "Loss of alpha identity reported in long-standing T1D and T2D",
        genes: ["PAX4", "SOX9", "NKX6-1", "PDX1", "INS", "MAFA", "GATA6", "HES1"],
        notes: "Verified via WebSearch; fewer than 10 genes as human evidence for alpha-cell dedifferentiation is much thinner than for beta cells. PAX4 gain and reduced ARX with increased NKX6.1 in alpha cells accompanying reduced beta-cell mass was directly shown in human pancreas (Sci Rep 2021, 'Increased NKX6.1... decreased ARX expression in alpha cells'); SOX9/GATA6/HES1 are shared progenitor-reversion markers by analogy to beta-cell dedifferentiation literature.",
        activities: {
          "alpha-identity": -2, glucagon: -2, "alpha-dediff": 3,
          "alpha-oxidative-stress": 1, "alpha-apoptosis": 1
        }
      },
      {
        id: "alpha-inflammatory",
        name: "Inflammatory response alpha cell",
        phenotype: "Cytokine and interferon exposure typical of insulitis in T1D",
        genes: ["STAT1", "IFIT1", "B2M", "IFI44L", "MX1", "ISG15", "HLA-A", "HLA-B", "TAP1", "CXCL10", "IRF1"],
        notes: "Interferon-stimulated gene/MHC-I signature also documented in alpha cells during insulitis, with alpha cells showing even stronger basal and induced immune/HLA responses than beta cells in T1D single-cell studies (Russell et al. 2019 Diabetes).",
        activities: {
          "alpha-identity": -1, "alpha-interferon": 3, "alpha-antigen": 3,
          "alpha-upr": 1, "alpha-oxidative-stress": 1
        }
      }
    ]
  }
];

const seedReferences = [
  {
    citation: "Talchai C, Xuan S, Lin HV, Sussel L, Accili D. Pancreatic β cell dedifferentiation as a mechanism of diabetic β cell failure. Cell. 2012;150(6):1223-1234. PMID: 22980982",
    note: "Foundational beta-cell dedifferentiation model: loss of identity genes, gain of progenitor markers (Neurog3, Sox9, Aldh1a3), FOXO1 nuclear exclusion, and emergence of alpha-cell-like markers underlying the dedifferentiated and transdifferentiated beta-cell states."
  },
  {
    citation: "Cinti F, Bouchi R, Kim-Muller JY, et al. Evidence of β-Cell Dedifferentiation in Human Type 2 Diabetes. J Clin Endocrinol Metab. 2016;101(3):1044-1054. PMID: 26713822",
    note: "Confirms ALDH1A3 as a marker of beta-cell dedifferentiation in human T2D pancreas."
  },
  {
    citation: "Pullen TJ, Rutter GA. When less is more: the forbidden fruits of gene repression in the adult β-cell. Diabetes Obes Metab. 2013;15(6):503-512.",
    note: "Defines 'disallowed genes' (LDHA, SLC16A1/MCT1) whose re-expression marks loss of beta-cell identity, used in the dedifferentiated state."
  },
  {
    citation: "Spijker HS, Song H, Ellenbroek JH, et al. Loss of β-Cell Identity Occurs in Type 2 Diabetes and Is Associated With Islet Amyloid Deposits. Diabetes. 2015;64(8):2928-2938.",
    note: "Human evidence for beta-to-alpha cell transdifferentiation (co-expression of ARX/MAFB/GCG in insulin-lineage cells), supporting the transdifferentiated beta-cell state."
  },
  {
    citation: "Human pancreatic α-cell heterogeneity and trajectory inference analyses reveal SMOC1 as a β-cell dedifferentiation gene. Nat Commun. 2025. PMID: 41057332",
    note: "Identifies SMOC1 as an alpha-lineage gene ectopically induced along the beta-to-alpha dedifferentiation/transdifferentiation trajectory in human T2D islets."
  },
  {
    citation: "Aguayo-Mazzucato C, Andle J, Lee TB Jr, et al. Acceleration of β Cell Aging Determines Diabetes and Senolysis Improves Disease Outcomes. Cell Metab. 2019;30(1):129-142. PMID: 31155496",
    note: "Defines beta-cell senescence markers (CDKN2A/p16, CDKN1A/p21) and use of B2M as a surface marker for FACS isolation of senescent beta cells."
  },
  {
    citation: "Thompson PJ, Shah A, Ntranos V, et al. Targeted Elimination of Senescent Beta Cells Prevents Type 1 Diabetes. Cell Metab. 2019;29(5):1045-1060.",
    note: "Characterizes the beta-cell senescence-associated secretory phenotype (SASP: GDF15, SERPINE1, CCL2, IL1B)."
  },
  {
    citation: "Zhong L, et al. / FoxM1-related studies (e.g., FoxM1 Is Up-Regulated by Obesity and Stimulates β-Cell Proliferation, Mol Endocrinol 2010; Insulin signaling regulates the FoxM1/PLK1/CENP-A pathway, PMC5382039).",
    note: "FOXM1/CCND2/PLK1/CENPA/BIRC5 as drivers of adaptive human beta-cell proliferation in obesity and pregnancy, supporting the proliferating beta-cell state."
  },
  {
    citation: "Xin Y, Gutierrez GD, Okamoto H, et al. and related human islet single-cell studies characterizing alpha-cell-enriched genes LOXL4, CRYBA2, GC, and SLC7A2.",
    note: "Human alpha-cell identity markers used in the mature-functional-alpha panel beyond the canonical GCG/ARX/MAFB set."
  },
  {
    citation: "Dean ED, Li M, Prasad N, et al. Interrupted Glucagon Signaling Reveals Hepatic α Cell Axis and Role for L-Glutamine in α Cell Proliferation. Cell Metab. 2017; and Pancreatic islet α cell function and proliferation require the arginine transporter SLC7A2. JCI 2024.",
    note: "SLC38A5/SLC7A2 amino-acid transporter induction linked to hyperglucagonemia and alpha-cell hyperplasia, used in the hyperglucagonemic alpha-cell state."
  },
  {
    citation: "Increased NKX6.1 expression and decreased ARX expression in alpha cells accompany reduced beta-cell volume in human subjects. Sci Rep. 2021;11:16951.",
    note: "Direct human evidence of alpha-cell reprogramming markers (NKX6-1 gain, ARX loss) used in the alpha-dedifferentiated state."
  },
  {
    citation: "Russell MA, Redick SD, Blodgett DM, et al. HLA Class II Antigen Processing and Presentation Pathway Components Demonstrated by Transcriptomics for Islet α, β, and δ-Cells in Type 1 Diabetes. Diabetes. 2019;68(5):988-1001.",
    note: "Documents interferon-stimulated gene/HLA class I-II induction across alpha, beta, delta (and by extension other) islet endocrine cell types during insulitis, supporting all *-inflammatory states."
  },
  {
    citation: "Marhfour I, Lopez XM, Lefkaditis D, et al. Expression of endoplasmic reticulum stress markers in the islets of patients with type 1 diabetes. Diabetologia. 2012;55(9):2417-2420.",
    note: "Human islet evidence for terminal UPR markers (DDIT3/CHOP, HSPA5, HERPUD1, DNAJB9) used in the er-stressed beta-cell state."
  },
  {
    citation: "Poitout V, Robertson RP. Glucolipotoxicity: fuel excess and beta-cell dysfunction. Endocr Rev. 2008;29(3):351-366.",
    note: "Reviews the combined glucose/lipid toxicity signature (TXNIP, CD36, SCD, ceramide pathway) used in the glucolipotoxicity beta-cell state."
  }
];

let model = loadModel();
let selectedCellTypeId = model.cellTypes[0]?.id || null;
let editorMode = null;
let editingId = null;
let editingReferenceIndex = null;
let selectedStateId = currentCellType()?.states[0]?.id || null;
let viewMode = "list";
let expandedProgramIds = new Set();
let githubToken = safeGetItem(GITHUB_TOKEN_KEY) || null;
let githubFile = null; // { path, sha, name } for whichever repo file was last loaded

const els = {
  cellTypeSelect: document.querySelector("#cellTypeSelect"),
  stateOptions: document.querySelector("#stateOptions"),
  selectedStateName: document.querySelector("#selectedStateName"),
  selectedStatePhenotype: document.querySelector("#selectedStatePhenotype"),
  selectedStateMarkers: document.querySelector("#selectedStateMarkers"),
  programActivityList: document.querySelector("#programActivityList"),
  viewModeList: document.querySelector("#viewModeList"),
  viewModeNetwork: document.querySelector("#viewModeNetwork"),
  networkView: document.querySelector("#networkView"),
  networkSvg: document.querySelector("#networkSvg"),
  expandAllPrograms: document.querySelector("#expandAllPrograms"),
  collapseAllPrograms: document.querySelector("#collapseAllPrograms"),
  editor: document.querySelector("#editor"),
  editorForm: document.querySelector("#editorForm"),
  editorTitle: document.querySelector("#editorTitle"),
  editorFields: document.querySelector("#editorFields"),
  deleteItem: document.querySelector("#deleteItem"),
  exportDialog: document.querySelector("#exportDialog"),
  exportForm: document.querySelector("#exportForm"),
  exportFileName: document.querySelector("#exportFileName"),
  referencesDialog: document.querySelector("#referencesDialog"),
  referencesList: document.querySelector("#referencesList"),
  showGithubFiles: document.querySelector("#showGithubFiles"),
  saveToGithub: document.querySelector("#saveToGithub"),
  githubDialog: document.querySelector("#githubDialog"),
  cancelGithub: document.querySelector("#cancelGithub"),
  githubFileList: document.querySelector("#githubFileList"),
  githubTokenInput: document.querySelector("#githubTokenInput"),
  githubTokenRemember: document.querySelector("#githubTokenRemember"),
  githubTokenSave: document.querySelector("#githubTokenSave"),
  githubTokenStatus: document.querySelector("#githubTokenStatus")
};

document.querySelector("#resetData").addEventListener("click", () => {
  model = { cellTypes: structuredClone(seedCellTypes), references: structuredClone(seedReferences) };
  selectedCellTypeId = model.cellTypes[0]?.id || null;
  selectedStateId = currentCellType()?.states[0]?.id || null;
  expandedProgramIds = new Set();
  saveModel();
  render();
  showToast("Model reset");
});

document.querySelector("#exportData").addEventListener("click", openExportDialog);
document.querySelector("#importData").addEventListener("change", importJson);
document.querySelector("#addProgram").addEventListener("click", () => openProgramEditor());
document.querySelector("#addState").addEventListener("click", () => openStateEditor());
document.querySelector("#editSelectedState").addEventListener("click", () => openStateEditor(selectedStateId));
document.querySelector("#cancelEdit").addEventListener("click", () => els.editor.close());
document.querySelector("#cancelExport").addEventListener("click", () => els.exportDialog.close());
document.querySelector("#showReferences").addEventListener("click", openReferencesDialog);
document.querySelector("#cancelReferences").addEventListener("click", () => els.referencesDialog.close());
els.cellTypeSelect.addEventListener("change", () => {
  selectedCellTypeId = els.cellTypeSelect.value;
  selectedStateId = currentCellType()?.states[0]?.id || null;
  expandedProgramIds = new Set();
  render();
});
els.viewModeList.addEventListener("click", () => {
  viewMode = "list";
  render();
});
els.viewModeNetwork.addEventListener("click", () => {
  viewMode = "network";
  render();
});
els.expandAllPrograms.addEventListener("click", () => {
  filteredPrograms().forEach((program) => expandedProgramIds.add(program.id));
  render();
});
els.collapseAllPrograms.addEventListener("click", () => {
  expandedProgramIds.clear();
  render();
});
els.editorForm.addEventListener("submit", saveEditor);
els.deleteItem.addEventListener("click", deleteEditorItem);
els.exportForm.addEventListener("submit", exportJson);
els.showGithubFiles.addEventListener("click", openGithubDialog);
els.cancelGithub.addEventListener("click", () => els.githubDialog.close());
els.githubTokenSave.addEventListener("click", saveGithubToken);
els.saveToGithub.addEventListener("click", saveModelToGithub);

render();
updateGithubSaveButton();

function currentCellType() {
  return model.cellTypes.find((cellType) => cellType.id === selectedCellTypeId) || model.cellTypes[0] || null;
}

function safeGetItem(key) {
  // localStorage can throw (not just return null) in some configurations --
  // private/incognito browsing, certain file:// setups, storage disabled by
  // policy. Treat that the same as "nothing stored" instead of crashing.
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function loadModel() {
  const stored = safeGetItem(STORAGE_KEY);
  if (stored) {
    try {
      return migrateModel(JSON.parse(stored));
    } catch {
      return { cellTypes: structuredClone(seedCellTypes), references: structuredClone(seedReferences) };
    }
  }

  // Fall back to the older single-cell-type storage format if present, so
  // existing users don't lose their edits when upgrading.
  const legacy = safeGetItem(LEGACY_STORAGE_KEY);
  if (legacy) {
    try {
      return migrateModel(JSON.parse(legacy));
    } catch {
      return { cellTypes: structuredClone(seedCellTypes), references: structuredClone(seedReferences) };
    }
  }

  return { cellTypes: structuredClone(seedCellTypes), references: structuredClone(seedReferences) };
}

function saveModel() {
  // If storage is unavailable, degrade to in-memory-only for this session
  // rather than throwing and breaking every action that edits the model.
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(model));
  } catch {
    /* ignore */
  }
}

function migrateModel(storedModel) {
  // Older exports/saves used a flat {programs, states} shape for a single
  // (beta) cell type. Wrap that into the new cellTypes[] shape.
  const rawCellTypes = Array.isArray(storedModel?.cellTypes)
    ? storedModel.cellTypes
    : (Array.isArray(storedModel?.programs) || Array.isArray(storedModel?.states))
      ? [{
          id: "beta-cell",
          name: "Beta cell",
          programs: Array.isArray(storedModel.programs) ? storedModel.programs : [],
          states: Array.isArray(storedModel.states) ? storedModel.states : []
        }]
      : [];

  const nextCellTypes = rawCellTypes.map((cellType) => ({
    id: cellType.id || slugifyValue(cellType.name || "cell-type", []),
    name: cellType.name || "Cell type",
    programs: Array.isArray(cellType.programs) ? cellType.programs : [],
    states: Array.isArray(cellType.states) ? cellType.states : []
  }));

  // Backfill any seed cell types (and seed programs/states within cell types
  // that already exist) that are missing, so upgrades pick up new defaults
  // without discarding user edits.
  seedCellTypes.forEach((seedCellType) => {
    const existing = nextCellTypes.find((cellType) => cellType.id === seedCellType.id);
    if (!existing) {
      nextCellTypes.push(structuredClone(seedCellType));
      return;
    }

    seedCellType.programs.forEach((seedProgram) => {
      if (!existing.programs.some((program) => program.id === seedProgram.id)) {
        existing.programs.push(structuredClone(seedProgram));
      }
    });

    seedCellType.states.forEach((seedState) => {
      if (!existing.states.some((state) => state.id === seedState.id)) {
        existing.states.push(structuredClone(seedState));
      }
    });
  });

  // Backfill any new seed references (by citation text) into the stored
  // references list, so upgrades pick up newly added literature citations
  // without discarding any the user may have added themselves.
  const existingReferences = Array.isArray(storedModel?.references) ? storedModel.references : [];
  const referenceCitations = new Set(existingReferences.map((ref) => ref.citation));
  const nextReferences = [...existingReferences];
  seedReferences.forEach((ref) => {
    if (!referenceCitations.has(ref.citation)) {
      nextReferences.push(structuredClone(ref));
    }
  });

  if (nextCellTypes.length === 0) {
    return { cellTypes: structuredClone(seedCellTypes), references: nextReferences };
  }

  return { cellTypes: nextCellTypes, references: nextReferences };
}

function render() {
  ensureSelectedCellType();
  ensureSelectedState();
  renderCellTypeOptions();
  renderStateOptions();
  renderSelectedState();
}

function filteredPrograms() {
  const cellType = currentCellType();
  if (!cellType) return [];
  return cellType.programs;
}

function filteredStates() {
  return currentCellType()?.states || [];
}

function ensureSelectedCellType() {
  if (!model.cellTypes.some((cellType) => cellType.id === selectedCellTypeId)) {
    selectedCellTypeId = model.cellTypes[0]?.id || null;
  }
}

function ensureSelectedState() {
  const states = currentCellType()?.states || [];
  if (!states.some((state) => state.id === selectedStateId)) {
    selectedStateId = states[0]?.id || null;
  }
}

function renderCellTypeOptions() {
  els.cellTypeSelect.innerHTML = model.cellTypes.map((cellType) => {
    return `<option value="${cellType.id}" ${cellType.id === selectedCellTypeId ? "selected" : ""}>${escapeHtml(cellType.name)}</option>`;
  }).join("");

  const cellType = currentCellType();
  document.title = cellType ? `${cellType.name} · Cell Model Browser` : "Cell Model Browser";
}

function renderStateOptions() {
  const cellType = currentCellType();
  els.stateOptions.innerHTML = filteredStates().map((state) => {
    const activeCount = (cellType?.programs || []).filter((program) => (state.activities[program.id] ?? 0) !== 0).length;
    return `
      <button class="state-option ${state.id === selectedStateId ? "selected" : ""}" data-state-option="${state.id}">
        <span>${escapeHtml(state.name)}</span>
        <small>${activeCount} active programs</small>
      </button>
    `;
  }).join("");

  els.stateOptions.querySelectorAll("[data-state-option]").forEach((button) => {
    button.addEventListener("click", () => {
      selectedStateId = button.dataset.stateOption;
      render();
    });
  });
}

function renderSelectedState() {
  const cellType = currentCellType();
  const state = (cellType?.states || []).find((item) => item.id === selectedStateId);
  if (!cellType || !state) {
    els.selectedStateName.textContent = "No states yet";
    els.selectedStatePhenotype.textContent = "Add a state to begin.";
    els.selectedStateMarkers.innerHTML = "";
    els.programActivityList.innerHTML = "";
    els.networkView.classList.add("hidden");
    els.programActivityList.classList.remove("hidden");
    els.networkSvg.innerHTML = "";
    return;
  }

  const programs = [...filteredPrograms()].sort((a, b) => {
    const aLevel = state.activities[a.id] ?? 0;
    const bLevel = state.activities[b.id] ?? 0;
    const strength = Math.abs(bLevel) - Math.abs(aLevel);
    if (strength !== 0) return strength;
    if (bLevel !== aLevel) return bLevel - aLevel;
    return a.name.localeCompare(b.name);
  });
  els.selectedStateName.textContent = state.name;
  els.selectedStatePhenotype.textContent = state.phenotype;
  renderStateMarkers(state);

  els.viewModeList.setAttribute("aria-pressed", String(viewMode === "list"));
  els.viewModeNetwork.setAttribute("aria-pressed", String(viewMode === "network"));
  els.programActivityList.classList.toggle("hidden", viewMode !== "list");
  els.networkView.classList.toggle("hidden", viewMode !== "network");

  if (viewMode === "network") {
    renderNetworkView(cellType, state, programs);
    return;
  }

  els.programActivityList.innerHTML = programs.map((program) => {
    const level = state.activities[program.id] ?? 0;
    const width = Math.max(8, Math.abs(level) / 3 * 100);
    const tone = toneForLevel(level);
    return `
      <article class="program-row" data-tone="${tone}">
        <div class="program-main">
          <div class="program-title-line">
            <h3>${escapeHtml(program.name)}</h3>
            <span>${escapeHtml(program.category)}</span>
          </div>
          <p>${escapeHtml(program.function)}</p>
          <div class="tag-list">${program.genes.map((gene) => `<span class="tag">${escapeHtml(gene)}</span>`).join("")}</div>
        </div>
        <div class="program-activity">
          <button class="activity" data-program="${program.id}" data-state="${state.id}" data-level="${level}">
            ${activityLabel(level)}
          </button>
          <div class="bar-track" aria-hidden="true">
            <span class="bar-fill" style="width:${width}%"></span>
          </div>
          <button class="ghost" data-edit-program="${program.id}">Edit program</button>
        </div>
      </article>
    `;
  }).join("");

  els.programActivityList.querySelectorAll(".activity").forEach((button) => {
    button.addEventListener("click", () => cycleActivity(button.dataset.state, button.dataset.program));
  });
  els.programActivityList.querySelectorAll("[data-edit-program]").forEach((button) => {
    button.addEventListener("click", () => openProgramEditor(button.dataset.editProgram));
  });
}

// Shown above the list/network toggle so it's visible regardless of which
// view mode is active -- this is the curated, literature-backed marker gene
// panel for the state as a whole (distinct from each program's own genes).
function renderStateMarkers(state) {
  const genes = Array.isArray(state.genes) ? state.genes : [];
  if (genes.length === 0) {
    els.selectedStateMarkers.innerHTML = "";
    return;
  }
  const stateRefs = referencesForState(state);
  els.selectedStateMarkers.innerHTML = `
    <div class="marker-genes-head">
      <span class="marker-genes-label">Marker genes (${genes.length})</span>
    </div>
    <div class="tag-list marker-tag-list">${genes.map((gene) => `<span class="tag marker-tag">${escapeHtml(gene)}</span>`).join("")}</div>
    ${state.notes ? `<p class="state-notes">${escapeHtml(state.notes)}</p>` : ""}
    ${stateRefs.length ? `
      <div class="state-references">
        <span class="state-references-label">References (${stateRefs.length})</span>
        <ul class="state-references-list">
          ${stateRefs.map((ref) => `
            <li class="state-reference-item">
              <p class="state-reference-citation">${escapeHtml(ref.citation || "")}</p>
              ${ref.note ? `<p class="state-reference-note">${escapeHtml(ref.note)}</p>` : ""}
            </li>
          `).join("")}
        </ul>
      </div>
    ` : ""}
  `;
}

// Best-effort match of a state's supporting literature: extracts the likely
// first-author surname from each reference's citation text (only when it's
// followed by an initials-like token, e.g. "Talchai C," or "Tsuchida T &",
// which reliably distinguishes real author-list citations from title-only
// ones) and checks whether that surname is mentioned in the state's notes.
// Not every reference is written in an author-first format, and not every
// state's notes name a specific paper, so this intentionally under-matches
// rather than guesses -- the full bibliography is always available via the
// References button regardless.
function referenceToken(citation) {
  const cleaned = String(citation || "").trim().replace(/^['"]+/, "");
  const match = cleaned.match(/^([A-Za-zÀ-ÖØ-öø-ÿ'’-]+)\s+([A-Z]{1,3})(?=[,.]|\s+(?:et\b|&|and\b))/);
  return match ? match[1] : null;
}

function referencesForState(state) {
  const notes = (state.notes || "").toLowerCase();
  if (!notes || !Array.isArray(model.references)) return [];
  return model.references.filter((ref) => {
    const token = referenceToken(ref.citation);
    return token && token.length > 3 && notes.includes(token.toLowerCase());
  });
}

function openReferencesDialog() {
  renderReferences();
  els.referencesDialog.showModal();
}

function renderReferences() {
  const refs = Array.isArray(model.references) ? model.references : [];
  els.referencesList.innerHTML = (refs.length === 0
    ? `<p class="no-references">No references recorded for this model.</p>`
    : refs.map((ref, index) => `
      <li class="reference-item">
        <div class="reference-item-body">
          <p class="reference-citation">${escapeHtml(ref.citation || "")}</p>
          ${ref.note ? `<p class="reference-note">${escapeHtml(ref.note)}</p>` : ""}
        </div>
        <button class="ghost" type="button" data-edit-reference="${index}">Edit</button>
      </li>
    `).join("")
  ) + `
    <li class="reference-item reference-item-add">
      <button type="button" id="addReference">Add reference</button>
    </li>
  `;

  els.referencesList.querySelectorAll("[data-edit-reference]").forEach((button) => {
    button.addEventListener("click", () => openReferenceEditor(Number(button.dataset.editReference)));
  });
  const addButton = els.referencesList.querySelector("#addReference");
  if (addButton) addButton.addEventListener("click", () => openReferenceEditor());
}

function toneForLevel(level) {
  if (level < 0) return "down";
  if (level === 0) return "base";
  if (level === 3) return "peak";
  return "up";
}

// Radial graph: the selected state sits at the center, its cell type's
// programs form a ring around it (sized/colored by activity in that state),
// and clicking a program node fans its genes out one ring further. Layout is
// computed with simple trigonometry rather than a physics simulation, since
// program count per state is small enough (a few dozen at most) that a fixed
// radial layout stays readable without needing force-directed placement.
function renderNetworkView(cellType, state, programs) {
  if (!cellType || !state || programs.length === 0) {
    els.networkSvg.innerHTML = "";
    return;
  }

  const width = 900;
  const height = 900;
  const center = { x: width / 2, y: height / 2 };
  const programRingRadius = 300;
  const geneRingOffset = 90;

  const nodes = programs.map((program, index) => {
    const angle = (index / programs.length) * Math.PI * 2 - Math.PI / 2;
    const level = state.activities[program.id] ?? 0;
    return {
      program,
      angle,
      level,
      tone: toneForLevel(level),
      x: center.x + Math.cos(angle) * programRingRadius,
      y: center.y + Math.sin(angle) * programRingRadius
    };
  });

  let edgesMarkup = "";
  let programMarkup = "";
  let geneMarkup = "";

  nodes.forEach((node) => {
    const strokeWidth = 1.5 + Math.abs(node.level) * 1.3;
    const opacity = node.level === 0 ? 0.35 : 0.85;
    edgesMarkup += `<line x1="${center.x}" y1="${center.y}" x2="${node.x}" y2="${node.y}" class="network-edge" data-tone="${node.tone}" stroke-width="${strokeWidth}" opacity="${opacity}"></line>`;

    const r = 14 + Math.abs(node.level) * 3;
    const expanded = expandedProgramIds.has(node.program.id);
    programMarkup += `
      <g class="network-node-group" data-program="${escapeHtml(node.program.id)}">
        <circle cx="${node.x}" cy="${node.y}" r="${r}" class="network-node" data-tone="${node.tone}" data-expanded="${expanded}"></circle>
        <text x="${node.x}" y="${node.y + r + 13}" text-anchor="middle" class="network-label">${escapeHtml(truncateLabel(node.program.name, 24))}</text>
        <title>${escapeHtml(node.program.name)} (${activityLabel(node.level)})\n${escapeHtml(node.program.function)}</title>
      </g>
    `;

    if (expanded && node.program.genes.length) {
      const genes = node.program.genes;
      const spread = Math.min(Math.PI / 2.4, 0.16 * genes.length);
      genes.forEach((gene, geneIndex) => {
        const t = genes.length === 1 ? 0.5 : geneIndex / (genes.length - 1);
        const geneAngle = node.angle - spread / 2 + t * spread;
        const gx = center.x + Math.cos(geneAngle) * (programRingRadius + geneRingOffset);
        const gy = center.y + Math.sin(geneAngle) * (programRingRadius + geneRingOffset);
        edgesMarkup += `<line x1="${node.x}" y1="${node.y}" x2="${gx}" y2="${gy}" class="network-gene-edge"></line>`;
        geneMarkup += `
          <g class="network-gene-group">
            <circle cx="${gx}" cy="${gy}" r="5" class="network-gene-node"></circle>
            <text x="${gx}" y="${gy - 9}" text-anchor="middle" class="network-gene-label">${escapeHtml(gene)}</text>
          </g>
        `;
      });
    }
  });

  els.networkSvg.innerHTML = `
    ${edgesMarkup}
    <g>
      <circle cx="${center.x}" cy="${center.y}" r="46" class="network-state-node"></circle>
      <text x="${center.x}" y="${center.y - 4}" text-anchor="middle" class="network-state-label">${escapeHtml(truncateLabel(state.name, 20))}</text>
      <text x="${center.x}" y="${center.y + 14}" text-anchor="middle" class="network-state-sublabel">${programs.length} programs</text>
    </g>
    ${programMarkup}
    ${geneMarkup}
  `;

  els.networkSvg.querySelectorAll("[data-program]").forEach((group) => {
    group.addEventListener("click", () => {
      const id = group.dataset.program;
      if (expandedProgramIds.has(id)) {
        expandedProgramIds.delete(id);
      } else {
        expandedProgramIds.add(id);
      }
      render();
    });
  });
}

function truncateLabel(value, maxLength) {
  if (value.length <= maxLength) return value;
  return `${value.slice(0, maxLength - 1)}…`;
}

function cycleActivity(stateId, programId) {
  const cellType = currentCellType();
  const state = cellType.states.find((item) => item.id === stateId);
  const current = state.activities[programId] ?? 0;
  const index = ACTIVITY_LEVELS.findIndex((level) => level.value === current);
  const next = ACTIVITY_LEVELS[(index + 1) % ACTIVITY_LEVELS.length].value;
  state.activities[programId] = next;
  saveModel();
  render();
}

function openProgramEditor(id) {
  const cellType = currentCellType();
  if (!cellType) return;
  editorMode = "program";
  editingId = id || null;
  editingReferenceIndex = null;
  const program = id
    ? cellType.programs.find((item) => item.id === id)
    : { name: "", category: "", function: "", genes: [] };

  els.editorTitle.textContent = id ? "Edit gene program" : "Add gene program";
  els.deleteItem.hidden = !id;
  els.editorFields.innerHTML = `
    ${field("Name", "name", program.name)}
    ${field("Category", "category", program.category)}
    ${field("Biological function", "function", program.function, "textarea")}
    ${field("Representative genes", "genes", program.genes.join(", "))}
  `;
  els.editor.showModal();
}

function openStateEditor(id) {
  const cellType = currentCellType();
  if (!cellType) return;
  editorMode = "state";
  editingId = id || null;
  editingReferenceIndex = null;
  const state = id
    ? cellType.states.find((item) => item.id === id)
    : { name: "", phenotype: "", genes: [], activities: {} };

  els.editorTitle.textContent = id ? "Edit cell state" : "Add cell state";
  els.deleteItem.hidden = !id;
  const activityFields = cellType.programs.map((program) => {
    const selected = state.activities[program.id] ?? 0;
    return `
      <div class="activity-editor">
        <span>${escapeHtml(program.name)}</span>
        <select name="activity:${program.id}">
          ${ACTIVITY_LEVELS.map((level) => `
            <option value="${level.value}" ${level.value === selected ? "selected" : ""}>${level.label}</option>
          `).join("")}
        </select>
      </div>
    `;
  }).join("");

  els.editorFields.innerHTML = `
    ${field("Name", "name", state.name)}
    ${field("Phenotype context", "phenotype", state.phenotype, "textarea")}
    ${field("Representative genes", "genes", state.genes.join(", "))}
    <label><span>Program activities</span></label>
    ${activityFields}
  `;
  els.editor.showModal();
}

function openCellTypeEditor(id) {
  editorMode = "cellType";
  editingId = id || null;
  editingReferenceIndex = null;
  const cellType = id ? model.cellTypes.find((item) => item.id === id) : { name: "" };

  els.editorTitle.textContent = id ? "Edit cell type" : "Add cell type";
  // Only allow deleting a cell type if more than one remains, so the app
  // always has at least one cell type to show.
  els.deleteItem.hidden = !id || model.cellTypes.length <= 1;
  els.editorFields.innerHTML = `
    ${field("Name", "name", cellType.name)}
    ${id ? "" : "<p>New cell types start with no programs or states — add those next.</p>"}
  `;
  els.editor.showModal();
}

// Reuses the same generic item-editor dialog as programs/states/cell types.
// `index` is the reference's position in model.references (stable enough
// for a single edit session -- the list isn't reordered while the dialog
// with the item editor is open on top of it).
function openReferenceEditor(index) {
  editorMode = "reference";
  editingId = null;
  editingReferenceIndex = Number.isInteger(index) ? index : null;
  const isEditing = editingReferenceIndex !== null;
  const ref = isEditing ? (model.references || [])[editingReferenceIndex] : { citation: "", note: "" };

  els.editorTitle.textContent = isEditing ? "Edit reference" : "Add reference";
  els.deleteItem.hidden = !isEditing;
  els.editorFields.innerHTML = `
    ${field("Citation", "citation", ref.citation, "textarea")}
    ${field("Note (what it supports)", "note", ref.note, "textarea")}
  `;
  els.editor.showModal();
}

function saveEditor(event) {
  event.preventDefault();
  const form = new FormData(els.editorForm);
  const cellType = currentCellType();

  if (editorMode === "program" && cellType) {
    const next = {
      id: editingId || slugify(form.get("name") || "program", cellType.programs),
      name: clean(form.get("name")),
      category: clean(form.get("category")),
      function: clean(form.get("function")),
      genes: splitGenes(form.get("genes"))
    };
    if (editingId) {
      cellType.programs = cellType.programs.map((program) => program.id === editingId ? next : program);
    } else {
      cellType.programs.push(next);
    }
  }

  if (editorMode === "state" && cellType) {
    const activities = {};
    for (const [key, value] of form.entries()) {
      if (key.startsWith("activity:")) activities[key.slice(9)] = Number(value);
    }
    const next = {
      id: editingId || slugify(form.get("name") || "state", cellType.states),
      name: clean(form.get("name")),
      phenotype: clean(form.get("phenotype")),
      genes: splitGenes(form.get("genes")),
      activities
    };
    if (editingId) {
      cellType.states = cellType.states.map((state) => state.id === editingId ? next : state);
    } else {
      cellType.states.push(next);
      selectedStateId = next.id;
    }
  }

  if (editorMode === "cellType") {
    const name = clean(form.get("name"));
    if (editingId) {
      const existing = model.cellTypes.find((item) => item.id === editingId);
      if (existing) existing.name = name;
    } else {
      const next = {
        id: slugify(name || "cell-type", model.cellTypes),
        name,
        programs: [],
        states: []
      };
      model.cellTypes.push(next);
      selectedCellTypeId = next.id;
      selectedStateId = null;
      expandedProgramIds = new Set();
    }
  }

  if (editorMode === "reference") {
    if (!Array.isArray(model.references)) model.references = [];
    const next = {
      citation: clean(form.get("citation")),
      note: clean(form.get("note"))
    };
    if (editingReferenceIndex !== null) {
      model.references[editingReferenceIndex] = next;
    } else {
      model.references.push(next);
    }
  }

  saveModel();
  els.editor.close();
  render();
  renderReferences();
}

function deleteEditorItem() {
  const cellType = currentCellType();
  if (editorMode === "program" && editingId && cellType) {
    cellType.programs = cellType.programs.filter((program) => program.id !== editingId);
    cellType.states.forEach((state) => delete state.activities[editingId]);
  }
  if (editorMode === "state" && editingId && cellType) {
    cellType.states = cellType.states.filter((state) => state.id !== editingId);
  }
  if (editorMode === "cellType" && editingId && model.cellTypes.length > 1) {
    model.cellTypes = model.cellTypes.filter((item) => item.id !== editingId);
    if (selectedCellTypeId === editingId) {
      selectedCellTypeId = model.cellTypes[0]?.id || null;
      selectedStateId = null;
      expandedProgramIds = new Set();
    }
  }
  if (editorMode === "reference" && editingReferenceIndex !== null && Array.isArray(model.references)) {
    model.references.splice(editingReferenceIndex, 1);
  }
  saveModel();
  els.editor.close();
  render();
  renderReferences();
}

function openExportDialog() {
  els.exportFileName.value = defaultExportFileName();
  els.exportDialog.showModal();
  els.exportFileName.focus();
  els.exportFileName.select();
}

function exportJson(event) {
  event.preventDefault();
  const blob = new Blob([JSON.stringify(model, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = normalizeJsonFileName(els.exportFileName.value);
  anchor.click();
  URL.revokeObjectURL(url);
  els.exportDialog.close();
}

function defaultExportFileName() {
  const date = new Date().toISOString().slice(0, 10);
  return `islet-cell-state-model-${date}.json`;
}

function normalizeJsonFileName(value) {
  const cleanName = clean(value).replace(/[\\/:*?"<>|]+/g, "-") || defaultExportFileName();
  return cleanName.toLowerCase().endsWith(".json") ? cleanName : `${cleanName}.json`;
}

function importJson(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.addEventListener("load", () => {
    try {
      const imported = JSON.parse(reader.result);
      // NOTE: deliberately not running this through migrateModel() — that
      // function also backfills the app's built-in seed cell types (used to
      // upgrade old browser-saved data), which would graft unrelated seed
      // content onto an intentionally self-contained tissue file the user
      // is loading here.
      model = validateImportedModel(imported);
      selectedCellTypeId = model.cellTypes[0]?.id || null;
      selectedStateId = currentCellType()?.states[0]?.id || null;
      expandedProgramIds = new Set();
      saveModel();
      render();
      showToast(`Loaded ${file.name}`);
    } catch (error) {
      showToast(error.message || "Could not load JSON");
    } finally {
      event.target.value = "";
    }
  });
  reader.addEventListener("error", () => {
    showToast("Could not read file");
    event.target.value = "";
  });
  reader.readAsText(file);
}

function validateImportedModel(imported) {
  if (!imported) {
    throw new Error("JSON must be an object");
  }

  // Accept either the current multi-cell-type shape or the older flat
  // {programs, states} shape for a single cell type.
  const cellTypes = Array.isArray(imported.cellTypes)
    ? imported.cellTypes
    : (Array.isArray(imported.programs) && Array.isArray(imported.states))
      ? [{ id: "beta-cell", name: "Beta cell", programs: imported.programs, states: imported.states }]
      : null;

  if (!cellTypes) {
    throw new Error("JSON must include a cellTypes array (or programs/states arrays)");
  }

  cellTypes.forEach((cellType) => {
    if (!cellType.name || !Array.isArray(cellType.programs) || !Array.isArray(cellType.states)) {
      throw new Error("Each cell type needs a name, programs array, and states array");
    }

    cellType.programs.forEach((program) => {
      if (!program.id || !program.name || !Array.isArray(program.genes)) {
        throw new Error("Each program needs id, name, and genes");
      }
    });

    cellType.states.forEach((state) => {
      if (!state.id || !state.name || !state.activities || typeof state.activities !== "object") {
        throw new Error("Each state needs id, name, and activities");
      }
      if (!Array.isArray(state.genes)) state.genes = [];
    });
  });

  const references = Array.isArray(imported.references) ? imported.references : [];

  return { cellTypes, references };
}

// --- GitHub integration -----------------------------------------------
// This app is hosted straight from the GitHub repo it lives in (via GitHub
// Pages), so "load from repo" and "save back to repo" both go through the
// GitHub Contents API directly from the browser. Reading the file list and
// file contents works unauthenticated for a public repo; writing requires a
// personal access token with write access, which the user pastes in here.
// The token is kept only in memory unless the user opts in to remembering
// it (in which case it's stored in this browser's localStorage) -- it is
// never sent anywhere except the GitHub API.

function openGithubDialog() {
  updateGithubTokenStatus();
  els.githubTokenInput.value = "";
  els.githubTokenRemember.checked = false;
  els.githubFileList.innerHTML = `<li class="github-file-loading">Loading files from GitHub…</li>`;
  els.githubDialog.showModal();
  loadGithubFileList();
}

function updateGithubTokenStatus() {
  els.githubTokenStatus.textContent = githubToken
    ? "Token set for this browser session"
    : "No token set yet — you can still load files";
}

function saveGithubToken() {
  const value = els.githubTokenInput.value.trim();
  if (!value) {
    showToast("Enter a token first");
    return;
  }
  githubToken = value;
  if (els.githubTokenRemember.checked) {
    try {
      localStorage.setItem(GITHUB_TOKEN_KEY, value);
    } catch {
      /* ignore */
    }
  }
  els.githubTokenInput.value = "";
  updateGithubTokenStatus();
  showToast("GitHub token saved for this session");
}

async function loadGithubFileList() {
  try {
    const response = await fetch(
      `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/?ref=${GITHUB_BRANCH}`,
      { headers: { Accept: "application/vnd.github+json" } }
    );
    if (!response.ok) throw new Error(`GitHub API error (${response.status})`);
    const items = await response.json();
    const jsonFiles = items.filter((item) => item.type === "file" && item.name.toLowerCase().endsWith(".json"));

    if (jsonFiles.length === 0) {
      els.githubFileList.innerHTML = `<li class="github-file-empty">No JSON files found in the repo root.</li>`;
      return;
    }

    els.githubFileList.innerHTML = jsonFiles.map((file) => `
      <li class="github-file-item">
        <span>${escapeHtml(file.name)}</span>
        <button class="ghost" type="button" data-load-github="${escapeHtml(file.path)}" data-sha="${escapeHtml(file.sha)}" data-download="${escapeHtml(file.download_url)}" data-name="${escapeHtml(file.name)}">Load</button>
      </li>
    `).join("");

    els.githubFileList.querySelectorAll("[data-load-github]").forEach((button) => {
      button.addEventListener("click", () => {
        loadGithubFile(button.dataset.loadGithub, button.dataset.sha, button.dataset.download, button.dataset.name);
      });
    });
  } catch (error) {
    els.githubFileList.innerHTML = `<li class="github-file-empty">Could not list repo files: ${escapeHtml(error.message)}</li>`;
  }
}

async function loadGithubFile(path, sha, downloadUrl, name) {
  try {
    const response = await fetch(downloadUrl);
    if (!response.ok) throw new Error(`Could not fetch ${path} (${response.status})`);
    const text = await response.text();
    const imported = JSON.parse(text);
    // Same reasoning as importJson(): a repo file is self-contained, so it
    // shouldn't get the app's built-in seed content grafted onto it.
    model = validateImportedModel(imported);
    githubFile = { path, sha, name };
    selectedCellTypeId = model.cellTypes[0]?.id || null;
    selectedStateId = currentCellType()?.states[0]?.id || null;
    expandedProgramIds = new Set();
    saveModel();
    render();
    updateGithubSaveButton();
    els.githubDialog.close();
    showToast(`Loaded ${name} from GitHub`);
  } catch (error) {
    showToast(error.message || "Could not load file from GitHub");
  }
}

function updateGithubSaveButton() {
  els.saveToGithub.hidden = !githubFile;
  els.saveToGithub.textContent = githubFile ? `Save to GitHub (${githubFile.name})` : "Save to GitHub";
}

async function saveModelToGithub() {
  if (!githubFile) {
    showToast("Load a file from GitHub first");
    return;
  }
  if (!githubToken) {
    showToast("Set a GitHub token first");
    openGithubDialog();
    return;
  }
  const proceed = confirm(`Save changes to ${githubFile.path} on the ${GITHUB_BRANCH} branch of ${GITHUB_OWNER}/${GITHUB_REPO}?`);
  if (!proceed) return;

  try {
    const response = await fetch(
      `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${githubFile.path}`,
      {
        method: "PUT",
        headers: {
          Authorization: `token ${githubToken}`,
          Accept: "application/vnd.github+json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: `Update ${githubFile.path} via Cell Model Browser`,
          content: utf8ToBase64(JSON.stringify(model, null, 2)),
          sha: githubFile.sha,
          branch: GITHUB_BRANCH
        })
      }
    );
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      throw new Error(payload?.message || `GitHub save failed (${response.status})`);
    }
    githubFile.sha = payload?.content?.sha || githubFile.sha;
    showToast(`Saved to GitHub: ${githubFile.path}`);
  } catch (error) {
    showToast(error.message || "Could not save to GitHub");
  }
}

function utf8ToBase64(str) {
  return btoa(unescape(encodeURIComponent(str)));
}

function field(label, name, value, type = "input") {
  const escaped = escapeHtml(value || "");
  const input = type === "textarea"
    ? `<textarea name="${name}">${escaped}</textarea>`
    : `<input name="${name}" value="${escaped}">`;
  return `<label><span>${label}</span>${input}</label>`;
}

function splitGenes(value) {
  return clean(value)
    .split(",")
    .map((gene) => gene.trim())
    .filter(Boolean);
}

function clean(value) {
  return String(value || "").trim();
}

// Generic slugifier: `items` is the collection the new id must be unique
// within (a cell type's programs, its states, or the top-level cellTypes).
function slugify(value, items) {
  return slugifyValue(value, items.map((item) => item.id));
}

function slugifyValue(value, existingIds) {
  const base = clean(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
  let id = base || "item";
  const allIds = new Set(existingIds);
  let suffix = 2;
  while (allIds.has(id)) {
    id = `${base}-${suffix}`;
    suffix += 1;
  }
  return id;
}

function activityLabel(value) {
  return ACTIVITY_LEVELS.find((level) => level.value === Number(value))?.label || "baseline";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.append(toast);
  setTimeout(() => toast.remove(), 1800);
}
