#!/usr/bin/env python3
"""Desktop editor for pancreatic islet cell-state program models.

The model covers a tissue (the pancreatic islet) made up of multiple cell
types (beta cell, alpha cell, ...), each with its own distinct set of gene
programs and cell states. The UI lets you pick a cell type and then inspect
or edit that cell type's states/programs independently of the others.
"""

import copy
import json
import logging
import os
import sys
import tkinter as tk
from tkinter import filedialog, font as tkfont, messagebox, simpledialog, ttk

UI_FONT_FAMILY = "Avenir"
UI_FONT_SIZE = 11


LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cell_state_app.log")
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


ACTIVITY_LEVELS = [
    (-2, "down"),
    (-1, "low"),
    (0, "baseline"),
    (1, "up"),
    (2, "high"),
    (3, "very high"),
]

ACTIVITY_LABELS = dict(ACTIVITY_LEVELS)
ACTIVITY_VALUES = {label: value for value, label in ACTIVITY_LEVELS}

SEED_REFERENCES = [
    {
        "citation": "Talchai C, Xuan S, Lin HV, Sussel L, Accili D. Pancreatic β cell dedifferentiation as a mechanism of diabetic β cell failure. Cell. 2012;150(6):1223-1234. PMID: 22980982",
        "note": "Foundational beta-cell dedifferentiation model: loss of identity genes, gain of progenitor markers (Neurog3, Sox9, Aldh1a3), FOXO1 nuclear exclusion, and emergence of alpha-cell-like markers underlying the dedifferentiated and transdifferentiated beta-cell states.",
    },
    {
        "citation": "Cinti F, Bouchi R, Kim-Muller JY, et al. Evidence of β-Cell Dedifferentiation in Human Type 2 Diabetes. J Clin Endocrinol Metab. 2016;101(3):1044-1054. PMID: 26713822",
        "note": "Confirms ALDH1A3 as a marker of beta-cell dedifferentiation in human T2D pancreas.",
    },
    {
        "citation": "Pullen TJ, Rutter GA. When less is more: the forbidden fruits of gene repression in the adult β-cell. Diabetes Obes Metab. 2013;15(6):503-512.",
        "note": "Defines 'disallowed genes' (LDHA, SLC16A1/MCT1) whose re-expression marks loss of beta-cell identity, used in the dedifferentiated state.",
    },
    {
        "citation": "Spijker HS, Song H, Ellenbroek JH, et al. Loss of β-Cell Identity Occurs in Type 2 Diabetes and Is Associated With Islet Amyloid Deposits. Diabetes. 2015;64(8):2928-2938.",
        "note": "Human evidence for beta-to-alpha cell transdifferentiation (co-expression of ARX/MAFB/GCG in insulin-lineage cells), supporting the transdifferentiated beta-cell state.",
    },
    {
        "citation": "Human pancreatic α-cell heterogeneity and trajectory inference analyses reveal SMOC1 as a β-cell dedifferentiation gene. Nat Commun. 2025. PMID: 41057332",
        "note": "Identifies SMOC1 as an alpha-lineage gene ectopically induced along the beta-to-alpha dedifferentiation/transdifferentiation trajectory in human T2D islets.",
    },
    {
        "citation": "Aguayo-Mazzucato C, Andle J, Lee TB Jr, et al. Acceleration of β Cell Aging Determines Diabetes and Senolysis Improves Disease Outcomes. Cell Metab. 2019;30(1):129-142. PMID: 31155496",
        "note": "Defines beta-cell senescence markers (CDKN2A/p16, CDKN1A/p21) and use of B2M as a surface marker for FACS isolation of senescent beta cells.",
    },
    {
        "citation": "Thompson PJ, Shah A, Ntranos V, et al. Targeted Elimination of Senescent Beta Cells Prevents Type 1 Diabetes. Cell Metab. 2019;29(5):1045-1060.",
        "note": "Characterizes the beta-cell senescence-associated secretory phenotype (SASP: GDF15, SERPINE1, CCL2, IL1B).",
    },
    {
        "citation": "Zhong L, et al. / FoxM1-related studies (e.g., FoxM1 Is Up-Regulated by Obesity and Stimulates β-Cell Proliferation, Mol Endocrinol 2010; Insulin signaling regulates the FoxM1/PLK1/CENP-A pathway, PMC5382039).",
        "note": "FOXM1/CCND2/PLK1/CENPA/BIRC5 as drivers of adaptive human beta-cell proliferation in obesity and pregnancy, supporting the proliferating beta-cell state.",
    },
    {
        "citation": "Xin Y, Gutierrez GD, Okamoto H, et al. and related human islet single-cell studies characterizing alpha-cell-enriched genes LOXL4, CRYBA2, GC, and SLC7A2.",
        "note": "Human alpha-cell identity markers used in the mature-functional-alpha panel beyond the canonical GCG/ARX/MAFB set.",
    },
    {
        "citation": "Dean ED, Li M, Prasad N, et al. Interrupted Glucagon Signaling Reveals Hepatic α Cell Axis and Role for L-Glutamine in α Cell Proliferation. Cell Metab. 2017; and Pancreatic islet α cell function and proliferation require the arginine transporter SLC7A2. JCI 2024.",
        "note": "SLC38A5/SLC7A2 amino-acid transporter induction linked to hyperglucagonemia and alpha-cell hyperplasia, used in the hyperglucagonemic alpha-cell state.",
    },
    {
        "citation": "Increased NKX6.1 expression and decreased ARX expression in alpha cells accompany reduced beta-cell volume in human subjects. Sci Rep. 2021;11:16951.",
        "note": "Direct human evidence of alpha-cell reprogramming markers (NKX6-1 gain, ARX loss) used in the alpha-dedifferentiated state.",
    },
    {
        "citation": "Russell MA, Redick SD, Blodgett DM, et al. HLA Class II Antigen Processing and Presentation Pathway Components Demonstrated by Transcriptomics for Islet α, β, and δ-Cells in Type 1 Diabetes. Diabetes. 2019;68(5):988-1001.",
        "note": "Documents interferon-stimulated gene/HLA class I-II induction across alpha, beta, delta (and by extension other) islet endocrine cell types during insulitis, supporting all *-inflammatory states.",
    },
    {
        "citation": "Marhfour I, Lopez XM, Lefkaditis D, et al. Expression of endoplasmic reticulum stress markers in the islets of patients with type 1 diabetes. Diabetologia. 2012;55(9):2417-2420.",
        "note": "Human islet evidence for terminal UPR markers (DDIT3/CHOP, HSPA5, HERPUD1, DNAJB9) used in the er-stressed beta-cell state.",
    },
    {
        "citation": "Poitout V, Robertson RP. Glucolipotoxicity: fuel excess and beta-cell dysfunction. Endocr Rev. 2008;29(3):351-366.",
        "note": "Reviews the combined glucose/lipid toxicity signature (TXNIP, CD36, SCD, ceramide pathway) used in the glucolipotoxicity beta-cell state.",
    },
]

DEFAULT_MODEL = {
    "cellTypes": [
        {
            "id": "beta-cell",
            "name": "Beta cell",
            "programs": [
                {
                    "id": "identity",
                    "name": "Beta-cell identity",
                    "category": "Core identity",
                    "function": "Mature beta-cell transcriptional identity",
                    "genes": ["INS", "IAPP", "PDX1", "NKX6-1", "MAFA", "UCN3", "PCSK1", "SLC30A8"],
                },
                {
                    "id": "insulin",
                    "name": "Insulin biosynthesis",
                    "category": "Secretion",
                    "function": "Production and processing of insulin",
                    "genes": ["INS", "PCSK1", "PCSK2", "CPE", "PAM", "IAPP"],
                },
                {
                    "id": "secretion",
                    "name": "Stimulus-secretion coupling",
                    "category": "Secretion",
                    "function": "Glucose sensing and insulin release",
                    "genes": ["GCK", "KCNJ11", "ABCC8", "CACNA1A", "CACNA1D", "SNAP25", "STX1A", "SYT7"],
                },
                {
                    "id": "granule",
                    "name": "Secretory granule biology",
                    "category": "Secretion",
                    "function": "Granule formation, trafficking, and docking",
                    "genes": ["CHGA", "CHGB", "SCG2", "SCGN", "VAMP2", "RAB3A", "RPH3AL"],
                },
                {
                    "id": "metabolism",
                    "name": "Oxidative metabolism",
                    "category": "Metabolism",
                    "function": "ATP production and glucose oxidation",
                    "genes": ["IDH3A", "SDHB", "NDUFA", "COX", "ATP5"],
                },
                {
                    "id": "mito-qc",
                    "name": "Mitochondrial quality control",
                    "category": "Metabolism",
                    "function": "Mitochondrial maintenance",
                    "genes": ["PINK1", "PRKN", "OPA1", "MFN2", "BNIP3"],
                },
                {
                    "id": "er-folding",
                    "name": "ER protein folding",
                    "category": "Protein homeostasis",
                    "function": "Folding of secreted proteins",
                    "genes": ["HSPA5", "PDIA4", "PDIA6", "CALR", "CANX"],
                },
                {
                    "id": "upr",
                    "name": "Unfolded protein response",
                    "category": "Protein homeostasis",
                    "function": "Adaptive ER stress",
                    "genes": ["XBP1", "ATF6", "EIF2AK3", "DDIT3", "HERPUD1", "DNAJB9", "ATF4"],
                },
                {
                    "id": "oxidative-stress",
                    "name": "Oxidative stress response",
                    "category": "Stress response",
                    "function": "Detoxification of reactive oxygen species",
                    "genes": ["TXN", "TXNIP", "PRDX1", "PRDX4", "GPX1", "SOD2"],
                },
                {
                    "id": "autophagy",
                    "name": "Autophagy / lysosome",
                    "category": "Protein homeostasis",
                    "function": "Recycling damaged proteins and organelles",
                    "genes": ["SQSTM1", "MAP1LC3B", "ATG", "CTSB", "CTSD"],
                },
                {
                    "id": "proteasome",
                    "name": "Proteasome",
                    "category": "Protein homeostasis",
                    "function": "Protein degradation",
                    "genes": ["PSMA", "PSMB", "PSMC"],
                },
                {
                    "id": "cell-cycle",
                    "name": "Cell cycle",
                    "category": "Cell fate",
                    "function": "Cell proliferation",
                    "genes": ["MKI67", "TOP2A", "CCNB1", "CDK1"],
                },
                {
                    "id": "dna-damage",
                    "name": "DNA damage",
                    "category": "Cell fate",
                    "function": "DNA repair and damage response",
                    "genes": ["GADD45A", "CDKN1A", "ATM", "BRCA1"],
                },
                {
                    "id": "hypoxia",
                    "name": "Hypoxia",
                    "category": "Stress response",
                    "function": "Oxygen response",
                    "genes": ["VEGFA", "EGLN3", "HIF1A targets"],
                },
                {
                    "id": "interferon",
                    "name": "Interferon response",
                    "category": "Immune response",
                    "function": "Antiviral and inflammatory signaling",
                    "genes": ["STAT1", "IFIT1", "IFIT3", "IFI44L", "MX1", "ISG15"],
                },
                {
                    "id": "antigen",
                    "name": "Antigen presentation",
                    "category": "Immune response",
                    "function": "Immune visibility",
                    "genes": ["B2M", "HLA-A", "HLA-B", "HLA-C", "TAP1", "TAP2"],
                },
                {
                    "id": "cytokine",
                    "name": "Cytokine signaling",
                    "category": "Immune response",
                    "function": "TNF, IL1, and JAK-STAT signaling",
                    "genes": ["SOCS1", "NFKBIA", "CCL2", "CXCL10"],
                },
                {
                    "id": "dediff",
                    "name": "Dedifferentiation",
                    "category": "Cell fate",
                    "function": "Loss of mature identity",
                    "genes": ["ALDH1A3", "SOX9", "NEUROG3", "FOSL1"],
                },
                {
                    "id": "development",
                    "name": "Developmental plasticity",
                    "category": "Cell fate",
                    "function": "Progenitor-like programs",
                    "genes": ["PAX4", "NKX2-2", "ISL1", "HES1"],
                },
                {
                    "id": "transdiff",
                    "name": "Beta-to-alpha transdifferentiation",
                    "category": "Cell fate",
                    "function": "Ectopic activation of alpha-cell lineage genes with loss of beta-cell identity",
                    "genes": ["ARX", "MAFB", "GCG", "IRX2"],
                },
                {
                    "id": "senescence",
                    "name": "Senescence",
                    "category": "Cell fate",
                    "function": "Stable stress and cell-cycle arrest",
                    "genes": ["CDKN2A", "CDKN1A", "GDF15", "SERPINE1"],
                },
                {
                    "id": "apoptosis",
                    "name": "Apoptosis",
                    "category": "Cell fate",
                    "function": "Programmed cell death",
                    "genes": ["BAX", "BBC3", "PMAIP1", "CASP3"],
                },
                {
                    "id": "survival",
                    "name": "Survival",
                    "category": "Cell fate",
                    "function": "Anti-apoptotic programs",
                    "genes": ["BCL2L1", "MCL1", "MANF"],
                },
                {
                    "id": "zinc",
                    "name": "Zinc homeostasis",
                    "category": "Structural maintenance",
                    "function": "Insulin crystallization",
                    "genes": ["SLC30A8", "MT1X", "MT2A"],
                },
                {
                    "id": "calcium",
                    "name": "Calcium homeostasis",
                    "category": "Structural maintenance",
                    "function": "Calcium handling",
                    "genes": ["ATP2A2", "RYR2", "ITPR3", "CALM"],
                },
                {
                    "id": "cytoskeleton",
                    "name": "Cytoskeleton",
                    "category": "Structural maintenance",
                    "function": "Vesicle movement",
                    "genes": ["ACTB", "TUBA1B", "MYH9"],
                },
                {
                    "id": "ecm",
                    "name": "ECM interaction",
                    "category": "Structural maintenance",
                    "function": "Adhesion and matrix sensing",
                    "genes": ["ITGA6", "ITGB1", "LAMB1", "COL4A1"],
                },
                {
                    "id": "lipid-handling",
                    "name": "Lipid uptake and handling",
                    "category": "Metabolism",
                    "function": "Fatty acid uptake, intracellular lipid trafficking, and lipid droplet buffering",
                    "genes": ["CD36", "FABP3", "FABP5", "PLIN2", "DGAT1", "DGAT2"],
                },
                {
                    "id": "fatty-acid-oxidation",
                    "name": "Fatty acid oxidation",
                    "category": "Metabolism",
                    "function": "Mitochondrial beta-oxidation and lipid-derived energy metabolism",
                    "genes": ["CPT1A", "CPT2", "ACADVL", "ACADM", "HADHA", "PPARA"],
                },
                {
                    "id": "lipotoxic-stress",
                    "name": "Lipotoxic stress",
                    "category": "Stress response",
                    "function": "Cellular stress from excess saturated fatty acids and toxic lipid intermediates",
                    "genes": ["SCD", "ELOVL6", "ACSL4", "CERS2", "CERS6", "DDIT3"],
                },
            ],
            "states": [
                {
                    "id": "mature-functional",
                    "name": "Mature functional beta cell",
                    "phenotype": "Canonical healthy beta cell",
                    "genes": ["INS", "IAPP", "PDX1", "NKX6-1", "MAFA", "UCN3", "PCSK1", "SLC30A8", "GCK", "CHGA", "ABCC8", "KCNJ11"],
                    "notes": "Canonical mature beta-cell identity/function panel (transcription factors, hormone, prohormone convertase, glucose sensing, KATP channel); textbook/consensus markers used across human islet single-cell atlases (e.g., Segerstolpe et al. 2016 Cell Metab).",
                    "activities": {
                        "identity": 3,
                        "insulin": 3,
                        "secretion": 3,
                        "granule": 2,
                        "metabolism": 2,
                        "er-folding": 0,
                        "proteasome": 1,
                        "upr": -1,
                        "interferon": -1,
                        "cell-cycle": -1,
                        "senescence": -1,
                        "apoptosis": -1,
                    },
                },
                {
                    "id": "secretory-adapted",
                    "name": "Secretory-adapted beta cell",
                    "phenotype": "Prolonged insulin demand; compensation, obesity, or pregnancy",
                    "genes": ["INS", "IAPP", "HSPA5", "XBP1", "PDIA6", "CHGA", "SCGN", "CPE", "PCSK1", "PCSK2", "PAM", "VAMP2", "CALR"],
                    "notes": "Reflects physiological (adaptive, non-terminal) UPR activation and increased prohormone-processing/secretory-granule capacity that accompanies compensatory insulin demand in pregnancy/obesity, distinct from the maladaptive terminal UPR of the er-stressed state (Lipson et al. 2006; Scheuner & Kaufman 2008 Endocr Rev).",
                    "activities": {
                        "identity": 2,
                        "insulin": 3,
                        "secretion": 2,
                        "granule": 2,
                        "er-folding": 2,
                        "upr": 1,
                        "metabolism": 2,
                        "autophagy": 1,
                        "oxidative-stress": 1,
                        "apoptosis": -1,
                    },
                },
                {
                    "id": "er-stressed",
                    "name": "ER-stressed beta cell",
                    "phenotype": "Common across T2D, CFRD, and cytokine exposure",
                    "genes": ["DDIT3", "HSPA5", "HERPUD1", "DNAJB9", "PDIA4", "ATF4", "XBP1", "ATF6", "EIF2AK3", "TRIB3", "ATF3", "PPP1R15A", "CALR"],
                    "notes": "Terminal/maladaptive UPR signature (PERK-ATF4-CHOP and IRE1-XBP1 arms) documented in T1D/T2D/CFRD islets and cytokine-exposed beta cells (Marhfour et al. 2012 Diabetologia; Eizirik & Cnop reviews).",
                    "activities": {
                        "identity": -2,
                        "insulin": -2,
                        "er-folding": 2,
                        "upr": 3,
                        "oxidative-stress": 2,
                        "proteasome": 1,
                        "autophagy": 1,
                        "apoptosis": 1,
                    },
                },
                {
                    "id": "interferon-activated",
                    "name": "Inflammatory response beta cell",
                    "phenotype": "Typical of early T1D or cytokine-driven inflammatory exposure",
                    "genes": ["STAT1", "IFIT1", "IFI44L", "MX1", "ISG15", "HLA-A", "B2M", "CXCL10", "HLA-B", "TAP1", "IRF1", "OAS1", "PSMB9"],
                    "notes": "Type I/II interferon-stimulated gene and MHC-I hyperexpression signature described in early/insulitic T1D beta cells (Russell et al. 2019 Diabetes; Marroqui et al. 2017 studies of cytokine-exposed islets).",
                    "activities": {
                        "identity": -1,
                        "interferon": 3,
                        "antigen": 3,
                        "cytokine": 2,
                        "upr": 1,
                        "oxidative-stress": 1,
                    },
                },
                {
                    "id": "glucolipotoxicity",
                    "name": "Glucolipotoxicity beta cell",
                    "phenotype": "Combined high glucose and elevated lipid exposure, often associated with metabolic stress in T2D",
                    "genes": ["TXNIP", "SCD", "CD36", "PLIN2", "DDIT3", "HSPA5", "SOD2", "CPT1A", "CXCL10", "ELOVL6", "ACSL4", "DGAT2", "CERS2"],
                    "notes": "Combined high glucose (TXNIP induction) and elevated free fatty acid signature (lipid droplet/ceramide/lipogenic and oxidative-stress genes) seen in glucolipotoxic beta-cell models relevant to T2D (Poitout & Robertson 2008 Endocr Rev; Cnop lab lipotoxicity/ceramide studies).",
                    "activities": {
                        "identity": -1,
                        "insulin": -1,
                        "secretion": -1,
                        "metabolism": 1,
                        "mito-qc": 1,
                        "er-folding": 2,
                        "upr": 2,
                        "oxidative-stress": 3,
                        "autophagy": 1,
                        "proteasome": 1,
                        "cytokine": 1,
                        "dediff": 1,
                        "apoptosis": 1,
                        "lipid-handling": 3,
                        "fatty-acid-oxidation": 2,
                        "lipotoxic-stress": 3,
                    },
                },
                {
                    "id": "dedifferentiated",
                    "name": "Dedifferentiated beta cell",
                    "phenotype": "Loss of mature beta-cell identity toward an ALDH1A3+ progenitor-like state, described in type 2 diabetes and aging",
                    "genes": ["ALDH1A3", "SOX9", "NEUROG3", "HES1", "GATA6", "MYCL", "SMOC1", "LDHA", "SLC16A1", "NKX2-2", "PDX1", "FOXO1"],
                    "notes": "Verified via WebSearch. Loss of mature identity toward a progenitor/multipotent-like and 'disallowed-gene'-expressing state: ALDH1A3/SOX9/NEUROG3/HES1/GATA6/FOXO1(nuclear exclusion) from Talchai et al. 2012 Cell and Cinti et al. 2016 JCEM (human T2D); LDHA/SLC16A1 are classic 'disallowed genes' re-expressed on identity loss (Pullen & Rutter 2013); SMOC1 is a newly identified (2025) alpha-lineage gene ectopically induced in dedifferentiating beta cells.",
                    "activities": {
                        "identity": -2,
                        "insulin": -2,
                        "secretion": -2,
                        "granule": -1,
                        "dediff": 3,
                        "development": 2,
                        "cell-cycle": -1,
                        "senescence": 0,
                        "apoptosis": -1,
                        "survival": 1,
                    },
                },
                {
                    "id": "transdifferentiated",
                    "name": "Transdifferentiated beta cell",
                    "phenotype": "Beta-to-alpha lineage conversion with ectopic glucagon expression, an extreme form of beta-cell plasticity reported in longstanding diabetes",
                    "genes": ["ARX", "MAFB", "GCG", "ALDH1A3", "IRX2", "POU6F2", "FEV", "KCNJ3", "SV2B", "SMOC1"],
                    "notes": "Verified via WebSearch. Beta-to-alpha lineage conversion signature (ectopic acquisition of full alpha-cell transcriptional program) from human islet studies of longstanding diabetes (Spijker et al. 2015 Diabetes; SMOC1 trajectory-inference paper, Nat Commun 2025).",
                    "activities": {
                        "identity": -2,
                        "insulin": -2,
                        "secretion": -1,
                        "dediff": 2,
                        "development": 2,
                        "transdiff": 3,
                        "cell-cycle": -1,
                        "apoptosis": -1,
                        "survival": 1,
                    },
                },
                {
                    "id": "proliferating",
                    "name": "Proliferating beta cell",
                    "phenotype": "Compensatory beta-cell replication seen in pregnancy, obesity, and early compensatory hyperplasia; identity is largely retained while cycling",
                    "genes": ["MKI67", "TOP2A", "CCNB1", "INS", "PDX1", "FOXM1", "CCND2", "CCND1", "PLK1", "CENPA", "BIRC5", "PCNA"],
                    "notes": "Verified via WebSearch. Compensatory replication signature retaining identity genes; FOXM1/CCND2/PLK1/CENPA axis and BIRC5 are established drivers of adaptive human beta-cell proliferation in obesity/pregnancy (Zhong lab FoxM1 studies; Aguayo-Mazzucato/Bonner-Weir compensatory expansion literature).",
                    "activities": {
                        "identity": 2,
                        "insulin": 2,
                        "secretion": 1,
                        "metabolism": 1,
                        "cell-cycle": 3,
                        "dna-damage": 1,
                        "senescence": -2,
                        "apoptosis": -1,
                        "survival": 2,
                    },
                },
                {
                    "id": "senescent",
                    "name": "Senescent beta cell",
                    "phenotype": "Cell-cycle-arrested, apoptosis-resistant beta cell with a senescence-associated secretory phenotype (SASP), implicated in aging and type 2 diabetes",
                    "genes": ["CDKN2A", "CDKN1A", "GDF15", "SERPINE1", "CCL2", "TP53", "B2M", "IL1B", "GLB1", "TNFRSF1B"],
                    "notes": "Verified via WebSearch. p16/CDKN2A (stable arrest) and p21/CDKN1A (early arrest) plus SASP factors (GDF15, SERPINE1/PAI-1, CCL2, IL1B) from Aguayo-Mazzucato et al. 2019 Cell Metab and Thompson et al. 2019 Cell Metab; B2M was used as a cell-surface sorting marker for senescent human beta cells in the same studies; GLB1 encodes SA-beta-galactosidase, the classical senescence enzyme marker.",
                    "activities": {
                        "identity": -1,
                        "insulin": -1,
                        "senescence": 3,
                        "cell-cycle": -2,
                        "oxidative-stress": 2,
                        "cytokine": 2,
                        "apoptosis": -1,
                        "survival": 1,
                        "upr": 1,
                    },
                },
            ],
        },
        {
            "id": "alpha-cell",
            "name": "Alpha cell",
            "programs": [
                {
                    "id": "alpha-identity",
                    "name": "Alpha-cell identity",
                    "category": "Core identity",
                    "function": "Mature alpha-cell transcriptional identity",
                    "genes": ["GCG", "ARX", "MAFB", "IRX2", "IRX1", "TTR"],
                },
                {
                    "id": "glucagon",
                    "name": "Glucagon biosynthesis",
                    "category": "Secretion",
                    "function": "Production and processing of glucagon",
                    "genes": ["GCG", "PCSK2", "CPE", "PAM"],
                },
                {
                    "id": "alpha-secretion",
                    "name": "Stimulus-secretion coupling",
                    "category": "Secretion",
                    "function": "Low-glucose sensing and glucagon release",
                    "genes": ["KCNK16", "CACNA1A", "SCN9A", "SNAP25", "STX1A", "SYT7"],
                },
                {
                    "id": "alpha-granule",
                    "name": "Secretory granule biology",
                    "category": "Secretion",
                    "function": "Granule formation, trafficking, and docking",
                    "genes": ["CHGA", "CHGB", "SCG2", "RAB3A", "VAMP2"],
                },
                {
                    "id": "alpha-metabolism",
                    "name": "Oxidative metabolism",
                    "category": "Metabolism",
                    "function": "ATP production and glucose oxidation",
                    "genes": ["IDH3A", "SDHB", "NDUFA", "COX", "ATP5"],
                },
                {
                    "id": "alpha-er-folding",
                    "name": "ER protein folding",
                    "category": "Protein homeostasis",
                    "function": "Folding of secreted proteins",
                    "genes": ["HSPA5", "PDIA4", "PDIA6", "CALR", "CANX"],
                },
                {
                    "id": "alpha-upr",
                    "name": "Unfolded protein response",
                    "category": "Protein homeostasis",
                    "function": "Adaptive ER stress",
                    "genes": ["XBP1", "ATF6", "EIF2AK3", "DDIT3", "ATF4"],
                },
                {
                    "id": "alpha-oxidative-stress",
                    "name": "Oxidative stress response",
                    "category": "Stress response",
                    "function": "Detoxification of reactive oxygen species",
                    "genes": ["TXN", "PRDX1", "GPX1", "SOD2"],
                },
                {
                    "id": "alpha-interferon",
                    "name": "Interferon response",
                    "category": "Immune response",
                    "function": "Antiviral and inflammatory signaling",
                    "genes": ["STAT1", "IFIT1", "IFI44L", "MX1", "ISG15"],
                },
                {
                    "id": "alpha-antigen",
                    "name": "Antigen presentation",
                    "category": "Immune response",
                    "function": "Immune visibility",
                    "genes": ["B2M", "HLA-A", "HLA-B", "TAP1", "TAP2"],
                },
                {
                    "id": "alpha-dediff",
                    "name": "Dedifferentiation / transdifferentiation",
                    "category": "Cell fate",
                    "function": "Loss of alpha identity and drift toward a beta-like or progenitor state",
                    "genes": ["ARX", "PAX4", "MAFB", "SOX9"],
                },
                {
                    "id": "alpha-apoptosis",
                    "name": "Apoptosis",
                    "category": "Cell fate",
                    "function": "Programmed cell death",
                    "genes": ["BAX", "BBC3", "PMAIP1", "CASP3"],
                },
                {
                    "id": "alpha-survival",
                    "name": "Survival",
                    "category": "Cell fate",
                    "function": "Anti-apoptotic programs",
                    "genes": ["BCL2L1", "MCL1"],
                },
            ],
            "states": [
                {
                    "id": "mature-functional-alpha",
                    "name": "Mature functional alpha cell",
                    "phenotype": "Canonical healthy alpha cell",
                    "genes": ["GCG", "ARX", "MAFB", "TTR", "IRX2", "IRX1", "PAX6", "FEV", "LOXL4", "CRYBA2", "GC", "SLC7A2"],
                    "notes": "Verified via WebSearch. Canonical alpha-cell identity/marker panel including transcription factors and human-alpha-enriched surface/secreted markers identified in single-cell islet atlases (LOXL4, CRYBA2, GC, SLC7A2 recur across human alpha-cell scRNA-seq studies; SLC7A2 confirmed functionally required for alpha-cell proliferation/secretion, JCI 2024).",
                    "activities": {
                        "alpha-identity": 3,
                        "glucagon": 3,
                        "alpha-secretion": 3,
                        "alpha-granule": 2,
                        "alpha-metabolism": 2,
                        "alpha-upr": -1,
                        "alpha-interferon": -1,
                        "alpha-apoptosis": -1,
                    },
                },
                {
                    "id": "hyperglucagonemic",
                    "name": "Hyperglucagonemic alpha cell",
                    "phenotype": "Chronic hyperglycemia-driven overactivity seen in T2D",
                    "genes": ["GCG", "PCSK2", "CHGA", "SLC7A2", "SLC38A5", "ARX", "MAFB", "TTR", "TXNIP"],
                    "notes": "Verified via WebSearch; fewer than 10 genes because a distinct human single-cell transcriptomic signature for chronic hyperglucagonemia (as opposed to physiology) is not well established. SLC38A5/SLC7A2 amino-acid transporter induction is documented in the liver-alpha-cell axis literature on glucagon receptor resistance/hyperglucagonemia (Kim et al. 2017 Cell Metab; Dean lab SLC7A2 studies, JCI 2024); remaining genes reflect increased glucagon biosynthetic machinery.",
                    "activities": {
                        "alpha-identity": 2,
                        "glucagon": 3,
                        "alpha-secretion": 2,
                        "alpha-granule": 2,
                        "alpha-metabolism": 2,
                        "alpha-er-folding": 1,
                        "alpha-upr": 1,
                        "alpha-oxidative-stress": 1,
                    },
                },
                {
                    "id": "alpha-dedifferentiated",
                    "name": "Dedifferentiated alpha cell",
                    "phenotype": "Loss of alpha identity reported in long-standing T1D and T2D",
                    "genes": ["PAX4", "SOX9", "NKX6-1", "PDX1", "INS", "MAFA", "GATA6", "HES1"],
                    "notes": "Verified via WebSearch; fewer than 10 genes as human evidence for alpha-cell dedifferentiation is much thinner than for beta cells. PAX4 gain and reduced ARX with increased NKX6.1 in alpha cells accompanying reduced beta-cell mass was directly shown in human pancreas (Sci Rep 2021, 'Increased NKX6.1... decreased ARX expression in alpha cells'); SOX9/GATA6/HES1 are shared progenitor-reversion markers by analogy to beta-cell dedifferentiation literature.",
                    "activities": {
                        "alpha-identity": -2,
                        "glucagon": -2,
                        "alpha-dediff": 3,
                        "alpha-oxidative-stress": 1,
                        "alpha-apoptosis": 1,
                    },
                },
                {
                    "id": "alpha-inflammatory",
                    "name": "Inflammatory response alpha cell",
                    "phenotype": "Cytokine and interferon exposure typical of insulitis in T1D",
                    "genes": ["STAT1", "IFIT1", "B2M", "IFI44L", "MX1", "ISG15", "HLA-A", "HLA-B", "TAP1", "CXCL10", "IRF1"],
                    "notes": "Interferon-stimulated gene/MHC-I signature also documented in alpha cells during insulitis, with alpha cells showing even stronger basal and induced immune/HLA responses than beta cells in T1D single-cell studies (Russell et al. 2019 Diabetes).",
                    "activities": {
                        "alpha-identity": -1,
                        "alpha-interferon": 3,
                        "alpha-antigen": 3,
                        "alpha-upr": 1,
                        "alpha-oxidative-stress": 1,
                    },
                },
            ],
        },
    ],
    "references": SEED_REFERENCES,
}


def split_genes(value):
    return [gene.strip() for gene in value.split(",") if gene.strip()]


def slugify(value, existing_ids):
    base = "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")
    base = "-".join(part for part in base.split("-") if part)
    base = base or "item"
    candidate = base
    suffix = 2
    while candidate in existing_ids:
        candidate = "{}-{}".format(base, suffix)
        suffix += 1
    return candidate


def validate_model(model):
    if not isinstance(model, dict):
        raise ValueError("Model must be a JSON object.")

    if isinstance(model.get("cellTypes"), list):
        raw_cell_types = model["cellTypes"]
    elif isinstance(model.get("programs"), list) and isinstance(model.get("states"), list):
        # Legacy single-cell-type format: wrap it as one cell type.
        raw_cell_types = [{
            "id": "beta-cell",
            "name": "Beta cell",
            "programs": model["programs"],
            "states": model["states"],
        }]
    else:
        raise ValueError("Model must contain a cellTypes array (or legacy programs/states arrays).")

    if not raw_cell_types:
        raise ValueError("Model must contain at least one cell type.")

    cell_type_ids = set()
    validated_cell_types = []
    for cell_type in raw_cell_types:
        if not isinstance(cell_type, dict) or not cell_type.get("name"):
            raise ValueError("Each cell type needs a name.")

        cell_type_id = cell_type.get("id") or slugify(cell_type["name"], cell_type_ids)
        if cell_type_id in cell_type_ids:
            cell_type_id = slugify(cell_type_id, cell_type_ids)
        cell_type_ids.add(cell_type_id)

        programs = cell_type.get("programs")
        states = cell_type.get("states")
        if not isinstance(programs, list) or not isinstance(states, list):
            raise ValueError("Each cell type needs programs and states arrays.")

        for program in programs:
            if not program.get("id") or not program.get("name"):
                raise ValueError("Each program needs an id and name.")
            program.setdefault("category", "")
            program.setdefault("function", "")
            if not isinstance(program.get("genes"), list):
                program["genes"] = []

        program_ids = {program["id"] for program in programs}
        for state in states:
            if not state.get("id") or not state.get("name"):
                raise ValueError("Each state needs an id and name.")
            state.setdefault("phenotype", "")
            state.setdefault("notes", "")
            if not isinstance(state.get("genes"), list):
                state["genes"] = []
            if not isinstance(state.get("activities"), dict):
                state["activities"] = {}
            state["activities"] = {
                program_id: int(level)
                for program_id, level in state["activities"].items()
                if program_id in program_ids and int(level) in ACTIVITY_LABELS
            }

        validated_cell_types.append({
            "id": cell_type_id,
            "name": cell_type["name"],
            "programs": programs,
            "states": states,
        })

    # Preserve any top-level literature references so they survive a
    # load/save round-trip instead of being silently dropped.
    references = model.get("references")
    if not isinstance(references, list):
        references = []

    return {"cellTypes": validated_cell_types, "references": references}


class ScrollFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = ttk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.content.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._resize_content)

    def _update_scroll_region(self, _event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_content(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)


class CellStateApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Cell State Model Editor")
        self.geometry("1180x800")
        self.minsize(980, 640)

        self.model = copy.deepcopy(DEFAULT_MODEL)
        self.file_path = None
        self.dirty = False
        self.selected_cell_type_id = self.model["cellTypes"][0]["id"]
        cell_type = self.current_cell_type()
        self.selected_state_id = cell_type["states"][0]["id"] if cell_type and cell_type["states"] else None
        self.activity_vars = {}
        self._cell_type_order = []

        self._configure_style()
        self._build_menu()
        self._build_layout()
        self.refresh_all()
        self.after(300, self.log_visible_layout)
        self.after(100, self.bring_to_front)

    def _configure_style(self):
        # Switch the named Tk fonts over to the UI font so every ttk widget
        # that defaults to them (Label, Entry, Button, menus, etc.) picks it up,
        # plus the classic tk.Listbox/tk.Text widgets below that also default
        # to TkDefaultFont.
        for font_name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont"):
            try:
                tkfont.nametofont(font_name).configure(family=UI_FONT_FAMILY, size=UI_FONT_SIZE)
            except tk.TclError:
                pass

        self.style = ttk.Style(self)
        self.style.configure("Title.TLabel", font=(UI_FONT_FAMILY, 14, "bold"))
        self.style.configure("Section.TLabel", font=(UI_FONT_FAMILY, 11, "bold"))
        self.style.configure("Muted.TLabel", foreground="#647178")
        self.style.configure("Selected.TButton", font=(UI_FONT_FAMILY, 9, "bold"))

    def _build_menu(self):
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="New from defaults", command=self.new_from_defaults)
        file_menu.add_command(label="Open JSON...", command=self.open_json)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save As...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.on_close)
        menu.add_cascade(label="File", menu=file_menu)
        self.configure(menu=menu)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_layout(self):
        # NOTE: this used to lay out header/left/right with .place(). On macOS,
        # Tk's place() manager combined with older bundled Tcl/Tk builds (8.5.x
        # and some 8.6.9 builds) has a known bug where content inside
        # place()-managed frames never gets painted. grid() does not have this
        # problem, so the whole top-level layout uses grid() instead.
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self, padding=(12, 12, 12, 0))
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.title_label = ttk.Label(header, text="Program space", style="Title.TLabel")
        self.title_label.pack(side="left")
        self.status_label = ttk.Label(header, text="", style="Muted.TLabel")
        self.status_label.pack(side="right")

        # Tissue is made up of multiple cell types; this bar picks which
        # cell type's programs/states are shown below.
        cell_type_bar = ttk.Frame(self, padding=(12, 8, 12, 8))
        cell_type_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        ttk.Label(cell_type_bar, text="Cell type", style="Section.TLabel").pack(side="left", padx=(0, 8))
        self.cell_type_var = tk.StringVar()
        self.cell_type_combo = ttk.Combobox(cell_type_bar, textvariable=self.cell_type_var, state="readonly", width=24)
        self.cell_type_combo.pack(side="left")
        self.cell_type_combo.bind("<<ComboboxSelected>>", self.on_cell_type_select)
        ttk.Button(cell_type_bar, text="Add cell type", command=self.add_cell_type).pack(side="left", padx=(10, 0))
        ttk.Button(cell_type_bar, text="Rename", command=self.rename_cell_type).pack(side="left", padx=(6, 0))
        ttk.Button(cell_type_bar, text="Delete cell type", command=self.delete_cell_type).pack(side="left", padx=(6, 0))

        left = ttk.Frame(self, width=280, padding=(12, 0, 10, 12))
        right = ttk.Frame(self, padding=(10, 0, 12, 12))
        left.grid(row=2, column=0, sticky="nsw")
        right.grid(row=2, column=1, sticky="nsew")
        left.grid_propagate(False)
        left.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(2, weight=1)

        ttk.Label(left, text="States", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        self.state_list = tk.Listbox(left, height=18, exportselection=False)
        self.state_list.grid(row=1, column=0, sticky="nsew", pady=(6, 8))
        self.state_list.bind("<<ListboxSelect>>", self.on_state_select)

        state_buttons = ttk.Frame(left)
        state_buttons.grid(row=2, column=0, sticky="ew")
        ttk.Button(state_buttons, text="Add", command=self.add_state).pack(side="left", fill="x", expand=True)
        ttk.Button(state_buttons, text="Duplicate", command=self.duplicate_state).pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(state_buttons, text="Delete", command=self.delete_state).pack(side="left", fill="x", expand=True)

        ttk.Separator(left).grid(row=3, column=0, sticky="ew", pady=14)
        ttk.Label(left, text="Programs", style="Section.TLabel").grid(row=4, column=0, sticky="w")
        ttk.Button(left, text="Add program", command=self.add_program).grid(row=5, column=0, sticky="ew", pady=(6, 5))
        ttk.Button(left, text="Edit selected program", command=self.edit_selected_program).grid(row=6, column=0, sticky="ew")

        details = ttk.LabelFrame(right, text="Selected state", padding=10)
        details.grid(row=0, column=0, sticky="ew")

        ttk.Label(details, text="Name").grid(row=0, column=0, sticky="w")
        self.state_name = ttk.Entry(details)
        self.state_name.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=3)

        ttk.Label(details, text="Phenotype").grid(row=1, column=0, sticky="nw")
        self.state_phenotype = tk.Text(details, height=3, wrap="word")
        self.state_phenotype.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=3)

        ttk.Button(details, text="Apply state details", command=self.apply_state_details).grid(row=2, column=1, sticky="e", pady=(7, 0))
        details.columnconfigure(1, weight=1)

        activity_header = ttk.Frame(right)
        activity_header.grid(row=1, column=0, sticky="ew", pady=(14, 6))
        ttk.Label(activity_header, text="Programs sorted by activity", style="Section.TLabel").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_args: self.refresh_program_rows())
        search = ttk.Entry(activity_header, textvariable=self.search_var)
        search.pack(side="right", fill="x", expand=True, padx=(16, 0))
        search.insert(0, "")

        self.program_scroll = ScrollFrame(right)
        self.program_scroll.grid(row=2, column=0, sticky="nsew")

    def bring_to_front(self):
        self.deiconify()
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(500, lambda: self.attributes("-topmost", False))
        # macOS Tk (especially the system-installed Tcl/Tk 8.5/8.6.9 builds) has a
        # known bug where the window frame draws but the widgets inside stay blank
        # until the window is resized. Force a redraw by nudging the size by a
        # pixel and back.
        self.update_idletasks()
        width, height = self.winfo_width(), self.winfo_height()
        self.geometry("{}x{}".format(width + 1, height))
        self.after(50, lambda: self.geometry("{}x{}".format(width, height)))

    def log_visible_layout(self):
        logging.info(
            "Visible layout root=%sx%s state_list=%sx%s program_area=%sx%s",
            self.winfo_width(),
            self.winfo_height(),
            self.state_list.winfo_width(),
            self.state_list.winfo_height(),
            self.program_scroll.winfo_width(),
            self.program_scroll.winfo_height(),
        )

    def current_cell_type(self):
        for cell_type in self.model["cellTypes"]:
            if cell_type["id"] == self.selected_cell_type_id:
                return cell_type
        return self.model["cellTypes"][0] if self.model["cellTypes"] else None

    def current_state(self):
        cell_type = self.current_cell_type()
        if not cell_type:
            return None
        for state in cell_type["states"]:
            if state["id"] == self.selected_state_id:
                return state
        return None

    def selected_program_id(self):
        focused = self.focus_get()
        if focused is not None:
            return getattr(focused, "program_id", None)
        return None

    def mark_dirty(self):
        self.dirty = True
        self.update_status()

    def update_status(self):
        name = os.path.basename(self.file_path) if self.file_path else "Untitled model"
        marker = "modified" if self.dirty else "saved"
        self.status_label.configure(text="{} ({})".format(name, marker))

    def refresh_all(self):
        self.refresh_cell_type_options()
        self.refresh_state_list()
        self.refresh_state_details()
        self.refresh_program_rows()
        self.update_status()

    def refresh_cell_type_options(self):
        cell_types = self.model["cellTypes"]
        self._cell_type_order = [cell_type["id"] for cell_type in cell_types]

        if self.selected_cell_type_id not in self._cell_type_order:
            self.selected_cell_type_id = self._cell_type_order[0] if self._cell_type_order else None

        self.cell_type_combo["values"] = [cell_type["name"] for cell_type in cell_types]
        if cell_types and self.selected_cell_type_id in self._cell_type_order:
            self.cell_type_combo.current(self._cell_type_order.index(self.selected_cell_type_id))

        cell_type = self.current_cell_type()
        self.title_label.configure(text="{} program space".format(cell_type["name"]) if cell_type else "Program space")

    def on_cell_type_select(self, _event):
        index = self.cell_type_combo.current()
        if index < 0 or index >= len(self._cell_type_order):
            return
        self.selected_cell_type_id = self._cell_type_order[index]
        cell_type = self.current_cell_type()
        self.selected_state_id = cell_type["states"][0]["id"] if cell_type and cell_type["states"] else None
        self.refresh_all()

    def add_cell_type(self):
        name = simpledialog.askstring("Add cell type", "Cell type name:", parent=self)
        if not name:
            return
        existing = {cell_type["id"] for cell_type in self.model["cellTypes"]}
        cell_type = {"id": slugify(name, existing), "name": name.strip(), "programs": [], "states": []}
        self.model["cellTypes"].append(cell_type)
        self.selected_cell_type_id = cell_type["id"]
        self.selected_state_id = None
        self.mark_dirty()
        self.refresh_all()

    def rename_cell_type(self):
        cell_type = self.current_cell_type()
        if not cell_type:
            return
        name = simpledialog.askstring(
            "Rename cell type", "Cell type name:", initialvalue=cell_type["name"], parent=self
        )
        if not name:
            return
        cell_type["name"] = name.strip()
        self.mark_dirty()
        self.refresh_all()

    def delete_cell_type(self):
        cell_type = self.current_cell_type()
        if not cell_type:
            return
        if len(self.model["cellTypes"]) == 1:
            messagebox.showerror("Cannot delete", "The model needs at least one cell type.")
            return
        if not messagebox.askyesno(
            "Delete cell type",
            "Delete '{}' and all of its programs and states?".format(cell_type["name"]),
        ):
            return
        self.model["cellTypes"] = [item for item in self.model["cellTypes"] if item["id"] != cell_type["id"]]
        self.selected_cell_type_id = self.model["cellTypes"][0]["id"]
        self.selected_state_id = None
        self.mark_dirty()
        self.refresh_all()

    def refresh_state_list(self):
        self.state_list.delete(0, tk.END)
        cell_type = self.current_cell_type()
        states = cell_type["states"] if cell_type else []

        selected_index = 0
        for index, state in enumerate(states):
            active = sum(1 for level in state.get("activities", {}).values() if level != 0)
            self.state_list.insert(tk.END, "{}  ({} active)".format(state["name"], active))
            if state["id"] == self.selected_state_id:
                selected_index = index
        if states:
            self.state_list.selection_set(selected_index)
            self.state_list.activate(selected_index)

    def refresh_state_details(self):
        state = self.current_state()
        self.state_name.delete(0, tk.END)
        self.state_phenotype.delete("1.0", tk.END)
        if not state:
            return
        self.state_name.insert(0, state.get("name", ""))
        self.state_phenotype.insert("1.0", state.get("phenotype", ""))

    def refresh_program_rows(self):
        for child in self.program_scroll.content.winfo_children():
            child.destroy()
        self.activity_vars = {}

        state = self.current_state()
        cell_type = self.current_cell_type()
        if not state or not cell_type:
            ttk.Label(self.program_scroll.content, text="No state selected.").pack(anchor="w", padx=8, pady=8)
            return

        query = self.search_var.get().strip().lower()
        programs = list(cell_type["programs"])
        if query:
            programs = [
                program
                for program in programs
                if query in " ".join(
                    [program["name"], program.get("category", ""), program.get("function", "")]
                    + program.get("genes", [])
                ).lower()
            ]

        programs.sort(
            key=lambda program: (
                -abs(state.get("activities", {}).get(program["id"], 0)),
                -state.get("activities", {}).get(program["id"], 0),
                program["name"].lower(),
            )
        )

        for row_index, program in enumerate(programs):
            self._add_program_row(row_index, state, program)

    def _add_program_row(self, row_index, state, program):
        row = ttk.Frame(self.program_scroll.content, padding=(8, 8))
        row.pack(fill="x", pady=(0, 4))
        row.columnconfigure(0, weight=1)

        title = "{}  [{}]".format(program["name"], program.get("category", ""))
        ttk.Label(row, text=title, style="Section.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(row, text=program.get("function", ""), style="Muted.TLabel", wraplength=640).grid(row=1, column=0, sticky="w", pady=(2, 0))
        ttk.Label(row, text=", ".join(program.get("genes", [])), wraplength=640).grid(row=2, column=0, sticky="w", pady=(4, 0))

        level = state.get("activities", {}).get(program["id"], 0)
        var = tk.StringVar(value=ACTIVITY_LABELS.get(level, "baseline"))
        self.activity_vars[program["id"]] = var
        combo = ttk.Combobox(row, textvariable=var, values=[label for _value, label in ACTIVITY_LEVELS], state="readonly", width=12)
        combo.program_id = program["id"]
        combo.grid(row=0, column=1, sticky="e", padx=(12, 0))
        combo.bind("<<ComboboxSelected>>", lambda _event, program_id=program["id"], value_var=var: self.set_activity(program_id, value_var.get()))

        edit_button = ttk.Button(row, text="Edit program", command=lambda program_id=program["id"]: self.edit_program(program_id))
        edit_button.program_id = program["id"]
        edit_button.grid(row=1, column=1, sticky="e", padx=(12, 0), pady=(3, 0))

        separator = ttk.Separator(self.program_scroll.content)
        separator.pack(fill="x", pady=(0, 4))

    def on_state_select(self, _event):
        selection = self.state_list.curselection()
        if not selection:
            return
        cell_type = self.current_cell_type()
        if not cell_type:
            return
        self.selected_state_id = cell_type["states"][selection[0]]["id"]
        self.refresh_state_details()
        self.refresh_program_rows()

    def apply_state_details(self):
        state = self.current_state()
        if not state:
            return
        name = self.state_name.get().strip()
        if not name:
            messagebox.showerror("Missing name", "State name cannot be empty.")
            return
        state["name"] = name
        state["phenotype"] = self.state_phenotype.get("1.0", tk.END).strip()
        self.mark_dirty()
        self.refresh_state_list()

    def set_activity(self, program_id, label):
        state = self.current_state()
        if not state:
            return
        state.setdefault("activities", {})[program_id] = ACTIVITY_VALUES[label]
        self.mark_dirty()
        self.refresh_state_list()
        self.refresh_program_rows()

    def add_state(self):
        cell_type = self.current_cell_type()
        if not cell_type:
            return
        name = simpledialog.askstring("Add state", "State name:", parent=self)
        if not name:
            return
        existing = {state["id"] for state in cell_type["states"]}
        state = {
            "id": slugify(name, existing),
            "name": name.strip(),
            "phenotype": "",
            "genes": [],
            "activities": {},
        }
        cell_type["states"].append(state)
        self.selected_state_id = state["id"]
        self.mark_dirty()
        self.refresh_all()

    def duplicate_state(self):
        cell_type = self.current_cell_type()
        state = self.current_state()
        if not cell_type or not state:
            return
        copied = copy.deepcopy(state)
        copied["name"] = "{} copy".format(copied["name"])
        copied["id"] = slugify(copied["name"], {item["id"] for item in cell_type["states"]})
        cell_type["states"].append(copied)
        self.selected_state_id = copied["id"]
        self.mark_dirty()
        self.refresh_all()

    def delete_state(self):
        cell_type = self.current_cell_type()
        state = self.current_state()
        if not cell_type or not state:
            return
        if len(cell_type["states"]) == 1:
            messagebox.showerror("Cannot delete", "The cell type needs at least one state.")
            return
        if not messagebox.askyesno("Delete state", "Delete '{}'?".format(state["name"])):
            return
        cell_type["states"] = [item for item in cell_type["states"] if item["id"] != state["id"]]
        self.selected_state_id = cell_type["states"][0]["id"]
        self.mark_dirty()
        self.refresh_all()

    def add_program(self):
        self.edit_program(None)

    def edit_selected_program(self):
        program_id = self.selected_program_id()
        if not program_id:
            messagebox.showinfo("Select a program", "Click in a program activity field or use an Edit program button.")
            return
        self.edit_program(program_id)

    def edit_program(self, program_id):
        cell_type = self.current_cell_type()
        if not cell_type:
            return
        program = None
        if program_id:
            program = next((item for item in cell_type["programs"] if item["id"] == program_id), None)
        ProgramDialog(self, program, self.save_program)

    def save_program(self, original_id, program):
        cell_type = self.current_cell_type()
        if not cell_type:
            return False
        existing_ids = {item["id"] for item in cell_type["programs"] if item["id"] != original_id}
        if not program["id"]:
            program["id"] = slugify(program["name"], existing_ids)
        if program["id"] in existing_ids:
            messagebox.showerror("Duplicate id", "A program with this id already exists.")
            return False

        if original_id:
            for index, item in enumerate(cell_type["programs"]):
                if item["id"] == original_id:
                    cell_type["programs"][index] = program
                    break
            if original_id != program["id"]:
                for state in cell_type["states"]:
                    activities = state.setdefault("activities", {})
                    if original_id in activities:
                        activities[program["id"]] = activities.pop(original_id)
        else:
            cell_type["programs"].append(program)

        self.mark_dirty()
        self.refresh_program_rows()
        return True

    def _reset_selection_after_load(self):
        self.selected_cell_type_id = self.model["cellTypes"][0]["id"] if self.model["cellTypes"] else None
        cell_type = self.current_cell_type()
        self.selected_state_id = cell_type["states"][0]["id"] if cell_type and cell_type["states"] else None

    def new_from_defaults(self):
        if not self.confirm_discard_changes():
            return
        self.model = copy.deepcopy(DEFAULT_MODEL)
        self.file_path = None
        self.dirty = False
        self._reset_selection_after_load()
        self.refresh_all()

    def open_json(self):
        if not self.confirm_discard_changes():
            return
        path = filedialog.askopenfilename(
            title="Open model JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as handle:
                self.model = validate_model(json.load(handle))
        except Exception as exc:
            messagebox.showerror("Could not open file", str(exc))
            return
        self.file_path = path
        self.dirty = False
        self._reset_selection_after_load()
        self.refresh_all()

    def save(self):
        if not self.file_path:
            return self.save_as()
        try:
            with open(self.file_path, "w", encoding="utf-8") as handle:
                json.dump(self.model, handle, indent=2)
                handle.write("\n")
        except Exception as exc:
            messagebox.showerror("Could not save file", str(exc))
            return False
        self.dirty = False
        self.update_status()
        return True

    def save_as(self):
        path = filedialog.asksaveasfilename(
            title="Save model JSON",
            defaultextension=".json",
            initialfile="islet-cell-state-model.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return False
        self.file_path = path
        return self.save()

    def confirm_discard_changes(self):
        if not self.dirty:
            return True
        choice = messagebox.askyesnocancel("Unsaved changes", "Save changes before continuing?")
        if choice is None:
            return False
        if choice:
            return self.save()
        return True

    def on_close(self):
        if self.confirm_discard_changes():
            self.destroy()


class ProgramDialog(tk.Toplevel):
    def __init__(self, parent, program, callback):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.original_id = program["id"] if program else None
        self.callback = callback
        self.title("Edit program" if program else "Add program")
        self.transient(parent)
        self.grab_set()

        data = program or {"id": "", "name": "", "category": "", "function": "", "genes": []}
        frame = ttk.Frame(self, padding=14)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        self.fields = {}
        rows = [
            ("ID", "id", data.get("id", "")),
            ("Name", "name", data.get("name", "")),
            ("Category", "category", data.get("category", "")),
            ("Genes", "genes", ", ".join(data.get("genes", []))),
        ]
        for row_index, (label, key, value) in enumerate(rows):
            ttk.Label(frame, text=label).grid(row=row_index, column=0, sticky="w", pady=3)
            entry = ttk.Entry(frame)
            entry.insert(0, value)
            entry.grid(row=row_index, column=1, sticky="ew", padx=(8, 0), pady=3)
            self.fields[key] = entry

        ttk.Label(frame, text="Function").grid(row=4, column=0, sticky="nw", pady=3)
        self.function_text = tk.Text(frame, height=4, wrap="word")
        self.function_text.insert("1.0", data.get("function", ""))
        self.function_text.grid(row=4, column=1, sticky="ew", padx=(8, 0), pady=3)

        buttons = ttk.Frame(frame)
        buttons.grid(row=5, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="left", padx=(0, 6))
        ttk.Button(buttons, text="Save", command=self.save).pack(side="left")

        self.fields["name"].focus_set()

    def save(self):
        name = self.fields["name"].get().strip()
        if not name:
            messagebox.showerror("Missing name", "Program name cannot be empty.", parent=self)
            return
        program = {
            "id": self.fields["id"].get().strip(),
            "name": name,
            "category": self.fields["category"].get().strip(),
            "function": self.function_text.get("1.0", tk.END).strip(),
            "genes": split_genes(self.fields["genes"].get()),
        }
        if self.callback(self.original_id, program):
            self.destroy()


if __name__ == "__main__":
    try:
        logging.info("Starting Cell State Model Editor")
        app = CellStateApp()
        total_programs = sum(len(cell_type["programs"]) for cell_type in app.model["cellTypes"])
        total_states = sum(len(cell_type["states"]) for cell_type in app.model["cellTypes"])
        logging.info(
            "Window created with %s cell types, %s states, and %s programs",
            len(app.model["cellTypes"]),
            total_states,
            total_programs,
        )
        print("Window created. If you do not see it, check Mission Control or other Spaces.")
        app.mainloop()
        logging.info("Main loop exited")
    except Exception:
        logging.exception("Fatal startup error")
        print("Fatal startup error. See {}".format(LOG_PATH), file=sys.stderr)
        raise
