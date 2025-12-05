# Solving the 2d Poisson Equation using the FEM and a CG Method

---

## Page 1

oo —— SSS S— ‘omputing Cen} — ——S- = ~ = Solving the 2d Poisson Equa sing= and=a =



---

## Page 2

Finite Element Method



---

## Page 3

Strong Formulation of the Poisson Equation H LR I[s Goal: Find the unknown function u (e.g., temperature, potential) on a domain Q, given a source F (e.g., heat source) This is described by the strong form. Find u : 2+ R such that —Au=f €Q (Poisson's Equation) (@) u=0 €€@2 (Boundary Condition) (2) Laplace operator A: Au= eu + ou 3 = a2 t ay? ) Problem: Requires u to be twice-differentiable. This is too restrictive and difficult to work with computationally. Notation for the L?-inner product: (= [ F-aax (a) 2 i November 24, 2025 Soling the 24 Poison Equation sng the FEM and a CG Method sei



---

## Page 4

Weak Formulation of the Poisson Equation I H LR I[s Idea: We ,weaken" the requirement from C? to C+ by testing the equation in an integral sense. Define function space V for both the solution u and ,test functions" v: V = AA(Q), (5) This space V contains all functions that are one time (weakly) differentiable and are zero on the boundary 8Q. Multiply the PDE by a test function v € V and integrate over 2 (-Au,v) =(f.v) WweV (6) Apply integration by parts (Green's theorem) to the left-hand side to move a derivative from u onto v: (wavy) f Anup ds = (f,¢) VPEV (7) on i November 24, 2025 Song the 2d Poisson Equation using the FEM anda CG Method site 4



---

## Page 5

Weak Formulation of the Poisson Equation II H LR I[s Since our test functions v € V are 0 on the boundary (v = 0 on 82), the boundary integral vanishes. This gives the weak formulation: Find u € V such that (Vu, Vv) =(f.v) WweV (8)



This is often written abstractly as a(u, v) = L(v), where:



© a(u, v) := (Wu, Vv) is the bilinear form (handles stiffness)



© L(v) :=(F.v) is the linear form (handles the source/load). ry November 24,2025 Sling the 24 Poison Equation using the FEM and 3 C6 Method sei 5



---

## Page 6

Meshing and Function Space I H LR I[s Problem: The space V = H4 is infinite-dimensional



Solution: We approximate V with a finite-dimensional subspace Vi) C V



Step 1: Meshing



We discretize the domain @ into a finite number of simple shapes (elements), like triangles. The collection of these elements is the mesh, Tj. The parameter h represents the mesh size (e.g., max triangle width)



Ral



November 24, 2025 Song the 2d Poisson Equation using the FEM anda CG Method seit 6



---

## Page 7

Meshing and Function Space II H LR I[s iad 77474174 VA VAVAPAVAVAVAVAVAPAI VAVAVAVAVAVAVAVAVAVAVAVAVAVAI (r¥-] AVA VAVAVAVAVAVAVAVAVAVAVAVAI . IVAVAVAVAVAVAVAVAVAVAVAVAVAVA\ Step 2: Define Vi, AVAVAVAVAVAAVAVAAVAVAVAYA We define Vj as the space of functions that are Od 5 VAVAVAVAVAVAVAVAVAVAVAVAVAVAI IVAVAVAVAVAVAVAVAVAVAVAVAVAVA\ * Continuous across the whole domain Q. > I OOO, * A simple polynomial (e.g., linear) on each triangle ed i VAVAVAVAVAVAVAVAVAVAVAVAVAMAI KETh IVAVAVAVAVAVAVAVAVAVAVAVAVAVA\ IAVAVAVAVAVAVAVAVAVAVAVAVAVA\ © Still zero on the boundary 8. 02 A 7 WANA VAVATA hiss the space of continuous, piecewise-linear oo PAA 00 02 04 06 08 10 Figure: A mesh Tj, of the unit square Ral November 24, 2025 Song the 2d Poisson Equation using the FEM anda CG Method site



---

## Page 8

Basis Functions (P1 Elements) I H LR I[s How do we build a basis for V;? We use local basis functions (or shape functions) @j associated with each node Nj of the mesh For P1 (piecewise-linear) elements, 6; has a key property © 67 is 1 at its ,own" node Nj © gj is 0 at all other nodes Ny (j # i). © 7 is linear on each triangle. This is the ,hat function" Ral November 24, 2025 Song the 2d Poisson Equation using the FEM anda CG Method site 8



---

## Page 9

Basis Functions (P1 Elements) II H LR I[s (3, ¥s) ‘Area Coordinates 3 On a single triangle with nodes (xa, 1), 02, v2), (03, ys), these shape functions are identical to the area coordinates L,; x = Lx + Loxo + Lax (9) y= Lin + Lays + Lays (20) , ° L=litletls (aa) Gan) Gay) Figure: A single linear triangular element. Ral Novemer 24, 2025 Soling the 24 Poison Equation sng the FEM and a CG Method seit 9



---

## Page 10

Basis Functions (P1 Elements) III H LR I[s Explicit Formulas The area coordinates L; are linear functions of (x, y) a+bix+a ey ee a1 = %2y3 — x3y2, bi = yo — ya, C1 = 3 — x2 (12) a2 + box + © p= Bee a2 = ay — M13, bo = Ya — Yi, C2 = M1 — 3 (13) a3 + bax + 63 by = BARTON a = mye — 20), bo =~ a, 3 = (14) Local Shape Functions On this linear triangle element, the three local shape functions are just: MOY) =Li boxy) =Lo bay) = bs (15) Ral Novemer 24, 2025 Soling the 24 Poison Equation sng the FEM and a CG Method seie 10



---

## Page 11

Gradients & Discrete Form I H LR I[s Gradients of Shape Functions Since the shape functions $, = L, are linear, their gradients are constant on each element: 86) Voi = (3 (16) ay a - ab, _ —% Ob1 _ Ya—¥s (a7) of se (20) Ox 2A oy 2A a - 862 _ a — x. Ob2 _ Ys Ya (as) Ob2 _ M8 (21) ax 2A ay 2A a - a _ Ob3 _ yi ~ yo (19) O$3 _ 2% (22) ax 2A ay 2A a) November 24,2025 Sling the 24 Poison Equation using the FEM and 3 C6 Method Sete it



---

## Page 12

Gradients & Discrete Form II H LR I[s The Galerkin Problem (Discrete Form) We now solve the weak form on the finite-dimensional space Vp: Find uy € Vp such that (Wun, Vvn) = (f. Vn) vn © Vi (23) ‘As the mesh size h—+ 0, the discrete solution up converges to the true solution u a) November 24,2025 Sohiog the 2 Poison Equation sing the FEM ad CG Meta sete 2



---

## Page 13

Converting into a Linear Equation System I H LR I[s Any function up in our space Vy can be written as a linear combination of its basis functions $y Un(x.¥) = Yo ujbj(x.¥) (24) rt Here, nis the total number of nodes in the mesh. Because $)(N;) = 6, the unknown coefficients u, are simply the unknown values of the solution at the nodes: uj = un(N,) Novemer 24, 2025 Soling the 24 Poison Equation sng the FEM and a CG Method sete 13



---

## Page 14

Converting into a Linear Equation System II H LR I[s Substitute this ,ansatz” into the Galerkin problem: (Vuln. Von) = (Ff. bn) Vm © Viv (25) (° (x +) ve) =(F.dn) Von € Vi (26) r= D4 (Vb), Von) = (Fb) Vbn € Vo (27) = This must hold for all @, € Vp. It is sufficient to test it against each basis function $ (for i= 1,...,.n) DY 4 (Vo), Voi) = (F.9;) Wie {1,..-.n} (28) rt Novemer 24, 2025 Soling the 24 Poison Equation sng the FEM and a CG Method Seite 14



---

## Page 15

Converting into a Linear Equation System III H LR I[s This is a linear system of equations Au = F! (Voi. Voi) - (Von, Vor) I fur (f,o1) = (29) (Vo1.Von) - (Von. Von) } Lun, (fF. bn) Ra i ia RN Stifines matric Load vector F The entries are: Ay = (V4). V0) = [ Vd) V0, dx (20) Fa (6.0) := [ F6, ox (21) lo Our goal is to solve this system for the unknown vector of nodal values w. Novemer 24, 2025 Soling the 24 Poison Equation sng the FEM and a CG Method sete 15



---

## Page 16

Assembling and Solving the System I H LR I[s Algorithm 1: Global Assembly input: Meh Tp, Sowce? SSS 1 Initialize A = 0 (sparse n x n matrix) 2 Initialize F = 0 (n x 1 vector) 4 foreach element e in mesh Ty, do ‘ Initialize A® = 0 (3 x 3 local matrix) 5 I tntiaize F° = 0 (3 x 2 local vector) + I Lets, 62.2 be the local shape functions on e > I fori 1030 : Fe Jefe dx : for j= 1 to 3.do Pa I AG = fe PO) VOi de 1 end 2 I end b I fori=1t0 340 “ Fla) += FF s for j= 1 to 3do 6 I Alas.) += AG » end a I end end 20 ApplyDirichlet8C(A, F) a return ALF November 24, 2025 Soling the 24 Poison Equation sng the FEM and a CG Method sete 16



---

## Page 17

Assembling and Solving the System II H LR I[s o 20 Structure of the Matrix A 40 * Aisa large, sparse matrix. 3 © The entry Aj is non-zero only if nodes i and j share 60 an element. © It is also symmetric (Aj; = Aj) and positive-definite. 80 100 o 2 4 60 80 100 column Figure: Sparsity pattern of A. November 24, 2025 Song the 2d Poisson Equation using the FEM anda CG Method sete 17



---

## Page 18

Assembling and Solving the System III H LR I[s Solving the System Because A is sparse, symmetric, and positive-definite, we don't use direct solvers (like A~!). We use efficient iterative solvers like the Conjugate Gradient (CG) Method Algorithm 2: Conjugate Gradient Method. Input: Matix A, vector b, mal ess %y SSCS ‘Output: Solution x



1 gb Ax



2 P="



2 for k “0 to maxit- 1 do



4 I aq = (rf) AP)



5 Ix = a4 + oxeK



6 Tet = tk ~ ADK



>I iflinestlla <= to! then



3] I return xc



9 I Be = CL ater)



I Best = nes + Bie



end



12 return x41 November 24, 2025 Song the 2d Poisson Equation using the FEM anda CG Method Seite 18



---

## Page 19

Solution of the Poisson Equation H LR I[s After solving Au = F for the vector u, we have the value u, at each node. We can then reconstruct the full solution un = u@) for visualization 1.00 I 0.06 0.75 I > 0.50 I 0.04 5 0.25 I 0.02 0.00 Bo 00 0.0 05 1.0 x Figure: The computed discrete solution uj, for a source f = 1 on the unit square Novemer 24, 2025 Soling the 24 Poison Equation sng the FEM and a CG Method seie 19



---

## Page 20

Bibliography



---

## Page 21

Bibliography I HuRIIsS



[1] T Wick. Numerical Methods for Partial Differential Equations. en. Hannover : Institutionelles Repositorium der Leibniz Universitat Hannover, 2020. DOI: 10.15488/9248.



[2] OC Zienkiewicz and RL Taylor. The finite element method. Volume 1: The basis. 5th ed. Oxford: Butterworth-Heinemann, 2002. 689 pp. URL: https: / /www. meil. pw.edu. pl/content /download/58297/306302/file/FEM _ Zienkiewicz%20Voll.pdf (visited on 10/28/2025)



