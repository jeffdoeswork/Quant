variables:

       //open-close
shape1 (0),
shape2 (0),
shape3 (0),
shape4 (0),
shape5 (0),
shape6 (0),
shape7 (0),
shape8 (0),
shape9 (0),
shape10(0),
shape11(0),
shape12(0),
shape13(0),
shape14(0),
shape15(0),
shape16(0),
shape17(0),
shape18(0),
shape19(0),
shape20(0),
shape21(0),
shape22(0),
shape23(0),
shape24(0),
shape25(0),
shape26(0),
shape27(0),
shape28(0),
shape29(0),
shape30(0),
shape31(0),
shape_magn_ave (0),
shape_ave_31 (0),
shape_ave_3 (0),
shape_ave (0);         //shape average of 5 days

shape1 = close - Open;
shape2 = close[1] - Open[1];
shape3 = close[2] - Open[2];
shape4 = close[3] - Open[3];
shape5 = close[4] - Open[4];
shape6 = close[5] - Open[5];
shape7 = close[6] - Open[6];
shape8 = close[7] - Open[7];
shape9 = close[8] - Open[8];
shape10 = close[9] - Open[9];
shape11 = close[10] - Open[10];
shape12 = close[11] - Open[11];
shape13 = close[12] - Open[12];
shape14 = close[13] - Open[13];
shape15 = close[14] - Open[14];
shape16 = close[15] - Open[15];
shape17 = close[16] - Open[16];
shape18 = close[17] - Open[17];
shape19 = close[18] - Open[18];
shape20 = close[19] - Open[19];
shape21 = close[20] - Open[20];
shape22 = close[21] - Open[21];
shape23 = close[22] - Open[22];
shape24 = close[23] - open[23];
shape25 = close[24] - Open[24];
shape26 = close[25] - Open[25];
shape27 = close[26] - open[26];
shape28 = close[27] - open[27];
shape29 = close[28] - Open[28];
shape30 = close[29] - Open[29];
shape31 = close[30] - open[30];

shape_ave = (shape1 + shape2 + shape3 + shape4 + shape5) / (5) ;
shape_ave_3 = (shape1 + shape2 + shape3) / (3) ;

shape_magn_ave = ( (absvalue (shape_ave[1]) ) + (absvalue (shape_ave[2]) ) + (absvalue (shape_ave[3]) ) + (absvalue (shape_ave[4]) ) + (absvalue (shape_ave[5]) )) / (5);

plot1 (shape_ave);
plot2 (shape_magn_ave);
plot3 (shape_magn_ave * -1);
plot4 (shape_ave * 2);
plot5 (shape_ave * -2);

shape_ave_31 = (shape1 + shape2 + shape3 + shape4 + shape5 + shape6 + shape7 + shape8 + shape9 + shape10 + shape11 + shape12 + shape13 + shape14 + shape15 + shape16 + shape17 +shape18 + shape19 + shape20 + shape21 + shape22 + shape23 + shape24 + shape25 + shape26 + shape27 + shape28 + shape29 + shape30 + shape31) / (31) ;

plot6 (shape_ave_3);
//plot2 (gas);
//plot3 (gas * -1);
//plot4 (juice * 2);
//plot5 (juice * -2)