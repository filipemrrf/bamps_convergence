#!/usr/bin/env wolframscript
Off[General::munfl]

(* Defines the functions needed in the hyp transformations *)
S = 30;
Omega[r_] := 1 - r^2/S^2;

(* Defines the exact solution *)
A = 1;
r0 = 0;
sigma = 1;
f[r_] = r * A * Exp[-((r - r0)/sigma)^2]
exact[T_, R_] := (f[T + R] - f[T - R])/R;
Psi[t_, r_] := exact[t + (2 * (r/Omega[r])^2 + S^2 - Sqrt[4 * (r/Omega[r])^2 * S^2 + S^4])/(2 * Sqrt[(r/Omega[r])^2 + 1]), r/Omega[r]];
psi = Psi[t, r]/Omega[r];

(* Reads what output is needed *)
data = Import["aux.csv", "Data", "HeaderLines" -> 0];

(* Outputs the exact solution for all the evolved fields *)
outPsi = OpenWrite["exact.u.psi"];

For[i=1, i<=Length[data[[1]]], i++,
    t = data[[1]][[i]];
    WriteString[outPsi, "\"Time = " <> ToString[FortranForm[N[t, 16]]] <> "\n"];

    For[j=1, j<=Length[data[[2]]], j++,
        r = Abs[data[[2]][[j]]];

        If[r==0||r==30, Continue[]];
        WriteString[outPsi, ToString[FortranForm[N[r, 16]]] <> "\t" <> ToLowerCase[StringReplace[ToString[FortranForm[N[psi, 16]]], " " -> ""]] <> "\n"];
    ];
    WriteString[outPsi, "\n"];
]

Close[outPsi]