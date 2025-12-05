## Page 1


| High-Per for m an ce Comput in g Center Stuttgart Solv in g the 2d Po is son Equ at ion us in g the FEM and a CG Method |
| --- |
| |


---

## Page 2

F in ite Element Method 

---

## Page 3


| Str on g F or mul at ion of the Po is son Equ at ion Goal: F in d the unknown function u (e.g., temper at ure, potential) on adomainΩ, givena source f (e.g., heat source). Th is is descri be d by the str on g for m. F in du:Ω→R such that −∆u=f ∈Ω (Po is son’s Equ at ion) (1) u=0 ∈∂Ω (Boundary C on d it ion) (2) Laplaceopera to r∆: ∂2u ∂2u ∆u= + (3) ∂ x2 ∂ y2 Problem: Requiresu to be twice-d if ferentiable. Th is is to orestrictive and d if ficult to w or k w it h comput at i on ally. Not at i on for the L2-in nerproduct: (cid:90) (f, g):= f ·gdx (4) Ω [1] |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e3 |


---

## Page 4


| Weak F or mul at ion of the Po is son Equ at ion I Idea: We„weaken“therequirement from C2 to C1 by test in g the equ at i on in an in tegralsense. Def in e function space V f or both the soluti on u and„test function s“v: V :=H 01(Ω), (5) Th is space V c on ta in sall function s that are on etime (weakly) d if ferentiable and arezeroon the boundary ∂Ω. Multiply the PDE by atest function v ∈V and in tegr at eoverΩ: (−∆u, v)=(f, v) ∀v ∈V (6) Apply in tegr at i on by parts (Green’s the orem) to the left-h and side to moveaderiv at ive from u on to v: (cid:90) (∇ u,∇ v)− ∂ nuφds =(f,φ) ∀φ∈V (7) ∂Ω [1] |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e4 |


---

## Page 5


| Weak F or mul at ion of the Po is son Equ at ion II S in ceourtest function sv ∈V are0on the boundary (v =0on ∂Ω), the boundary in tegralvan is hes. Th is gives the weak for mul at ion: F in du∈V suchthat (∇ u,∇ v)=(f, v) ∀v ∈V (8) Th is is of tenwr it tenabstractly as a (u, v)=L (v), where: • a (u, v):=(∇ u,∇ v) is the bil in ear for m (h and lesst if fness). • L (v):=(f, v) is the l in ear for m (h and les the source/load). [1] |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e5 |


---

## Page 6


| Mesh in g and Function Space I Problem: Thespace V =H1 is in fin it e-dimensi on al. 0 Solution: Weapproxim at e V w it haf in ite-dimensi on alsubspace V h⊂V. Step1: Mesh in g Wed is cretize the domainΩin to a f in ite num be r of simpleshapes (elements), liketri an gles. Thecollecti on of the se elementsis the mesh, Th. Theparameterhrepresents the meshsize (e.g., maxtri an glewidth). [2,1] |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e6 |


---

## Page 7


| Mesh in g and Function Space II 1.0 0.8 Step2: Def in e V h Wedef in e V h as the spaceof function s that are: 0.6 • C on t in uousacross the wholedomainΩ. y • as implepolynomial (e.g., l in ear) on each tri an gle 0.4 K∈Th. • Stillzeroon the boundary ∂Ω. 0.2 Th is is the space of c on t in uous, piecew is e-l in ear functi on s. 0.0 0.0 0.2 0.4 0.6 0.8 1.0 x Figure: Amesh Th of the un it square. [2,1] |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e7 |

| | | | | | | | N on e | | | | N on e | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| | | | | | | | N on e | | | | N on e | | | | | |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e | N on e |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| | | | | | | | N on e | | | | N on e | | | | | |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| N on e | | | | | | | N on e | | | | N on e | | | | | |
| | | N on e | N on e | | N on e | N on e | | N on e | N on e | N on e | | N on e | N on e | | N on e | N on e |


---

## Page 8


| B as is Functi on s (P1 Elements) I Howdowebuildab as is for V h? Weuselocalb as is function s (orshape function s)φ i as soci at edwi the achnode N i of the mesh. F or P1(piecew is e-l in ear) elements,φ i h as akeyproperty: • φ i is1at it s„own“node N i. • φ is0atallo the rnodes N (j (cid:54)=i). i j • φ i is l in earon each tri an gle. Th is is the„h at function“. [2,1] |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e8 |


---

## Page 9


| B as is Functi on s (P1 Elements) II (x3, y3) Area Co or din at es 3 On as in gletri an gle w it h nodes (x1, y1),(x2, y2),(x3, y3), theseshape function sare identicalto the areaco or din at es L i: x =L1x1+L2x2+L3x3 (9) 1 2 y =L1y1+L2y2+L3y3 (10) (x1, y1) (x2, y2) 1=L1+L2+L3 (11) Figure: As in glel in eartri an gularelement. [2,1] |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e9 |


---

## Page 10


| B as is Functi on s (P1 Elements) III Explicit For mulas Theareaco or din at es L arel in ear function sof (x, y): i a1+b1x+c1y L1= , a1=x2y3−x3y2, b1=y2−y3, c1=x3−x2 (12) 2A a2+b2x+c2y L2= , a2=x3y1−x1y3, b2=y3−y1, c2=x1−x3 (13) 2A a3+b3x+c3y L3= , a3=x1y2−x2y1, b3=y1−y2, c3=x2−x1 (14) 2A Local Shape Function s On this l in eartri an gleelement, thethreelocalshape function sarejust: φ1(x, y)=L1 φ2(x, y)=L2 φ3(x, y)=L3 (15) [2,1] |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e10 |


---

## Page 11


| Gradients & D is crete F or m I Gradients of Shape Function s S in ce the shape function sφ i =L i arel in ear, theirgradientsarec on stan to n each element: (cid:34)∂φi (cid:35) ∇φ i = ∂∂ φx i (16) ∂ y ∂φ1 y2−y3 ∂φ1 x3−x2 = (17) = (20) ∂ x 2A ∂ y 2A ∂φ2 y3−y1 ∂φ2 x1−x3 = (18) = (21) ∂ x 2A ∂ y 2A ∂φ3 y1−y2 ∂φ3 x2−x1 = (19) = (22) ∂ x 2A ∂ y 2A [2,1] |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e11 |


---

## Page 12


| Gradients & D is crete F or m II The Galerk in Problem (D is crete For m) Wenowsolve the weak for mon the f in ite-dimensi on alspace V h: F in du h∈V h suchthat (∇ u h,∇ v h)=(f, v h) ∀v h∈V h (23) As the meshsizeh→0, thed is cretesoluti on u c on vergesto the truesoluti on u. h [2,1] |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e12 |


---

## Page 13


| C on vert in g in to a L in ear Equ at ion System I Any function u h in ourspace V h c an bewr it ten as al in earcombin at i on of it sb as is function sφ j: n (cid:88) u h (x, y)= u jφ j (x, y) (24) j=1 Here, nis the to talnum be r of nodesin the mesh. Becauseφ j (N i)=δ ij, the unknown coefficientsu j aresimplythe unknownvaluesof the soluti on at the nodes: u j =u h (N j). |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e13 |


---

## Page 14


| C on vert in g in to a L in ear Equ at ion System II Subst it utethis„ans at z“in to the Galerk in problem: (∇ u h,∇φ h)=(f,φ h) ∀φ h∈V h (25)     n (cid:88) ∇ u jφ j,∇φ h=(f,φ h) ∀φ h∈V h (26) j=1 n (cid:88) (cid:0) (cid:1) u j ∇φ j,∇φ h =(f,φ h) ∀φ h∈V h (27) j=1 This must hold for all φ h∈V h. It is sufficient to test it aga in st each bas is functionφ i (f or i =1,..., n): n (cid:88) (cid:0) (cid:1) u j ∇φ j,∇φ i =(f,φ i) ∀i ∈{1,..., n} (28) j=1 |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e14 |


---

## Page 15


| C on vert in g in to a L in ear Equ at ion System III Th is is al in earsystemof equ at ion s Au=F!      (∇φ1,∇φ1) ... (∇φn,∇φ1) u1 (f,φ1)   . . ... . .     . . .  =  . .   (29)  . .  .  (∇φ1,∇φn) ... (∇φn,∇φn) un (f,φn) (cid:124) (cid:123)(cid:122) (cid:125)(cid:124)(cid:123)(cid:122)(cid:125) (cid:124) (cid:123)(cid:122) (cid:125) St if fnessm at rix A u Loadvec to r F Theentriesare: (cid:90) (cid:0) (cid:1) A ij = ∇φ j,∇φ i := ∇φ j·∇φ i dx (30) Ω (cid:90) F i =(f,φ i):= fφ i dx (31) Ω Our goal is to solve this systemfor the unknownvec to r of nodalvaluesu. |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e15 |


---

## Page 16


| as sembl in g and Solv in g the System I Alg or ithm1: Global As sembly in put : Mesh Th, Sourcef 1 In it ialize A=0(sparsen×nm at rix) 2 In it ialize F=0(n×1vec to r) 3 for each elemente in mesh Thdo In it ialize Ae=0(3×3localm at rix) 4 In it ialize Fe=0(3×1localvec to r) 5 6 Letφ1,φ2,φ3be the localshape function s on e 7 8 f or i F= ie1 =to (cid:82) e3 fd φo idx 19 f or j A= ij1 =to (cid:82)3 e ∇ do 0 e φj·∇φidx 11 end 12 end 13 f or i=1to3do 14 F [gi]+=F ie 15 f or j=1to3do A [gi, gj]+=Ae 16 ij 17 end 18 end 19 end 20 Apply Dirichlet BC (A, F) 21 return A, F |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e16 |


---

## Page 17


| as sembl in g and Solv in g the System II 0 20 Structureof the M at rix A 40 wor • A is alarge, sparsem at rix. • Theentry A ij is non-zero on ly if nodesi andj share 60 anelement. • Itis also symmetric (A ij =A ji) andpos it ive-def in ite. 80 100 0 20 40 60 80 100 column Figure: Spars it yp at tern of A. |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e17 |


---

## Page 18


| as sembl in g and Solv in g the System III Solv in g the System Because A is sparse, symmetric, andpos it ive-def in ite, wedon’tusedirectsolvers (like A−1). Weuseefficient iter at ivesolverslike the C on jug at e Gradient (CG) Method. Alg or ithm2: C on jug at e Gradient Method in put : M at rix A, vec to rb, in it ialguessx0 Output: Soluti on x 1 r0=b−Ax0 2 p0=r0 3 f or k=0to m (cid:124) axit-1 (cid:124) do 4 αk=(r krk)/(p k Apk) 5 xk+1=xk+αkpk 6 rk+1=rk−αk Apk 7 if (cid:107) rk+1(cid:107)2<=to l the n 8 retu (cid:124) rn xk+1 (cid:124) 9 βk=(r k+1rk+1)/(r krk) 10 pk+1=rk+1+βkpk 11 end 12 returnxk+1 |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e18 |


---

## Page 19


| Solution of the Po is son Equ at ion Aftersolv in g Au=F for the vec to ru, wehave the valueu j at each node. Wecan the nrec on struct the fullsolution u h=(cid:80) u jφ j f or v is ualiz at ion. 1.00 0.06 0.75 0.04 0.50 y u 0.25 0.02 0.00 0.00 0.0 0.5 1.0 x Figure: Thecomputedd is cretesoluti on u f or a source f =1on the un it square. h |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e19 |

| |
| --- |
| |

| |
| --- |
| |


---

## Page 20

Bibliography 

---

## Page 21


| Bibliography I [1] TWick. Numerical Method s for Partial D if ferential Equ at ion s.en. H an nover: in st it uti on elles Reposi to riumder Leibniz Universität H an nover,2020. DOI:10.15488/9248. [2] OCZienkiewicz and RLTaylor. Thef in ite element method. Volume1: Theb as is.5thed. Ox for d: Butterw or th-He in em an n,2002.689pp. URL: https://www.meil.pw.edu.pl/c on tent/download/58297/306302/file/FEM_Zienkiewicz%20Vol1.pdf (v is itedon 10/28/2025). |
| --- |
| Novem be r24,2025 Solv in gthe2d Po is son Equ at ion us in g the FEM and a CGMethod Se it e21 |

