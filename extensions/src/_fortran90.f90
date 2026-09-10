module ahri
    implicit none

    private
    public::hello_fortran90

contains
    subroutine hello_fortran90()
        print *, "Hello Fortran90!"
    end subroutine hello_fortran90
end module ahri
