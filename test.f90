program test
implicit none
logical, pointer :: L
allocate(L)
L = .false.
print *, L
if (L .EQV. .true.) then
print *, "it's true!"
else
print *, "it's false!"
end if 
deallocate(L)
end
