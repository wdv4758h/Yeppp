!
!                      Yeppp! library implementation
!
! This file is part of Yeppp! library and licensed under 2-clause BSD license.
! See library/LICENSE.txt for details.
!
!
MODULE yepMath
    INTERFACE
        INTEGER(C_INT) FUNCTION yepMath_Log_V64f_V64f(x, y, n) BIND(C, NAME='yepMath_Log_V64f_V64f')
            USE ISO_C_BINDING, ONLY: C_INT, C_DOUBLE, C_SIZE_T
            IMPLICIT NONE
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: x
            REAL(C_DOUBLE), INTENT(OUT), DIMENSION(n) :: y
            INTEGER(C_SIZE_T), VALUE                  :: n
        END FUNCTION yepMath_Log_V64f_V64f
        INTEGER(C_INT) FUNCTION yepMath_Exp_V64f_V64f(x, y, n) BIND(C, NAME='yepMath_Exp_V64f_V64f')
            USE ISO_C_BINDING, ONLY: C_INT, C_DOUBLE, C_SIZE_T
            IMPLICIT NONE
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: x
            REAL(C_DOUBLE), INTENT(OUT), DIMENSION(n) :: y
            INTEGER(C_SIZE_T), VALUE                  :: n
        END FUNCTION yepMath_Exp_V64f_V64f
    END INTERFACE
END MODULE yepMath
