#!/bin/sh
START_TIME=$SECONDS
python cross_match.py --separation=180 --make_table \
	--table1=../original_cats/mwacs_all_b3_140206.vot \
	--details1=Name,RAJ2000,e_RAJ2000,DEJ2000,e_DEJ2000,180,S180,e_S180,PA,MajAxis,MinAxis,Fit,- \
	--units1=deg,arcmin,deg,arcmin,Jy,Jy,deg,arcmin,arcmin \
	--ra_lims1=0,100 \
	--dec_lims1=-55,-20 \
	--prefix1=mwacs \
	--table2=../original_cats/vlssr_names.vot \
	--details2=Name,RA,RA_error,Dec,Dec_error,74,Flux,Flux_error,PA,major,minor,-,ID \
	--units2=deg,arcsec,deg,arcsec,Jy,Jy,deg,arcsec,arcsec \
	--ra_lims2=0,140 \
	--dec_lims2=-20,40 \
	--prefix2=vlssr
STRING_1="Time to match vlssr: "
TIME_1=$SECONDS
ELAPSED_1=$(($TIME_1 - $START_TIME))
PRINT_1=$STRING_1$ELAPSED_1
echo $PRINT_1
#-------------------------------------------------------------------------------------------------
python cross_match.py --separation=180 --make_table \
	--table1=../original_cats/mwacs_all_b3_140206.vot \
	--details1=Name,RAJ2000,e_RAJ2000,DEJ2000,e_DEJ2000,180,S180,e_S180,PA,MajAxis,MinAxis,Fit,- \
	--units1=deg,arcmin,deg,arcmin,Jy,Jy,deg,arcmin,arcmin \
	--ra_lims1=0,100 \
	--dec_lims1=-55,-20 \
	--prefix1=mwacs \
	--table2=../original_cats/vizier_mrc.vot \
	--details2=MRC,_RAJ2000,e_RA2000,_DEJ2000,e_DE2000,408,S408,e_S408,-,-,-,Mflag,- \
	--units2=deg,sec,deg,arcsec,Jy,Jy,-,-,- \
	--ra_lims2=150,250 \
	--dec_lims2=-30,10 \
	--prefix2=mrc
STRING_2="Time to match mrc: "
TIME_2=$SECONDS
ELAPSED_2=$(($TIME_2 - $TIME_1))
PRINT_2=$STRING_2$ELAPSED_2
echo $PRINT_2
#-------------------------------------------------------------------------------------------------
python cross_match.py --separation=180 --make_table \
	--table1=../original_cats/mwacs_all_b3_140206.vot \
	--details1=Name,RAJ2000,e_RAJ2000,DEJ2000,e_DEJ2000,180,S180,e_S180,PA,MajAxis,MinAxis,Fit,- \
	--units1=deg,arcmin,deg,arcmin,Jy,Jy,deg,arcmin,arcmin \
	--ra_lims1=0,100 \
	--dec_lims1=-55,-20 \
	--prefix1=mwacs \
	--table2=../original_cats/sumss_names.vot \
	--details2=Name,RA,RA_error,Dec,Dec_error,843,Flux,Flux_error,PA,major,minor,-,ID \
	--units2=deg,arcsec,deg,arcsec,Jy,Jy,deg,arcsec,arcsec \
	--ra_lims2=0,100 \
	--dec_lims2=-60,-30 \
	--prefix2=sumss
STRING_3="Time to match sumss: "
TIME_3=$SECONDS
ELAPSED_3=$(($TIME_3 - $TIME_2))
PRINT_3=$STRING_3$ELAPSED_3
echo $PRINT_3
#-------------------------------------------------------------------------------------------------
python cross_match.py --separation=180 --make_table \
	--table1=../original_cats/mwacs_all_b3_140206.vot \
	--details1=Name,RAJ2000,e_RAJ2000,DEJ2000,e_DEJ2000,180,S180,e_S180,PA,MajAxis,MinAxis,Fit,- \
	--units1=deg,arcmin,deg,arcmin,Jy,Jy,deg,arcmin,arcmin \
	--ra_lims1=0,100 \
	--dec_lims1=-55,-20 \
	--prefix1=mwacs \
	--table2=../original_cats/nvss_reduced.vot \
	--details2=NVSS,_RAJ2000,e_RAJ2000,_DEJ2000,e_DEJ2000,1400,S1.4,e_S1.4,PA,MajAxis,MinAxis,-,Field \
	--units2=deg,sec,deg,arcsec,mJy,mJy,deg,arcsec,arcsec \
	--ra_lims2=100,200 \
	--dec_lims2=-40,0 \
	--prefix2=nvss
STRING_4="Time to match nvss: "
TIME_4=$SECONDS
ELAPSED_4=$(($TIME_4 - $TIME_3))
PRINT_4=$STRING_4$ELAPSED_4
echo $PRINT_4
#-------------------------------------------------------------------------------------------------
python calculate_bayes.py --primary_cat=mwacs --matched_cats=vlssr,mrc,sumss,nvss \
	--primary_freq=180 --matched_freqs=74,408,843,1400 \
	--out_name=bayes_mw-v-m-s-n.txt
STRING_5="Time to calculate posterior probabilities: "
TIME_5=$SECONDS
ELAPSED_5=$(($TIME_5 - $TIME_4))
PRINT_5=$STRING_5$ELAPSED_5
echo $PRINT_5
-------------------------------------------------------------------------------------------------
python make_table.py --matched_cats=mwacs,vlssr,mrc,sumss,nvss \
	--pref_cats=nvss,sumss,mwacs,mrc,vlssr \
	--input_bayes=bayes_mw-v-m-s-n.txt \
	--cat_freqs=180,74,408,843,1400 \
	--prob_thresh=0.8,0.95 \
	--epsilon_thresh=0.1 --chi_thresh=10 \
	--resolution=00:03:00 \
	--output_name=puma_mw-v-m-s-n --split=00:01:15 #--verbose #--figure_draw=4 #
STRING_6="Time to apply criteria and create final matched table: "
TIME_6=$SECONDS
ELAPSED_6=$(($TIME_6 - $TIME_5))
PRINT_6=$STRING_6$ELAPSED_6
#-------------------------------------------------------------------------------------------------
STRING_7="Total Time: "
TIME_7=$SECONDS
ELAPSED_7=$(($TIME_7 - $START_TIME))
PRINT_7=$STRING_7$ELAPSED_7
echo $PRINT_1
echo $PRINT_2
echo $PRINT_3
echo $PRINT_4
echo $PRINT_5
echo $PRINT_6