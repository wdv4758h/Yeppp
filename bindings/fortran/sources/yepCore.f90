!
!                      Yeppp! library implementation
!
! This file is part of Yeppp! library and licensed under 2-clause BSD license.
! See library/LICENSE.txt for details.
!
!
MODULE yepCore
    INTERFACE
        INTEGER(C_INT) FUNCTION yepCore_Add_V64fV64f_V64f(x, y, z, n) BIND(C, NAME='yepCore_Add_V64fV64f_V64f')
            USE ISO_C_BINDING, ONLY: C_INT, C_DOUBLE, C_SIZE_T
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: x
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: y
            REAL(C_DOUBLE), INTENT(OUT), DIMENSION(n) :: z
            INTEGER(C_SIZE_T), VALUE                  :: n
        END FUNCTION yepCore_Add_V64fV64f_V64f
        INTEGER(C_INT) FUNCTION yepCore_Subtract_V64fV64f_V64f(x, y, z, n) BIND(C, NAME='yepCore_Subtract_V64fV64f_V64f')
            USE ISO_C_BINDING, ONLY: C_INT, C_DOUBLE, C_SIZE_T
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: x
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: y
            REAL(C_DOUBLE), INTENT(OUT), DIMENSION(n) :: z
            INTEGER(C_SIZE_T), VALUE                  :: n
        END FUNCTION yepCore_Subtract_V64fV64f_V64f
        INTEGER(C_INT) FUNCTION yepCore_Multiply_V64fV64f_V64f(x, y, z, n) BIND(C, NAME='yepCore_Multiply_V64fV64f_V64f')
            USE ISO_C_BINDING, ONLY: C_INT, C_DOUBLE, C_SIZE_T
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: x
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: y
            REAL(C_DOUBLE), INTENT(OUT), DIMENSION(n) :: z
            INTEGER(C_SIZE_T), VALUE                  :: n
        END FUNCTION yepCore_Multiply_V64fV64f_V64f
        INTEGER(C_INT) FUNCTION yepCore_SumSquares_V64f_S64f(x, y, n) BIND(C, NAME='yepCore_SumSquares_V64f_S64f')
            USE ISO_C_BINDING, ONLY: C_INT, C_DOUBLE, C_SIZE_T
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: x
            REAL(C_DOUBLE), INTENT(OUT)               :: y
            INTEGER(C_SIZE_T), VALUE                  :: n
        END FUNCTION yepCore_SumSquares_V64f_S64f
        INTEGER(C_INT) FUNCTION yepCore_DotProduct_V64fV64f_S64f(x, y, z, n) BIND(C, NAME='yepCore_DotProduct_V64fV64f_S64f')
            USE ISO_C_BINDING, ONLY: C_INT, C_DOUBLE, C_SIZE_T
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: x
            REAL(C_DOUBLE), INTENT(IN), DIMENSION(n)  :: y
            REAL(C_DOUBLE), INTENT(OUT)               :: z
            INTEGER(C_SIZE_T), VALUE                  :: n
        END FUNCTION yepCore_DotProduct_V64fV64f_S64f
    END INTERFACE
END MODULE yepCore
