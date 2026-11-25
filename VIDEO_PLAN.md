# Demonstration video plan — under 3 minutes

Target length: 2 minutes 40 seconds. Language: English. No third-party music or trademarks.

1. 0:00–0:20 — Show the project, Windows host and QNX SDP 8.0 SDK.
2. 0:20–0:40 — Run the four automated tests and show all passing.
3. 0:40–1:05 — Run SDK inspection and show the qcc driver, headers and both GCC front-ends.
4. 1:05–1:40 — Build AArch64 and x86_64. Show ELF machine IDs 183 and 62, file sizes and SHA-256 evidence.
5. 1:40–2:00 — Explain the QNX Neutrino IPC probe: ChannelCreate, ConnectAttach, MsgSend, MsgReceive and MsgReply.
6. 2:00–2:40 — Show QNX 8.0 booted in QEMU and run the x86_64 probe. Show runtime_sysname=QNX, runtime_qnx=1, qnx_msgsend=1 and exit code 0.

Recording must show the actual running software and target output, not slides or simulated results. If runtime verification fails, do not submit a video implying success.
