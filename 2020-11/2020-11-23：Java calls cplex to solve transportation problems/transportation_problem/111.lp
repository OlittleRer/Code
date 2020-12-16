\ENCODING=ISO-8859-1
\Problem name: ilog.cplex

Minimize
 obj: 250 x11 + 420 x12 + 380 x13 + 280 x14 + 1280 x21 + 990 x22 + 1440 x23
      + 1520 x24 + 1550 x31 + 1420 x32 + 1660 x33 + 1730 x34
Subject To
 c1: x11 + x12 + x13 + x14  = 45
 c2: x21 + x22 + x23 + x24  = 120
 c3: x31 + x32 + x33 + x34  = 95
 c4: x11 + x21 + x31  = 80
 c5: x12 + x22 + x32  = 78
 c6: x13 + x23 + x33  = 47
 c7: x14 + x24 + x34  = 55
End
