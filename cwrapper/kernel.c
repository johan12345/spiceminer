#include "CustomSpice.h"

/* Load kernel */
char* furnsh_custom(char* path) {
    furnsh_c(path);
    CHECK_EXCEPTION
    FINALIZE
}

/* Unload kernel */
char* unload_custom(char* path) {
    unload_c(path);
    CHECK_EXCEPTION
    FINALIZE
}

/* Find all IDs in an spk file */
char* spkobj_custom(char* path, SpiceCell* ids) {
    spkobj_c(path, ids);
    CHECK_EXCEPTION
    FINALIZE
}
