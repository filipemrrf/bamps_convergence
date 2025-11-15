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
WriteTime[outList_, t_] := Module[{i}, For[i=1, i<=Length[outList], i++,
    WriteString[outList[[i]], "\"Time = " <> ToString[FortranForm[N[t, 16]]] <> "\n"];
    ];
];
WriteField[out_, r_, field_] := WriteString[out, ToString[FortranForm[N[r,16]]] <> "\t" <> ToLowerCase[StringReplace[ToString[FortranForm[N[field, 16]]], " " -> ""]] <> "\n"];
WriteNewLine[outList_] := Module[{i}, For[i=1, i<=Length[outList], i++,
    WriteString[outList[[i]], "\n"];
    ];
];
CloseFiles[outList_] := Module[{i}, For[i=1, i<=Length[outList], i++,
    Close[outList[[i]]];
    ];
];

(* Defines the Minkowski metric in cartesian coordinates *)
gMindd = {{-1, 0, 0, 0}, 
          { 0, 1, 0, 0}, 
          { 0, 0, 1, 0}, 
          { 0, 0, 0, 1}};

(* Defines the Jacobian that changes coordinates from cartesian to spherical and vice versa *)
XCart = {T, X, Y, Z};
XSpher = {T, R, theta, phi} /. theta -> ArcCos[Z/R] /. R -> Sqrt[X^2 + Y^2 + Z^2] /. phi -> Sign[Y] ArcCos[X/Sqrt[X^2 + Y^2]];
Table[D[XSpher[[nu]], XCart[[mu]]], {mu, 1, 4}, {nu, 1, 4}] /. Derivative[1][Sign][Y] -> 0;
jCartdu = Assuming[{Element[X, Reals] && Element[Y, Reals] && Element[Z, Reals]}, % // FullSimplify];
jSpherdu = Inverse[jCartdu] // Simplify;

(* Changes the coordinates of the Minkowski metric to spherical *)
Table[Sum[jSpherdu[[mu, a]] jSpherdu[[nu, b]] gMindd[[a, b]], {a, 1, 4}, {b, 1, 4}], {mu, 1, 4}, {nu, 1, 4}] // Simplify;
gMinSphericaldd = % /. X^2 + Y^2 + Z^2 -> R^2 /. X^2 + Y^2 -> R^2 Sin[theta]^2 // Simplify;

(* Defines the functions needed in the hyp transformations *)
HypDef = {Omega -> Function[r, 1 - r^2/S^2], H -> Function[r, (4 r^7 S^2 - r^5 (8 + r^2) S^4 + r^3 (4 + 3 r^2) S^6)/((r^2 + S^2) (r^4 + S^4 + r^2 S^2 (-2 + S^2))^(3/2))], L -> Function[r, 1 + r^2/S^2], Xi -> Function[r, (r^12 - 2 r^10 S^2 - r^8 (1 + 13 r^2) S^4 + 4 r^6 (1 + 8 r^2 + 2 r^4) S^6 - r^4 (1 + 22 r^2 + 21 r^4 + r^6) S^8 + 2 r^2 (-1 + 3 r^4 + 2 r^6) S^10 + (1 + r^2)^3 S^12)/(r^4 + S^4 + r^2 S^2 (-2 + S^2))^3], Upsilon -> Function[r, -((4 r)/S^2)], iota -> Function[r, (4 r^6 - r^4 (8 + r^2) S^2 + r^2 (4 + 3 r^2) S^4)/(r^4 + S^4 + r^2 S^2 (-2 + S^2))^(3/2)]};
HypHOmegaLReturn = {Xi[r] -> ((1 - H[r]^2) L[r]^2)/Omega[r]^2, Upsilon[r] -> (Omega[r]^2 - L[r]^2)/r, iota[r] -> (H[r] L[r])/r};

(* Defines the Jacobian that changes coordinates from spherical to hyperboloidal spherical and the respective rules *)
XSpher = {T, R, theta, phi} /.T -> t + h[R] /. R -> r/Omega[r];
XHypSpher = {t, r, theta, phi};
$Assumptions = Element[r, Reals] && r >= 0 && r <= S;
Table[D[XSpher[[nu]], XHypSpher[[mu]]], {mu, 1, 4}, {nu, 1, 4}];
jHypdu = % /.Derivative[1][h][r/Omega[r]] -> H[r] /. Derivative[1][Omega][r] -> (Omega[r] - L[r])/r // Simplify;

(* Changes the coordinates of the metric to hyperboloidal *)
Table[Sum[jHypdu[[mu, a]] jHypdu[[nu, b]] gMinSphericaldd[[a, b]], {a, 1, 4}, {b, 1, 4}], {mu, 1, 4}, {nu, 1, 4}];
gHypdd = % /.R -> r/Omega[r] // Simplify;

(* Conformally rescales the metric *)
gHypConformaldd = Omega[r]^2 gHypdd;

(* Changes coordinates to Cartesian Hyperboloidal *)
Table[Sum[jCartdu[[mu, a]] jCartdu[[nu, b]] gHypConformaldd[[a, b]], {a, 1, 4}, {b, 1, 4}], {mu, 1, 4}, {nu, 1, 4}] /.{X -> x, Y -> y, Z -> z};
% /. Sin[theta]^2 -> (x^2 + y^2)/r^2 /.rToCart // Simplify;
% /. cartToR // Simplify;
gHypConformalCartdd = % /. (-1 + H[r]^2) -> (-Xi[r] Omega[r]^2)/L[r]^2 // Simplify;

Inverse[gHypConformalCartdd] // Simplify;
invgHypConformalCartuu = % /. cartToR // Simplify;

(* Calculates the Christoffel symbols *)
XHypCart = {t, x, y, z};
Table[1/2 Sum[ReplaceRepeated[Flatten[{HypHOmegaLReturn, rToCart}]][invgHypConformalCartuu][[a, d]] 
    (D[ReplaceRepeated[Flatten[{HypHOmegaLReturn, rToCart}]][invgHypConformalCartuu][[c, d]], XHypCart[[b]]] +
     D[ReplaceRepeated[Flatten[{HypHOmegaLReturn, rToCart}]][invgHypConformalCartuu][[b, d]], XHypCart[[c]]] -
     D[ReplaceRepeated[Flatten[{HypHOmegaLReturn, rToCart}]][invgHypConformalCartuu][[b, c]], XHypCart[[d]]]), {d, 1, 4}]
    {a, 1, 4}, {b, 1, 4}, {c, 1, 4}] // Simplify;
% /. cartToR // Simplify;
% /. (-1 + H[r]^2) -> (-\[CapitalXi][r] \[CapitalOmega][r]^2)/L[r]^2;
% // Expand;
GammaHypConformalCartudd = % /. Omega[r]^2 -> r Upsilon[r] + L[r]^2 // Simplify;

(* Calculates the 3+1 quantities *)
gammadd = Table[gHypConformalCartdd[[i, j]], {i, 2, 4}, {j, 2, 4}];
Inverse[gammadd] // Simplify;
invgammauu = % /. cartToR // Simplify;

1/Sqrt[-invgHypConformalCartuu[[1, 1]]] // Simplify;
% /. HypHOmegaLReturn // Simplify;
alpha = % /. (1 - H[r]^2) -> (Xi[r] Omega[r]^2)/L[r]^2 // Simplify;

betad = Table[gHypConformalCartdd[[1, i]], {i, 2, 4}];
Table[Sum[invgammauu[[i, j]] betad[[j]], {j, 1, 3}], {i, 1, 3}] // Simplify;
betau = % /. cartToR // Simplify;
Table[D[ReplaceAll[rToCart][betau[[j]]], XHypCart[[i]]], {i, 2, 4}, {j, 1, 3}] // Simplify;
% /. cartToR /. Sqrt[x^2 + y^2 + z^2] -> r // Simplify;
% // Expand;
dbetau = % /. H[r] L[r] -> r iota[r] // FullSimplify;

nd = {-alpha, 0, 0, 0};
nu = Flatten[{1/alpha, -betau/alpha}] // Simplify;
Table[Sum[invgammauu[[i, j]] D[ReplaceAll[rToCart][Log[alpha]], XHypCart[[j+1]]], {j, 1, 3}], {i, 1, 3}] // Simplify;
accel = % /. rToCart // Simplify;

extrinsicK = Table[(1/(2 alpha) (Sum[gammadd[[j, k]] (D[betau[[k]] \. rToCart, XHypCart[[i+1]]] + Sum[GammaHypConformalCartudd[[k, i, l]] betau[[l]], {l, 1, 3}]), {k, 1, 3}] + 
        Sum[gammadd[[i, k]] (D[betau[[k]] \. rToCart, XHypCart[[j+1]]] + Sum[GammaHypConformalCartudd[[k, j, l]] betau[[l]], {l, 1, 3}]), {k, 1, 3}])), {i, 1, 3}, {j, 1, 3}] // Simplify;

1/Omega[Sqrt[x^2 + y^2 + z^2]] (Sum[invgHypConformalCartuu[[a, b]] (D[Omega[Sqrt[x^2 + y^2 + z^2]], XHypCart[[a]], XHypCart[[b]]] - 
    Sum[GammaHypConformalCartudd[[c, a, b]] D[Omega[Sqrt[x^2 + y^2 + z^2]], XHypCart[[c]]], {c, 1, 4}]), {a, 1, 4}, {b, 1, 4}]) /. Omega -> Function[r, 1 - r^2/S^2];
Assuming[S > 0 && Ri >= 0 && r >= 0 && r >= Ri && r <= S, % // Simplify];
Assuming[S > 0 && Ri >= 0 && r >= 0 && r >= Ri && r <= S, % /. cartToR // Simplify];
Assuming[S > 0 && Ri >= 0 && r >= 0 && r >= Ri && r <= S, % // Together];
Assuming[S > 0 && Ri >= 0 && r >= 0 && r >= Ri && r <= S, % // Simplify];
Assuming[S > 0 && Ri >= 0 && r >= 0 && r >= Ri && r <= S, % /. cartToR // Simplify];
Assuming[S > 0 && Ri >= 0 && r >= 0 && r >= Ri && r <= S, oomboxom = % /. HypDef // Simplify];

1/Omega[Sqrt[x^2 + y^2 + z^2]]^2 (Sum[invgHypConformalCartuu[[a, b]] D[Omega[Sqrt[x^2 + y^2 + z^2]], XHypCart[[a]]] D[Omega[Sqrt[x^2 + y^2 + z^2]], XHypCart[[b]]], {a, 1, 4}, {b, 1, 4}]) /. \[CapitalOmega] -> Function[r, 1 - r^2/S^2];
Assuming[S > 0 && Ri >= 0 && r >= 0 && r >= Ri, % // Simplify];
Assuming[S > 0 && Ri >= 0 && r >= 0 && r >= Ri, % /. (x^2 + y^2 + z^2) -> r^2 // Simplify];
Assuming[S > 0 && Ri >= 0 && r >= 0 && r >= Ri, % /. HypDef // Simplify];
Assuming[S > 0 && Ri >= 0 && r >= 0 && r >= Ri, oom2dom2 = % /. (x^2 + y^2 + z^2) -> r^2 // Simplify];

(* Defines the exact solution *)
S = 30;
A = 1;
r0 = 0;
sigma = 1;
f[r_] = r * A * Exp[-((r - r0)/sigma)^2]
exact[T_, R_] := (f[T + R] - f[T - R])/R;
Psi[t_, r_] := exact[t + (2 * (r/Omega[r])^2 + S^2 - Sqrt[4 * (r/Omega[r])^2 * S^2 + S^4])/(2 * Sqrt[(r/Omega[r])^2 + 1]), r/Omega[r]];
psi = Psi[t, r]/Omega[r] /. HypDef // Simplify;

(* Defines the reduction constraints *)
aux = Sum[-nu[[a]] * D[psi /.rToCart, xHypCart[[a]]], {a,1,4}] /. HypDef;
pi = aux /.cartToR;

aux = Table[D[psi /.rToCart, xHypCart[[a]]], {a,2,4}] /. HypDef;
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

outGammaxx = OpenWrite["exact.stat.gammaxx"];
outGammaxy = OpenWrite["exact.stat.gammaxy"];
outGammaxz = OpenWrite["exact.stat.gammaxz"];
outGammayy = OpenWrite["exact.stat.gammayy"];
outGammayz = OpenWrite["exact.stat.gammayz"];
outGammazz = OpenWrite["exact.stat.gammazz"];

outChristgammaxxx = OpenWrite["exact.stat.Christgammaxxx"];
outChristgammaxxy = OpenWrite["exact.stat.Christgammaxxy"];
outChristgammaxxz = OpenWrite["exact.stat.Christgammaxxz"];
outChristgammaxyy = OpenWrite["exact.stat.Christgammaxyy"];
outChristgammaxyz = OpenWrite["exact.stat.Christgammaxyz"];
outChristgammaxzz = OpenWrite["exact.stat.Christgammaxzz"];
outChristgammayxx = OpenWrite["exact.stat.Christgammayxx"];
outChristgammayxy = OpenWrite["exact.stat.Christgammayxy"];
outChristgammayxz = OpenWrite["exact.stat.Christgammayxz"];
outChristgammayyy = OpenWrite["exact.stat.Christgammayyy"];
outChristgammayyz = OpenWrite["exact.stat.Christgammayyz"];
outChristgammayzz = OpenWrite["exact.stat.Christgammayzz"];
outChristgammazxx = OpenWrite["exact.stat.Christgammazxx"];
outChristgammazxy = OpenWrite["exact.stat.Christgammazxy"];
outChristgammazxz = OpenWrite["exact.stat.Christgammazxz"];
outChristgammazyy = OpenWrite["exact.stat.Christgammazyy"];
outChristgammazyz = OpenWrite["exact.stat.Christgammazyz"];
outChristgammazzz = OpenWrite["exact.stat.Christgammazzz"];

outAccelx = OpenWrite["exact.stat.accelx"];
outAccely = OpenWrite["exact.stat.accely"];
outAccelz = OpenWrite["exact.stat.accelz"];

outDbetaxx = OpenWrite["exact.stat.dbetaxx"];
outDbetaxy = OpenWrite["exact.stat.dbetaxy"];
outDbetaxz = OpenWrite["exact.stat.dbetaxz"];
outDbetayx = OpenWrite["exact.stat.dbetayx"];
outDbetayy = OpenWrite["exact.stat.dbetayy"];
outDbetayz = OpenWrite["exact.stat.dbetayz"];
outDbetazx = OpenWrite["exact.stat.dbetazx"];
outDbetazy = OpenWrite["exact.stat.dbetazy"];
outDbetazz = OpenWrite["exact.stat.dbetazz"];

outOomboxom = OpenWrite["exact.stat.oomboxom"];
outOom2dom2 = OpenWrite["exact.stat.oom2dom2"];

outList = {outPsi, outPi, outPhix, outPhiy, outPhiz, outPsiRHS, outPiRHS, outPhixRHS, outPhiyRHS, outPhizRHS, outOmega, outAlpha, outBetax, outBetay, outBetaz, outGammaxx, outGammaxy, outGammaxz, outGammayy, outGammayz, outGammazz, outChristgammaxxx, outChristgammaxxy, outChristgammaxxz, outChristgammaxyy, outChristgammaxyz, outChristgammaxzz, outChristgammayxx, outChristgammayxy, outChristgammayxz, outChristgammayyy, outChristgammayyz, outChristgammayzz, outChristgammazxx, outChristgammazxy, outChristgammazxz, outChristgammazyy, outChristgammazyz, outChristgammazzz, outAccelx, outAccely, outAccelz, outDbetaxx, outDbetaxy, outDbetaxz, outDbetayx, outDbetayy, outDbetayz, outDbetazx, outDbetazy, outDbetazz, outOomboxom, outOom2dom2}

For[i=1, i<=Length[data[[1]]], i++,
    t = data[[1]][[i]];

    WriteTime[outList, t];
    
    For[j=1, j<=Length[data[[2]]], j++,
        r = Abs[data[[2]][[j]]];
        If[r==0||r==30, Continue[]];

        WriteField[outPsi, r, psi];
        WriteField[outPi, r, pi /. cartoon];
        WriteField[outPhix, r, phi[[1]] /. cartoon];
        WriteField[outPhiy, r, phi[[2]] /. cartoon];
        WriteField[outPhiz, r, phi[[3]] /. cartoon];

        WriteField[outPsiRHS, r, psiRHS];
        WriteField[outPiRHS, r, piRHS /. cartoon];
        WriteField[outPhixRHS, r, phiRHS[[1]] /. cartoon];
        WriteField[outPhiyRHS, r, phiRHS[[2]] /. cartoon];
        WriteField[outPhizRHS, r, phiRHS[[3]] /. cartoon];

        WriteField[outOmega, r, Omega[r] /. HypDef];
        WriteField[outAlpha, r, alpha /. HypDef];
        WriteField[outBetax, r, betau[[1]] /. HypDef /. cartoon];
        WriteField[outBetay, r, betau[[2]] /. HypDef /. cartoon];
        WriteField[outBetaz, r, betau[[3]]/. HypDef /. cartoon];

        WriteField[outGammaxx, r, gammadd[[1,1]] /. HypDef /. cartoon];
        WriteField[outGammaxy, r, gammadd[[1,2]] /. HypDef /. cartoon];
        WriteField[outGammaxz, r, gammadd[[1,3]] /. HypDef /. cartoon];
        WriteField[outGammayy, r, gammadd[[2,2]] /. HypDef /. cartoon];
        WriteField[outGammayz, r, gammadd[[2,3]] /. HypDef /. cartoon];
        WriteField[outGammazz, r, gammadd[[3,3]] /. HypDef /. cartoon];

        WriteField[outAccelx, r, accelu[[1]] /. HypDef /. cartoon];
        WriteField[outAccely, r, accelu[[2]] /. HypDef /. cartoon];
        WriteField[outAccelz, r, accelu[[3]] /. HypDef /. cartoon];
    ];

    WriteNewLine[outList];
]

CloseFiles[outList];