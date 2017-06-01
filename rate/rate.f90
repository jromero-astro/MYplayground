program rate

!GERMAN MOLPECERES DE DIEGO (2017)
!THIS PROGRAM CALCULATES THE RATE CONSTANT INCLUDING TUNNELING AS PROPOSED BY FERMANN & AUERBACH (JPC 112,15 2000)
!OF A SURFACE PROCESS

implicit real*8 (a-h,o-z)

real*8 ::  expo, zpointr,zpoints,zpointts, den,Er,Ep,Ets,gapd,gapi
integer :: nmodesr, nmodesp , nmodetst, tini, tfin
real*8, parameter :: kboltz=1.38064D-23 , planck=6.626070D-34 , pi=3.14159265359, c= 2.99792418D10 ,avo=6.023D23
real*8, parameter :: R=8.314472D-3
real*8, parameter :: eheV=27. , ehkcal=627.5 , cmhz=2.99793D10
real*8, dimension(:), allocatable :: vibmodesr, vibmodesp, vibmodetst
real*8, dimension(10000) :: Qreac, Qprod, Qts, ktst , ktsti, tunn , ktotd , tunni, ktoti

open (5,file='modes.dat',status='unknown')
open (4,file='parameters.dat',status='unknown')
open (8, file='output.dat')
open (9, file='graph.dat')
read (4,*) Tini, Tfin

!ALLOCATE ARRAYS

read(5,*) nmodesr
allocate (vibmodesr(nmodes))
write(8,*) '++++++++++++++++++++++++++++++++++'
write(8,*) 'NUMBER OF VIB MODES IN REACTANTS'
write(8,*) nmodesr
write(8,*) '++++++++++++++++++++++++++++++++++'
read(5,*) nmodesp
allocate (vibmodesp(nmodes))
write(8,*) '++++++++++++++++++++++++++++++++++'
write(8,*) 'NUMBER OF VIB MODES IN PRODUCTS' 
write(8,*) nmodesp
write(8,*) '++++++++++++++++++++++++++++++++++'
read(5,*) nmodetst
allocate (vibmodetst(nmodes))
write(8,*) '++++++++++++++++++++++++++++++++++'
write(8,*) 'NUMBER OF VIB MODES IN TS' 
write(8,*)  nmodetst
write(8,*) '++++++++++++++++++++++++++++++++++'

!READ MODES


!REACTANTS

write(8,*) 'VIB MODES REACTANTS' 
write(8,*) '++++++++++++++++++++++++++++++++++'
do i=1,nmodesr
	read(5,*) vibmodesr (i)
write(8,*) (vibmodesr (i))
end do

write(8,*) '++++++++++++++++++++++++++++++++++'
!PRODUCTS
write(8,*) 'VIB MODES PRODUCTS' 
do i=1, nmodesp
	read (5,*) vibmodesp (i)
	write(8,*) vibmodesp (i)
end do

write(8,*) '++++++++++++++++++++++++++++++++++'
!TS
write(8,*) 'VIB MODES TS' 
do i=1, nmodetst
	read(5,*) vibmodetst (i)
	write(8,*) vibmodetst (i)
end do

!CONVERT (REAL) VIBRATIONAL FREQUENCIES TO TOTAL VIBRATIONAL PARTITION FUNCTION

!REACTANTS

write(8,*) '++++++++++++++++++++++++++++++++++'
write(8,*) 'PARTITION FUNCTION REACTANTS'
do i=Tini,Tfin, 5
	Qreac(i)=1.
	do j=1,nmodesr
		expo=-((planck*vibmodesr(j)*cmhz)/(kboltz*i))
		den= 1-dexp(expo)
		Qreac(i)=Qreac(i)*(1/den)
	end do
write(8,*) 'Temperature' , i , Qreac (i)
end do	

write(8,*) '++++++++++++++++++++++++++++++++++'
!PRODUCTS
write(8,*) 'PARTITION FUNCTION PRODUCTS'
do i=Tini,Tfin, 5
	Qprod(i)=1.
	do j=1,nmodesp
		expo=-((planck*c*vibmodesp(j))/(kboltz*i))
		den= 1-dexp(expo)
		Qprod(i)=Qprod(i)*(1/den)
	end do
write(8,*) 'Temperature' , i , Qprod (i)
end do

write(8,*) '++++++++++++++++++++++++++++++++++'
!TS	
write(8,*) 'PARTITION FUNCTION TS'
do i=Tini,Tfin, 5
	Qts(i)=1.
!El 2 a continuacion elimina que se mapee la frecuencia imaginaria 
	do j=2,nmodetst
		expo=-((planck*c*vibmodetst(j))/(kboltz*i))
		den= 1-dexp(expo)
		Qts(i)=Qts(i)*(1/den)
	end do
write(8,*) 'Temperature' , i , Qts (i)
end do

write(8,*) '++++++++++++++++++++++++++++++++++'
!HASTA AQUI FUNCIONA PERFECTO
!CALCULO DE LA CONSTANTE DE VELOCIDAD COMO k=(Qts/Qa.Qb)*kb*T/h*EXP(-AE/RT
!READ ELECTRONIC ENERGY+ZPE IN HARTREE
read(4,*) Er,Ep,Ets

gapd=(Ets-Er)
gapi=(Ets-Ep)
write(8,*) 'BARRERA DIRECTA(eV)' , gapd*ehev
write(8,*) 'BARRERA DIRECTA(KCAL/MOL)' , gapd*ehkcal

write(8,*) 'BARRERA INVERSA(eV)' , gapi*ehev
write(8,*) 'BARRERA INVERSA(KCAL/MOL)' , gapi*ehkcal

if (gapd*10 < gapi) then 
	write(8,*) 'LA REACCION NO ES UN EQUILIBRIO'
	else
	write(8,*) 'CUIDADO! LA REACCION PUEDE SER UN EQUILIBRIO'
end if
write(8,*) '+++++++++++++++++NO TUNNELING RATE CONSTANTS++++++++++'

!CALCULATION OF ENERGETIC TERM

do i=Tini,Tfin, 5
	ktst(i)=((kboltz*i)/planck)*(Qts(i)/(Qreac(i)))*dexp(-(gapd*2600)/(R*i))
	ktsti(i)=((kboltz*i)/planck)*(Qts(i)/(Qprod(i)))*dexp(-(gapi*2600)/(R*i))
	write(8,*) 'Temperature' , i ,'DIRECT' , ktst(i), 'INVERSE' , ktsti(i)
end do
	

write(8,*) '++++++++++++++TUNNELING CORRECTION++++++++++++++++++'
write(8,*) 'FOLLOWING' , vibmodetst(1) , 'CM-1 MODE'
write(8,*) '++++++++++++++++++++++++++++++++++++++++++++++++++++'
!HASTA AQUI FUNCIONA BIEN
!TUNNELING CORRECTIONS, SEE ABOVEMENTIONED PAPER


do i = Tini, Tfin, 5
	tunn(i)=dexp(-(2*pi*gapd*(2600/avo)*1000)/(planck*dabs(vibmodetst(1))*cmhz))&
	*(1+((2*pi*kboltz*i)/(planck*dabs(vibmodetst(1))*cmhz)))*dexp((gapd*2600)/(R*i))
	tunni(i)=dexp(-(2*pi*gapi*(2600/avo)*1000)/(planck*dabs(vibmodetst(1))*cmhz))&
	*(1+((2*pi*kboltz*i)/(planck*dabs(vibmodetst(1))*cmhz)))*dexp((gapi*2600)/(R*i))
	write(8,*) 'Temperature' , i , "TUNNELING FACTOR DIRECT" , tunn(i) , "TUNNELING FACTOR INVERT" , tunni(i)
end do

write(8,*) '++++++++++++++CORRECTED RATE CONSTANT++++++++++++++++++'
do i= Tini, Tfin , 5
	ktotd(i)=ktst(i)*tunn(i)
	ktoti(i)=ktsti(i)*tunni(i)
	write(8,*)  'Temperature' , i , 'RATE CONSTANT DIRECT',  ktotd(i), "RATE CONSTANT INVERSE" , ktoti(i)
end do

do i= Tini, Tfin , 5
	write (9,*) i , ktotd(i)
end do

end
	
	 


