# GRAPHS REF.
--------------

**meaning of numbers:**
- 18  = # sectors in the TPC (one side, IROC+OROC together)
- 72  = # sectors in the TPC (two sides, IROC and OROC separately)
- 144 = arbitrary number of bins in phi (two sides, IROC and OROC separately)
- 10  = arbitrary number of bins in eta
_____________________________________________________________________

## graphs

* TPC clusters/tracks (144 points for "Phi", 18 for "Sector")  
    - grNclPhi[Pos/Neg][A/C] -- number of clusters of positively/negatively charged  tracks on A/C side as a func. of phi  
    - grNtrPhi[Pos/Neg][A/C] -- as above but for tracks  
    - grNclSector[Pos/Neg][A/C] -- as above but as a function of sector id (exactly the same but with lower granularity: 18 instead of 144)  
    - grNtrSector[Pos/Neg][A/C] -- as above

* DCA (144 points for phi, 10 for eta)
    - grdca[r/z]\_[pos/neg]\_[[A/C]SidePhi/Eta] -- radial/z component of the DCAs (distances of closest approach) of positive/negative tracks on A/C side as a function of phi/eta

* per sector: occupancy and electronics status,
    see e.g.: http://aliqatpceos.web.cern.ch/aliqatpceos/data/2018/LHC18o/pass1/000293496/rawQAInformation.png  
    and   http://aliqatpceos.web.cern.ch/aliqatpceos/data/2018/LHC18r/pass1/000297333/cluster_occupancy.png
    - 3 different estimates of occupancy (important):
        + grRawLocalMax -- number of maxima in the signal
        + grRawAboveThr -- number of above threshold
        + grRawQMax     -- maximal charge measured
    - electronics:
        + grOCDBStatus  -- if OCDB was available (if not then default calibration params were used)
        + grActiveHV    -- if HighVoltage is active in the sector (if not, nothing is measured)
        + grActiveAltro -- if single read-out pixels were switched on
        + grActiveDDL   -- if DDL was active?
        + grActiveSCD

* HV in given Read-Out Chamber (72 points)
    - grROCHVStatus
    - grROCHVTimeFraction
    - grROCHVMedian
    - grROCHVNominal

-----------------------------------

** Actual list of graphs + number of points: **

- grNclPhiPosA. 144
- grNclPhiNegA. 144
- grNclPhiPosC. 144
- grNclPhiNegC. 144
- grNtrPhiPosA. 144
- grNtrPhiNegA. 144
- grNtrPhiPosC. 144
- grNtrPhiNegC. 144

- grNclSectorPosA. 18
- grNclSectorNegA. 18
- grNclSectorPosC. 18
- grNclSectorNegC. 18
- grNtrSectorPosA. 18
- grNtrSectorNegA. 18
- grNtrSectorPosC. 18
- grNtrSectorNegC. 18

- grOCDBStatus. 72
- grRawLocalMax. 72
- grRawAboveThr. 72
- grRawQMax. 72
- grActiveHV. 72
- grActiveAltro. 72
- grActiveDDL. 72
- grActiveSCD. 72
- grROCHVStatus. 72
- grROCHVTimeFraction. 72
- grROCHVMedian. 72
- grROCHVNominal. 72

- grdcar_pos_Eta. 10
- grdcar_neg_Eta. 10
- grdcaz_pos_Eta. 10
- grdcaz_neg_Eta. 10

- grdcar_pos_ASidePhi. 144
- grdcar_neg_ASidePhi. 144
- grdcaz_pos_ASidePhi. 144
- grdcaz_neg_ASidePhi. 144
- grdcar_pos_CSidePhi. 144
- grdcar_neg_CSidePhi. 144
- grdcaz_pos_CSidePhi. 144
- grdcaz_neg_CSidePhi. 144
