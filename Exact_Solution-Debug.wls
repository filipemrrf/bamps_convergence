#!/usr/bin/env wolframscript
Off[General::munfl]

(* Defines the hyp cartesian coordinates *)
xHypCart = {t, x, y, z};

(* Defines shorthands to transformations between cartesian and spherical coordinates *)
rToCart = {r->Sqrt[x^2+y^2+z^2]};
cartToR = {Sqrt[x^2+y^2+z^2]->r};

(* Defines a reduction to the x axis *)
cartoon = {x->r, y->0, z->0};

(* Defines a shorthands for writing to files *)
WriteTime[out_, t_] := WriteString[out, "\"Time = " <> ToString[FortranForm[N[t, 16]]] <> "\n"];
WriteField[out_, r_, field_] := WriteString[out, ToString[FortranForm[N[r,16]]] <> "\t" <> ToLowerCase[StringReplace[ToString[FortranForm[N[field, 16]]], " " -> ""]] <> "\n"];

(* Defines the functions needed in the hyp transformations *)
S = 30;
Omega[r_] := 1 - r^2/S^2;
H[r_] := (4 r^7 S^2 - r^5 (8 + r^2) S^4 + r^3 (4 + 3 r^2) S^6)/((r^2 + S^2) (r^4 + S^4 + r^2 S^2 (-2 + S^2))^(3/2));
L[r_] := 1 + r^2/S^2;
Xi[r_] := (r^12 - 2 r^10 S^2 - r^8 (1 + 13 r^2) S^4 + 4 r^6 (1 + 8 r^2 + 2 r^4) S^6 - r^4 (1 + 22 r^2 + 21 r^4 + r^6) S^8 + 2 r^2 (-1 + 3 r^4 + 2 r^6) S^10 + (1 + r^2)^3 S^12)/(r^4 + S^4 + r^2 S^2 (-2 + S^2))^3;
Upsilon[r_] := -((4 r)/S^2);
iota[r_] := (4 r^6 - r^4 (8 + r^2) S^2 + r^2 (4 + 3 r^2) S^4)/(r^4 + S^4 + r^2 S^2 (-2 + S^2))^(3/2);

(* Defines the 3+1 variables *)
alpha = 1/Sqrt[Xi[r]/L[r]^2];
betau = {-((x * H[r] * L[r])/(r * Xi[r])), -((y * H[r] * L[r])/(r * Xi[r])), -((z * H[r] * L[r])/(r * Xi[r]))};
nu = Flatten[{1/alpha, -betau/alpha}] //Simplify;

(* Defines the exact solution *)
A = 1;
r0 = 0;
sigma = 1;
f[r_] = r * A * Exp[-((r - r0)/sigma)^2]
exact[T_, R_] := (f[T + R] - f[T - R])/R;
Psi[t_, r_] := exact[t + (2 * (r/Omega[r])^2 + S^2 - Sqrt[4 * (r/Omega[r])^2 * S^2 + S^4])/(2 * Sqrt[(r/Omega[r])^2 + 1]), r/Omega[r]];
psi = Psi[t, r]/Omega[r];

(* Defines the reduction constraints *)
aux = Sum[-nu[[a]] * D[psi /.rToCart, xHypCart[[a]]], {a,1,4}];
pi = aux /.cartToR;

aux = Table[D[psi /.rToCart, xHypCart[[a]]], {a,2,4}];
phi = aux /.cartToR;

(* Defines the exact RHS *)
psiRHS = D[psi, t]
piRHS = D[pi, t]
phiRHS = Table[D[phi[[i]], t], {i,1,3}]

(* Reads what output is needed *)
data=Import["aux.csv", "Data", "HeaderLines" -> 0];

(* Outputs the exact solution for all the evolved fields *)
outPsi = OpenWrite["exact.u.psi"];
outPi = OpenWrite["exact.u.pi"];
outPhix = OpenWrite["exact.u.phix"];
outPhiy = OpenWrite["exact.u.phiy"];
outPhiz = OpenWrite["exact.u.phiz"];

(* Outputs the RHS *)
outPsiRHS = OpenWrite["exact.ru.psi"];
outPiRHS = OpenWrite["exact.ru.pi"];
outPhixRHS = OpenWrite["exact.ru.phix"];
outPhiyRHS = OpenWrite["exact.ru.phiy"];
outPhizRHS = OpenWrite["exact.ru.phiz"];

(* Outputs the ustat variables *)
outOmega = OpenWrite["exact.stat.Omega"];
outAlpha = OpenWrite["exact.stat.alpha"];
outBetax = OpenWrite["exact.stat.betax"];
outBetay = OpenWrite["exact.stat.betay"];
outBetaz = OpenWrite["exact.stat.betaz"];

For[i=1, i<=Length[data[[1]]], i++,
    t = data[[1]][[i]];

    WriteTime[outPsi, t];
    WriteTime[outPi, t];
    WriteTime[outPhix, t];
    WriteTime[outPhiy, t];
    WriteTime[outPhiz, t];

    WriteTime[outPsiRHS, t];
    WriteTime[outPiRHS, t];
    WriteTime[outPhixRHS, t];
    WriteTime[outPhiyRHS, t];
    WriteTime[outPhizRHS, t];

    WriteTime[outOmega, t];
    WriteTime[outAlpha, t];
    WriteTime[outBetax, t];
    WriteTime[outBetay, t];
    WriteTime[outBetaz, t];
    
    For[j=1, j<=Length[data[[2]]], j++,
        r = Abs[data[[2]][[j]]];
        If[r==0||r==30, Continue[]];

        WriteField[outPsi, r, psi];
        WriteField[outPi, r, pi/.cartoon];
        WriteField[outPhix, r, phi[[1]]/.cartoon];
        WriteField[outPhiy, r, phi[[2]]/.cartoon];
        WriteField[outPhiz, r, phi[[3]]/.cartoon];

        WriteField[outPsiRHS, r, psiRHS];
        WriteField[outPiRHS, r, piRHS/.cartoon];
        WriteField[outPhixRHS, r, phiRHS[[1]]/.cartoon];
        WriteField[outPhiyRHS, r, phiRHS[[2]]/.cartoon];
        WriteField[outPhizRHS, r, phiRHS[[3]]/.cartoon];

        WriteField[outOmega, r, Omega[r]];
        WriteField[outAlpha, r, alpha];
        WriteField[outBetax, r, betau[[1]]/.cartoon];
        WriteField[outBetay, r, betau[[2]]/.cartoon];
        WriteField[outBetaz, r, betau[[3]]/.cartoon];
    ];

    WriteString[outPsi, "\n"];
    WriteString[outPi, "\n"];
    WriteString[outPhix, "\n"];
    WriteString[outPhiy, "\n"];
    WriteString[outPhiz, "\n"];

    WriteString[outPsiRHS,"\n"];
    WriteString[outPiRHS,"\n"];
    WriteString[outPhixRHS,"\n"];
    WriteString[outPhiyRHS,"\n"];
    WriteString[outPhizRHS,"\n"];

    WriteString[outOmega,"\n"];
    WriteString[outAlpha,"\n"];
    WriteString[outBetax,"\n"];
    WriteString[outBetay,"\n"];
    WriteString[outBetaz,"\n"];
]

Close[outPsi]
Close[outPi]
Close[outPhix]
Close[outPhiy]
Close[outPhiz]

Close[outPsiRHS]
Close[outPiRHS]
Close[outPhixRHS]
Close[outPhiyRHS]
Close[outPhizRHS]

Close[outOmega]
Close[outAlpha]
Close[outBetax]
Close[outBetay]
Close[outBetaz]