#!/usr/bin/env wolframscript
(* ::Package:: *)

Off[General::munfl]

(* ::Input:: *)
data=Import["aux.csv","CSV"];


(* ::Input:: *)
\[Phi][T_,R_]:=(f[T+R]-f[T-R])/R/.f->Function[x, x A Exp[-((x-r0)/\[Sigma])^2]]/.{A->1,\[Sigma]->1,r0->0};


(* ::Input:: *)
\[CapitalOmega][r_]:= 1;
Layers={T->t,R->r}/.{Ri->30,Rt->0,S->30};

(*If[r<=Ri,1,If[r<Rt,1+((r-Ri)^5 (6 r^2+3 r Ri+Ri^2-5 (3 r+Ri) Rt+10 Rt^2))/((Ri-Rt)^5 (Ri-S)^2),]]*)
(*+(2R^2+S^2-\[Sqrt](4R^2 S^2+S^4))/(2\[Sqrt](R^2+1))*)
(*(r-Ri)/\[CapitalOmega][r]+Ri*)

(* ::Input:: *)
outStream=OpenWrite["exact_sol.txt"];


(* ::Input:: *)
For[i=1,i<=Length[data[[1]]],i++,
t=data[[1]][[i]];
WriteString[outStream,"\"Time = "<> ToString[FortranForm[N[t,16]]]<>"\n"];
For[j=1,j<=Length[data[[2]]],j++,
r=data[[2]][[j]];
If[r==0||r==30,Continue[],\[Psi]=(\[Phi][T,R]/\[CapitalOmega][r])/.{Ri->0,Rt->0,S->30}//.Layers];
WriteString[outStream,ToString[FortranForm[N[r,16]]]<>"\t"<>ToLowerCase[StringReplace[ToString[FortranForm[N[\[Psi],16]]]," "->""]]<>"\n"];
];
WriteString[outStream,"\n"];
]


(* ::Input:: *)
(*For[i=1,i<=Length[data[[1]]],i++,*)
(*t=data[[1]][[i]];*)
(*WriteString[outStream,"\"Time = "<> ToString[t]<>"\n"];*)
(*For[j=1,j<=Length[data[[2]]],j++,*)
(*r=data[[2]][[j]];*)
(*If[r==0,*)
(*Clear[r];*)
(*\[Psi]=Limit[\[Phi][T,R]//.Layers,r->0,Direction->"FromAbove"];*)
(*r=0,*)
(*If[r==30,*)
(*Clear[r];*)
(*\[Psi]=Limit[\[Phi][T,R]//.Layers,r->30,Direction->"FromBelow"];*)
(*r=30,*)
(*\[Psi]=\[Phi][T,R]//.Layers]];*)
(*WriteString[outStream,ToString[r]<>"\t"<>ToLowerCase[StringReplace[ToString[FortranForm[N[\[Psi],16]]]," "->""]]<>"\n"];*)
(*];*)
(*WriteString[outStream,"\n"];*)
(*]*)


(* ::Input:: *)
Close[outStream];