       program convert_vasp2abinit_density

! program to read the VASP density file and
! convert it the format of ABINIT so that it
! can be used with the 'cut3d' program.
! J M Sullivan NRL 1/18/02

! J M Sullivan NRL 2/6/02
! Additional switch to convert the LOCPOT file from
! vasp into the cut3d format.
!

! JMS 8/6/2003
! Couple of bugs fixed: 1) Typo in index of density for fixing the negative values (see below)
!                       2) Use periodic boundary conditions to properly line up data for the interpolation
!                          of the density.

      implicit none

! integers
      integer j, nxmax, nx, ny, nz, i, nl, is,k
      integer stride, natoms, natoms_max, ispin, dan_unit
      integer ntype, nend, rmdr, cnt, istat, nspin, nstart
      integer, allocatable :: type(:), typelist(:), indexmap(:,:,:)
      integer ntype_max, sio, iswitch, origin_atom, i2, j2, k2, cnt2
      parameter(ntype_max=100) ! Maximum number of types of atoms
      integer cnt_find, d_or_p, cntdmax, istart, iend, i1, j1, k1
      parameter(cntdmax=500000)
      integer, allocatable :: index(:,:), index2(:,:,:)

      integer iatom2, il, ndata
! doubles
      double precision, allocatable :: tmp(:)
      double precision, allocatable :: density(:,:), xred(:,:)
      double precision :: sumt, vol, afac, rprim(3,3), dv, v(3), v2(3), a0
      double precision :: tol, origin(3), dens1, dens2, delta2, delta
      double precision :: dorigin(3), HeV, pi, disc(cntdmax), dx, dy, dz
      double precision, allocatable :: potavg(:), charge(:), chargelist(:)
      parameter(a0=0.529177d0,tol=1.d-5, HeV=27.2116)

! characters
      character*100 title1, title2, title3
      character*2, allocatable :: label1(:), label(:)

! logicals
      logical integrate_file, locpot, direct_write
      logical remap

! to fake an ABINIT file
      character*6 codvsn
      character*132 title4
      parameter(codvsn='vasp43')

      integer headform, fform, bantot, date, intxc, ixc, natom
      integer n1, n2, n3, nkpt, nspden, nspinor, nsppol, nsym
      integer occopt, pspso, pspdat, pspcod, pspxc, lmax, lloc, mmax
      integer itype, cntd
      parameter(headform=23,fform=52)
      integer, allocatable :: istwfk(:), nband(:), npwarr(:), symrel(:,:,:)

      double precision acell(3), zatom, residm, ecut, dval, avgsum
      double precision, allocatable :: zatnum(:), tnons(:,:),occ(:), &
      kpt(:,:), tmp2(:), zion(:)


      character*100 fname

      intrinsic max

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

      pi = acos(-1.0)

      read(*,450) fname
 450  format(a100)
      open(unit=10,file=fname,status='old',form='formatted')


! number of bad densitites
      cntd = 0

! standard ouptut
      sio = 6

! format (# of columns for density in input file)
      stride=5
      allocate(tmp(stride))

! number of types of atoms
      write(sio,'(a)') "Number of atom types?"
      read(*,*) ntype
      allocate(type(ntype),label1(ntype),charge(ntype))
      do i = 1, ntype
         write(*,'(a,2x,i5,2x,a)') "Label & charge for atom #", i, "type?"
         read(*,*) label1(i), charge(i)
      enddo
      write(sio,'(a)') "Number of spin states?"
      read(*,*) nspin

!_jms 2/6/02
      write(*,*) "Density (0) or Potential (1):"
      read(*,*) d_or_p
      locpot = .false.
      if( d_or_p == 1 ) then
         locpot = .true. ! the input file is a potential, not a density
      endif
      
!_jms 2/6/02

      read(10,*) title1
      read(10,*) afac
      do i = 1, 3
         read(10,*) (rprim(j,i),j=1,3)
         write(*,*) (rprim(j,i),j=1,3)
         rprim(:,i) = rprim(:,i)*afac/a0
      enddo

! cell volume
      vol = rprim(1,1)*(rprim(2,2)*rprim(3,3)-rprim(3,2)*rprim(2,3))+ &
          rprim(2,1)*(rprim(3,2)*rprim(1,3)-rprim(1,2)*rprim(3,3))+ &
          rprim(3,1)*(rprim(1,2)*rprim(2,3)-rprim(2,2)*rprim(1,3))
      write(sio,'(a,5x,f15.8)') "Volume of unit cell:", vol
      read(10,*) (type(j),j=1,ntype)
      write(*,*) (type(j),j=1,ntype)
      write(*,*) (charge(j),j=1,ntype)
      natoms = 0
      do i = 1, ntype
         natoms = natoms + type(i)
      enddo
      allocate(label(natoms))
      k = 0
      do i = 1, ntype
         do j = 1, type(i)
            k = k + 1
            label(k) = label1(i)
         enddo
      enddo

      write(sio,'(a,5x,i5)') "Number of atoms:", natoms
      read(10,*) title2
      allocate(xred(3,natoms))
      if( origin_atom == 0 ) then
         origin(:) = 0.0
      endif
      do i = 1, natoms
         read(10,*) (xred(j,i),j=1,3)
      enddo
      read(10,*)
      read(10,*) nx, ny, nz
      do i = 1, 3
         v(i) = rprim(i,1)*origin(1)+rprim(i,2)*origin(2)+rprim(i,3)*origin(3)
      enddo

      write(sio,'(a,5x,i8)') "Number of real space points:", nx*ny*nz
      allocate(density(nspin,nx*ny*nz),STAT=istat)
      allocate(index(3,nx*ny*nz),index2(nx,ny,nz))
      density(:,:) = 0.0
      if( istat /= 0 ) then
         write(sio,'(a)') "Failed to allocate memory for the density."
         write(sio,'(a,5x,f12.8)') "Memory demands (MB):", float(nspin*8*nx*ny*nz)/1.d6
      endif
      dv = vol/float(nx*ny*nz)
      write(sio,'(a,5x,f8.4)') "Integration weight:", dv


      nl = nx*ny*nz/stride
!      write(*,*) "Number of input lines:", nl
      write(*,*)
      sumt = 0.0
      cnt = 0
      is = 1
      do i = 1, nl
         read(10,*) (tmp(j),j=1,stride)
         do j = 1, stride
            cnt = cnt + 1
            density(is,cnt) = tmp(j)
            sumt = sumt + tmp(j)

!_jms 2/6/02
            if ( .not. locpot ) then
!_jms 2/6/02

               if( tmp(j) .lt. 0.0 ) then
!                  write(*,*) cnt
!                  write(*,*) tmp(j)
!                  write(sio,'(a)') "Negative density?"
                  cntd = cntd + 1
                  if( cntd > cntdmax ) then
                     write(*,'(a)') "Recompile with larger cntdmax parameter"
                     stop 'recompile'
                  endif
                  disc(cntd) = tmp(j)
!                  density(is,cnt) = 0.0
!                  stop 'n(x)<0'
               endif

!_jms 2/6/02
            endif
!_jms 2/6/02

         enddo
      enddo
      if( cnt < nx*ny*nz ) then
         read(10,*) (tmp(j-cnt),j=cnt+1,nx*ny*nz)
         do j = cnt+1, nx*ny*nz
            sumt = sumt + tmp(j-cnt)
            density(is,j) = tmp(j-cnt)

!_jms 2/6/02
            if ( .not. locpot ) then
!_jms 2/6/02

               if( tmp(j-cnt) .lt. 0.0 ) then
!                  write(*,*) cnt
!                  write(*,*) tmp(j-cnt)
!                  write(sio,'(a)') "Negative density?"
                  cntd = cntd + 1
                  disc(cntd) = tmp(j-cnt)
!                  density(is,j) = 0.0
!                  stop 'n(x)<0'
               endif

!_jms 2/6/02
            endif
!_jms 2/6/02
         enddo
      endif
      sumt = sumt/float(nx*ny*nz)
      if( .not. locpot ) then
         write(sio,'(a,5x,f20.12)') "Total electron charge:", sumt
      else
         write(sio,'(a,5x,f20.12)') "Average up potential (eV):", sumt
      endif

      if( .not. locpot ) then
         write(sio,'(a,2x,i8)') "Number of bad density points we discarded:", cntd
         !write(sio,*) "Summary of those points:", disc(1:cntd)
         write(sio,*)
      endif


! Spin-polarized calculations
      if( nspin == 2 ) then
         is = 2

!_jms 2/6/02
         if( .not. locpot ) then
!_jms 4/2/03
! This reads in the data for the augmentation occupancies
            do i = 1, natoms
               read(10,'(a24,i4,i4)') title3, iatom2, ndata
               if( iatom2 /= i ) then
                  stop 'incorrect atom match'
               endif
               if( ndata == 0 ) then
                  read(10,*)
               else
                  stride = 5
                  nl = ndata/stride
                  if( nl == 0 ) then
                     read(10,*) (tmp(j),j=1,ndata)
                  else
                     do il = 1, nl
                        read(10,*) (tmp(j),j=1,stride)
                     enddo
                     read(10,*) (tmp(j),j=1,ndata-nl*stride)
                  endif                  
               endif
!_jms 4/2/03
            enddo
         endif
!_jms 2/6/02

         rmdr = natoms
         nend = stride
         if( natoms < nend ) nend = natoms
         do while ( rmdr .gt. 0 )
            read(10,*) (tmp(i),i=1,nend)
            rmdr = rmdr - stride
            if( rmdr .lt. stride ) then
               nend = rmdr
            endif
         enddo
         read(10,*) nx, ny, nz
         nl = nx*ny*nz/stride
!         write(*,*) "Number of input lines:", nl
         write(*,*)
         sumt = 0.0
         cnt = 0
         do i = 1, nl
            read(10,*) (tmp(j),j=1,stride)
            do j = 1, stride
               cnt = cnt + 1
               density(is,cnt) = tmp(j)
               sumt = sumt + tmp(j)
            enddo
         enddo
         if( cnt < nx*ny*nz ) then
            read(10,*) (tmp(j-cnt),j=cnt+1,nx*ny*nz)
            do j = cnt+1, nx*ny*nz
               sumt = sumt + tmp(j-cnt)
               density(is,j) = tmp(j-cnt)
            enddo
         endif
         sumt = sumt/float(nx*ny*nz)
         if( .not. locpot ) then
            write(sio,'(a,5x,f12.8)') "Total electron moment:", sumt
         else
            write(sio,'(a,5x,f12.8)') "Average dn potential (eV):", sumt
         endif

      endif
      close(10)
      cnt = nx*ny*nz
!      write(*,*) "Number of points in the file:", cnt
      write(*,*)


! renormalize the density to the same as the ABINIT format (total and up)
      if( nspin == 2 ) then

!_jms 2/6/02
         if( .not. locpot ) then
!_jms 2/6/02

! This constructs the first component as the total density and the 2nd as the spin
! up density.
            write(*,*) "Renormalizing the density"
            allocate(tmp2(cnt))
            tmp2(1:cnt) = (density(1,1:cnt)+density(2,1:cnt))/2.0/vol
            density(2,1:cnt) = tmp2(1:cnt)
            deallocate(tmp2)

!_jms 2/6/02
         else
            density(2,1:cnt) = density(2,1:cnt)/HeV
!_jms 2/6/02

         endif
      endif
      if( .not. locpot ) then
         density(1,1:cnt) = density(1,1:cnt)/vol
      else
         density(1,1:cnt) = density(1,1:cnt)/HeV
      endif
      write(*,*) "Producing an output file:"


!_jms 12/10/02
! Now we patch the negative density values by averaging the neighboring points
      cnt = 0
      do i = 1, nx
         do j = 1, ny
            do k = 1, nz
               cnt = cnt + 1
               index(1,cnt) = i
               index(2,cnt) = j
               index(3,cnt) = k
               index2(i,j,k) = cnt
            enddo
         enddo
      enddo

      if( .not. locpot ) then
         write(*,'(a)') "Here we fix the density to be positive definite."
         do cnt = 1, nx*ny*nz
            do is = 1, nspin
               
! if we encounter a negative density value we simply average the neighboring 6 points

!_jms 8/6/2003 Fixed bug here: density(is,i) -> density(is,cnt)
               if( density(is,cnt) < 0.0 ) then
                  i = index(1,cnt)
                  j = index(2,cnt)
                  k = index(3,cnt)
                  avgsum = 0.d0
                  do i1 = i-1, i+1, 2
                     do j1 = j-1, j+1, 2
                        do k1 = k-1, k+1, 2
!                           if( density(is,index2(i1,j1,k1)) < 0.0 ) then
!                              stop 'you are screwed'
!                           endif

!_jms 8/6/2003 Watch out for address errors and use the PBC's to get the data
! line up correct.
                           if( k1 == 0 ) then
                              k2 = nz
                           elseif( k1 == nz+1 ) then
                              k2 = 1
                           else
                              k2 = k1
                           endif

                           if( j1 == 0 ) then
                              j2 = ny
                           elseif( j1 == ny+1 ) then
                              j2 = 1
                           else
                              j2 = j1
                           endif

                           if( i1 == 0 ) then
                              i2 = nx
                           elseif( i1 == nx+1 ) then
                              i2 = 1
                           else
                              i2 = i1
                           endif

!                           write(*,*) avgsum, density(is,index2(i2,j2,k2))
                           avgsum = avgsum + density(is,index2(i2,j2,k2))
                        enddo
                     enddo
                  enddo
!                  if( avgsum < 0.0 ) then
!                     write(*,*) is
!                     write(*,*) avgsum
!                     write(*,*) i, nx
!                     write(*,*) j, ny
!                     write(*,*) k, nz
!                     stop 'you are screwed'
!                  endif
                  density(is,cnt) = avgsum/6.0
               endif
               
            enddo ! end of loop over spin
         enddo ! end of loop over space
      endif


!_jms 12/10/02



! make a dan file
      open(unit=66,file='dan.out',status='unknown',form='formatted')
      write(66,*) nx, ny, nz
      write(66,*) 1, nx
      write(66,*) 1, ny
      write(66,*) 1, nz
      cnt = 0
      do i = 1, nx
         do j = 1, ny
            do k = 1, nz
            cnt=cnt+1
            write(66,*) density(1,cnt)
            enddo
         enddo
      enddo
      close(66)

         direct_write = .true.
!         direct_write = .false.
! produce an ABINIT density file
      if( .not. locpot ) then
         open(unit=50,file='txo_VASP_DEN',status='unknown',form='unformatted')

!_jms 12/4/02

         if( direct_write) then
            if( nspin == 2 ) then
               open(unit=51,file='dens.out_up',status='unknown',form='formatted')
               open(unit=52,file='dens.out_dn',status='unknown',form='formatted')
               write(51,*) rprim(1,1), rprim(2,2), rprim(3,3)
               write(52,*) rprim(1,1), rprim(2,2), rprim(3,3)
               write(51,*) nx, ny, nz
               write(52,*) nx, ny, nz
            else
               open(unit=51,file='dens.out',status='unknown',form='formatted')
               write(51,*) rprim(1,1), rprim(2,2), rprim(3,3)
               write(51,*) nx, ny, nz
            endif
         endif

      else
         open(unit=50,file='txo_VASP_POT',status='unknown',form='unformatted')

!_jms 12/4/02
         if( direct_write) then
            if( nspin == 2 ) then
               open(unit=51,file='pot.out_up',status='unknown',form='formatted')               
               open(unit=52,file='pot.out_dn',status='unknown',form='formatted')
               write(51,*) rprim(1,1), rprim(2,2), rprim(3,3)
               write(52,*) rprim(1,1), rprim(2,2), rprim(3,3)
               write(51,*) nx, ny, nz
               write(52,*) nx, ny, nz
            else
               open(unit=51,file='pot.out',status='unknown',form='formatted')
               write(51,*) rprim(1,1), rprim(2,2), rprim(3,3)
               write(51,*) nx, ny, nz
            endif
         endif

      endif

!_jms 12/4/02



!_jms testing cut3d program for numerical artifacts
      if( direct_write) then
         cnt = 0
         do k = 1, nz
            avgsum = 0.d0
            do i = 1, nx
               do j = 1, ny
                  cnt = cnt + 1
                  avgsum = avgsum + density(1,cnt)
               enddo
            enddo
            write(78,*) k, avgsum/float(nx*ny)
         enddo
         acell(1) = rprim(1,1)
         acell(2) = rprim(2,2)
         acell(3) = rprim(3,3)
         dx = acell(1)/float(nx)
         dy = acell(2)/float(ny)
         dz = acell(3)/float(nz)
         do ispin = 1, nspin
            cnt2 = 0
            do k = 1, nz
               do i = 1, nx
                  do j =1, ny
                     cnt2 = cnt2 + 1
 !                    if( density(ispin,cnt2) < 0.0 ) then
 !                       stop 'bad density point'
 !                    endif

                     write(50+ispin,'(4(f20.16,2x))') float(i-1)*dx, float(j-1)*dy, &
                     float(k-1)*dz, density(ispin,cnt2)
                  enddo
               enddo
            enddo
            close(50+ispin)
         enddo

      endif
!_jms 12/4/02

      write(50) codvsn, headform,fform
      bantot=1
      date=00
      intxc=1
      ixc=1
      natom = natoms
      n1 = nx
      n2 = ny
      n3 = nz
      nkpt = 1
      nsppol = nspin
      nspden = nspin
      nspinor = 1
      nsym = 1
      occopt=1
      ecut=1.d0
      acell(1:3) = 1.d0
      write(50) bantot,date,intxc,ixc,natom,n1,n2,n3,&
      nkpt,nspden,nspinor,nsppol,nsym,ntype,occopt,acell(1:3),ecut,rprim(1:3,1:3)
      write(22,*) bantot,date,intxc,ixc,natom,n1,n2,n3,&
      nkpt,nspden,nspinor,nsppol,nsym,ntype,occopt,acell(1:3),ecut,rprim(1:3,1:3)


      allocate(nband(nkpt*nsppol),npwarr(nkpt),istwfk(nkpt),kpt(3,nkpt))
      allocate(occ(bantot),tnons(3,nsym),zatnum(ntype),symrel(3,3,nsym))
      nband(1:nkpt*nsppol) = 1
      npwarr(1:nkpt) = 1
      symrel(1:3,1:3,1:nsym) = 0
      symrel(1,1,1) = 1
      symrel(2,2,1) = 1
      symrel(3,3,1) = 1
      istwfk(1:nkpt) = 1
      kpt(1:3,1:nkpt) = 0.0
      occ(1:bantot) = 1.0
      tnons(1:3,1:nsym) = 0.0
      zatnum(1:ntype) = charge(1:ntype)
      allocate(chargelist(natom),typelist(natom))
      k=0
      do i = 1, ntype
         do j = 1, type(i)
            k=k+1
            chargelist(k) = charge(i)
            typelist(k)=i
         enddo
      enddo
!      write(*,*) "charge list:", chargelist
      
      write(50) nband(1:nkpt*nsppol),npwarr(1:nkpt), &
      symrel(1:3,1:3,1:nsym),typelist(1:natom),istwfk(1:nkpt),&
      kpt(1:3,1:nkpt),occ(1:bantot),tnons(1:3,1:nsym),zatnum(1:ntype)
      allocate(zion(ntype))
      zion=zatnum
      do itype=1,ntype
         title4='vasp_fake_file'
         zatom = zion(itype)
         pspso=0
         pspdat=0
         pspcod=0
         pspxc=1
         lmax=0
         lloc=0
         mmax=0
         write(50) title4,zatom,zion(itype),pspso,pspdat,pspcod,pspxc,&
         lmax,lloc,mmax
      enddo
      residm=1.d-6
!_jms 11/15/2004
!jms_old write(50) residm,xred(1:3,1:natom) 
      write(50) residm,xred(1:3,1:natom), residm, residm
!_jms nrl 11/15/2004
      do ispin=1, nspden
         write(50) (density(ispin,cnt),cnt=1,n1*n2*n3)
      enddo
      close(50)

! perform the cell averages
      if( .not. locpot ) then
         write(*,*) "Caveat: charges are total and up"
      else
         write(*,*) "Caveat: potentials are up and down"
      endif

      allocate(potavg(nspden))
      do ispin = 1, nspden
         potavg(ispin) = sum( density(ispin,:) )
         potavg(ispin) = potavg(ispin)/float(n1*n2*n3)
         if( .not. locpot ) then
            potavg(ispin) = vol*potavg(ispin)
         endif
      enddo

      if( .not. locpot ) then
         if( nspden == 2 ) then
            tmp(1) = potavg(2)
            potavg(2) = potavg(1)-tmp(1)
            potavg(1) = tmp(1)
         endif
      endif

      do ispin = 1, nspden
         if( locpot ) then
            write(*,*) "Average potential (Ha):", ispin, potavg(ispin)
         else
            write(*,*) "Average density (Ha):", ispin, potavg(ispin)
         endif
      enddo
      if( nspden == 2 ) then
         if( .not. locpot ) then
            write(*,'(a,5x,f8.4)') "Average moment:", potavg(1) - potavg(2)
         else
            write(*,'(a,5x,f8.4)') "Average potential difference (eV):", &
            (potavg(1) - potavg(2))*27.2116
         endif
      endif


      end

      
