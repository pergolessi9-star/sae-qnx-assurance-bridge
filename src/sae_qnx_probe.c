#include <stdio.h>
#include <string.h>
#include <sys/utsname.h>
int main(void) {
    struct utsname info;
#ifdef __QNXNTO__
    const int built_for_qnx = 1;
#else
    const int built_for_qnx = 0;
#endif
    if (uname(&info) != 0) { perror("uname"); return 3; }
    printf("SAE_QNX_PROBE_V1\n");
    printf("compile_target_qnx=%d\n", built_for_qnx);
    printf("runtime_sysname=%s\n", info.sysname);
    printf("runtime_release=%s\n", info.release);
    printf("runtime_machine=%s\n", info.machine);
    printf("runtime_qnx=%d\n", strcmp(info.sysname, "QNX") == 0);
    return (built_for_qnx && strcmp(info.sysname, "QNX") == 0) ? 0 : 2;
}
