import v16_split as M
for case,xlo,Ls in (('ts35',1.6,(9.0,9.2,9.5)),('kerr35',1.3,(4.0,4.3,4.5))):
    M.XLO=xlo; WL=M.wfun_L(case)
    for L in Ls: print(case, L, M.wmax(WL(-L)))
