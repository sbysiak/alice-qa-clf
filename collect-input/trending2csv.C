void trending2csv(const char* infname){
    const char* infname = "trending_merged_LHC18q_withStatusTree.root";
    const char* outfname = TString(infname).ReplaceAll(".root", ".csv");
    FILE* outfile;
    outfile = fopen(outfname, "a");

    TFile* infile = TFile::Open(TString(infname));
    if (!infile) return;
    cout << "infile: " << infile << endl;

    // infile->cd();
    TTree *t = (TTree*) infile->Get("tpcQA");
    cout << "tree: " << t << endl;
    if (!t) return;

    char* name = 0;
    TString name_ts = 0;

    TObjArray* branches = t->GetListOfBranches();
    Int_t nBranches = branches->GetSize();
    Double_t* branchVals = 0;
    for (int iBranch=0; iBranch<nBranches; iBranch++){
        name = branches->At(iBranch)->GetName();
        name_ts = TString(name);
        if (name_ts.Contains(".") && (! name_ts.Contains("String"))) continue;
        if (name_ts.EqualTo("rawClusterCounter")) continue;
        if (name_ts.EqualTo("rawSignalCounter")) continue;
        printf("%s\n", name);
        fprintf(outfile, "%s, ", name);
        t->Draw(name, "", "goff");
        branchVals = t->GetV1();
        Double_t val = 0;
        for (int iVal=0; iVal < t->GetEntries(); iVal++){
            val = branchVals[iVal];
            fprintf(outfile, "%f, ", val);
        }
        fprintf(outfile, "\n");
    }

    TList* aliases = t->GetListOfAliases();
    Int_t nAliases = aliases->GetSize();
    Double_t* aliasVals = 0;
    for (int iAlias=0; iAlias < nAliases; iAlias++){
        name = aliases->At(iAlias)->GetName();
        name_ts = TString(name);
        if (name_ts.EqualTo("")) continue;
        if (name_ts.Contains(".") && ! name_ts.Contains("String")) continue;
        if (name_ts.EqualTo("rawClusterCounter")) continue;
        if (name_ts.EqualTo("rawSignalCounter")) continue;
        printf("%s\n", name);
        fprintf(outfile, "%s, ", name);
        t->Draw(name, "", "goff");
        aliasVals = t->GetV1();
        Double_t val = 0;
        for (int iVal=0; iVal < t->GetEntries(); iVal++){
            val = aliasVals[iVal];
            if (iVal != t->GetEntries()-1) fprintf(outfile, "%f, ", val);
            else fprintf(outfile, "%f", val);

        }
        fprintf(outfile, "\n");
    }

    fclose(outfile);
    infile->Close();
}
