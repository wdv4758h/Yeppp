!
!                      Yeppp! library implementation
!
! This file is part of Yeppp! library and licensed under 2-clause BSD license.
! See library/LICENSE.txt for details.
!
!
MODULE yepLibrary
    INTERFACE
        INTEGER(C_INT) FUNCTION yepLibrary_Init() BIND(C, NAME='yepLibrary_Init')
            USE ISO_C_BINDING, ONLY: C_INT
            IMPLICIT NONE
        END FUNCTION yepLibrary_Init
        INTEGER(C_INT) FUNCTION yepLibrary_Release() BIND(C, NAME='yepLibrary_Release')
            USE ISO_C_BINDING, ONLY: C_INT
            IMPLICIT NONE
        END FUNCTION yepLibrary_Release
        INTEGER(C_INT) FUNCTION yepLibrary_GetTimerTicks(t) BIND(C, NAME='yepLibrary_GetTimerTicks')
            USE ISO_C_BINDING, ONLY: C_INT, C_INT64_T
            IMPLICIT NONE
            INTEGER(C_INT64_T), INTENT(OUT) :: t
        END FUNCTION yepLibrary_GetTimerTicks
        INTEGER(C_INT) FUNCTION yepLibrary_GetTimerFrequency(f) BIND(C, NAME='yepLibrary_GetTimerFrequency')
            USE ISO_C_BINDING, ONLY: C_INT, C_INT64_T
            IMPLICIT NONE
            INTEGER(C_INT64_T), INTENT(OUT) :: f
        END FUNCTION yepLibrary_GetTimerFrequency
        INTEGER(C_INT) FUNCTION yepLibrary_GetTimerAccuracy(a) BIND(C, NAME='yepLibrary_GetTimerAccuracy')
            USE ISO_C_BINDING, ONLY: C_INT, C_INT64_T
            IMPLICIT NONE
            INTEGER(C_INT64_T), INTENT(OUT) :: a
        END FUNCTION yepLibrary_GetTimerAccuracy
    END INTERFACE
END MODULE yepLibrary
