#include <stdio.h>
#include <string.h>
#include <sys/utsname.h>

#ifdef __QNXNTO__
#include <errno.h>
#include <pthread.h>
#include <sys/neutrino.h>
#endif

typedef struct {
    int sequence;
    char payload[24];
} sae_request_t;

typedef struct {
    int accepted;
    char payload[24];
} sae_reply_t;

#ifdef __QNXNTO__
static int sae_channel_id = -1;

static void *sae_ipc_server(void *unused) {
    sae_request_t request;
    sae_reply_t reply;
    int rcvid;
    (void)unused;

    memset(&request, 0, sizeof(request));
    memset(&reply, 0, sizeof(reply));

    rcvid = MsgReceive(sae_channel_id, &request, sizeof(request), NULL);
    if (rcvid == -1) {
        return NULL;
    }

    if (request.sequence == 42 &&
        strcmp(request.payload, "SAE-QNX-PING") == 0) {
        reply.accepted = 1;
        (void)snprintf(reply.payload, sizeof(reply.payload), "%s", "SAE-QNX-PONG");
    }

    (void)MsgReply(rcvid, EOK, &reply, sizeof(reply));
    return NULL;
}

static int sae_test_message_passing(void) {
    pthread_t server_thread;
    int connection_id;
    int result = 0;
    sae_request_t request;
    sae_reply_t reply;

    sae_channel_id = ChannelCreate(0);
    if (sae_channel_id == -1) {
        return 0;
    }

    if (pthread_create(&server_thread, NULL, sae_ipc_server, NULL) != 0) {
        (void)ChannelDestroy(sae_channel_id);
        return 0;
    }

    connection_id = ConnectAttach(0, 0, sae_channel_id, _NTO_SIDE_CHANNEL, 0);
    if (connection_id != -1) {
        memset(&request, 0, sizeof(request));
        memset(&reply, 0, sizeof(reply));
        request.sequence = 42;
        (void)snprintf(request.payload, sizeof(request.payload), "%s", "SAE-QNX-PING");

        if (MsgSend(connection_id, &request, sizeof(request), &reply, sizeof(reply)) == 0 &&
            reply.accepted == 1 &&
            strcmp(reply.payload, "SAE-QNX-PONG") == 0) {
            result = 1;
        }
        (void)ConnectDetach(connection_id);
    }

    (void)pthread_join(server_thread, NULL);
    (void)ChannelDestroy(sae_channel_id);
    sae_channel_id = -1;
    return result;
}
#endif

int main(void) {
    struct utsname info;
    int runtime_qnx = 0;
    int built_for_qnx = 0;
    int message_passing = 0;

#ifdef __QNXNTO__
    built_for_qnx = 1;
#endif

    if (uname(&info) != 0) {
        perror("uname");
        return 3;
    }

    runtime_qnx = (strcmp(info.sysname, "QNX") == 0);

#ifdef __QNXNTO__
    message_passing = sae_test_message_passing();
#endif

    printf("SAE_QNX_PROBE_V2\n");
    printf("compile_target_qnx=%d\n", built_for_qnx);
    printf("runtime_sysname=%s\n", info.sysname);
    printf("runtime_release=%s\n", info.release);
    printf("runtime_machine=%s\n", info.machine);
    printf("runtime_qnx=%d\n", runtime_qnx);
    printf("qnx_msgsend=%d\n", message_passing);

    return (built_for_qnx && runtime_qnx && message_passing) ? 0 : 2;
}
