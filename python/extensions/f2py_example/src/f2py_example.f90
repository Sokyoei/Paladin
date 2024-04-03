module ahrif90
    implicit none

    private
    public::hello

contains
    subroutine hello()
        print *, "hello Fortran90"
    end subroutine hello
end module ahrif90
