// macro exporting time statistics of chunks (1 chunk correspond to single ROOT file) to *.csv file
// it can also draw a plot with run id on horizontal and time on vertical axis

void time2csv(){
    // Float_t convert_time(Float_t cetTimeLHC){
    //     Float_t tstamp = cetTimeLHC+1262304000.-3600.;
    //     return tstamp;
    // }


    const char* run_dir = "data/run-286454/";
    TSystemDirectory dir_data(run_dir, run_dir);
    TList *files_list = dir_data.GetListOfFiles();
    files_list->Sort();
    TIterator *iter = files_list->MakeIterator();

    TSystemFile* sysfile;
    TString file_name;

    Int_t n = 520;
    if (n < 0) n = files_list->GetEntries()-3;
    files_list->Print();
    printf("\n\n n = %d", n);
    Double_t x[n];
    Double_t y[n];
    Double_t ey[n];
    Double_t ex[n];


    FILE *fout = fopen("chunks_stats.csv", "w");
    if (fout == NULL)
    {
        printf("Error opening file!\n");
        exit(1);
    }
    fprintf(fout, "chunk_id,mean,std,mini,median,maxi\n");

    Int_t i = -1;
    while(1){

        sysfile = (TSystemFile*) iter->Next();
        if (!sysfile) break;
        file_name = TString(sysfile->GetName());
        cout<<"---"<<file_name<<endl;
        if (file_name.EndsWith(".root")){
            i += 1;
            if (i > n) break;

            TString fpath = dir_data.GetName()+("/"+TString(file_name));
            // file names: QAresults_18000286454019.2610.root - 4 digits 
            // or        : QAresults_18000286454039.102.root  - 3 digits
            Int_t chunkA = TString( fpath(fpath.First('.')-2, 2) ).Atoi();
            Int_t chunkB = TString( fpath(fpath.First('.')+1, fpath.Last('.')-fpath.First('.')-1) ).Atoi();
            Int_t chunk_id = chunkA*10000 + chunkB;
            if (fpath.Contains("merged")) chunk_id = TString(fpath(fpath.Last('_')+1, fpath.Last('.')-fpath.Last('_')-1)).Atoi();
            TFile *tfile = TFile::Open(fpath);

            gDirectory->cd("Vertex_Performance");
            TList *cOutputVtxESD = (TList*) gROOT->FindObject("cOutputVtxESD");
            TTree *t = (TTree*) cOutputVtxESD->FindObject("fTreeBeamSpot");
            t->Draw("cetTimeLHC >> htime", "", "goff");
            TH1D *htime = (TH1D*) gDirectory->Get("htime");
            // htime->Draw();  // draws histo of time of single chunk

            // they return exactly center of the first/last
            // not empty bin of the hist obtained with tree->Draw("var >> hist")
            Float_t mini = t->GetMinimum("cetTimeLHC");
            Float_t maxi = t->GetMaximum("cetTimeLHC");

            Float_t mean = htime->GetMean();
            Float_t std  = htime->GetStdDev();
            Double_t median, q;
            q = 0.5; // 0.5 for "median"
            htime->GetQuantiles(1, &median, &q);

            x[i] = chunk_id;
            y[i] = (mini+maxi)/2;
            ey[i] = (maxi-mini)/2;
            ex[i] = 0;

            //cout<<"\t mini="<< mini << " maxi=" << maxi <<" chunk_id="<<chunk_id;
            // cout << "chunk_id = " << chunk_id <<
            //         " old_mini = " << mini << " new mini = " << new_mini <<
            //         " old maxi = " << maxi << " new maxi = " << new_maxi <<
            //         endl;
            TString new_id = TString( fpath(fpath.First('_')+1, fpath.Last('.')-fpath.First('_')-1) ).ReplaceAll(".","_");
            // printf("chunk_id = %s  -->  %d.%d\t mean=%.1f std=%.1f mini=%.1f median=%.1f maxi=%.1f\n", new_id.Data(), chunkA, chunkB , mean, std, mini, median, maxi);
            fprintf(fout, "%s,%.1f,%.1f,%.1f,%.1f,%.1f\n", new_id.Data(), mean, std, mini, median, maxi);
        }
        cout<<endl;
    }
    x[0] = x[1];
    y[0] = y[1];
    TGraphErrors *graph = new TGraphErrors(n, x, y, ex, ey);
    graph->SetMarkerStyle(22);

    // PLOT - 1 point = mean of 1 chunk, errorbar = (min,max)
    TDatime da(2010,1,1,1,0,0);
    graph->GetYaxis()->SetTimeOffset(da.Convert());
    graph->GetYaxis()->SetTimeDisplay(1);
    graph->GetYaxis()->SetTimeFormat("|%y%m%d %H:%M:%S|");
    //graph->Draw("ap");

    fclose(fout);

}
