
import numpy as np
import matplotlib.pyplot as plt

# 1. INPUT MESSAGE
message = "hello"

# Convert each character into 8-bit ASCII binary
binary_data = ""

for character in message:
    binary_data += format(ord(character), "08b")

# Convert binary string into integer bits
bits = np.array([int(bit) for bit in binary_data])

# Number of bits
N = len(bits)

print("Sent Message      :", repr(message))
print("Binary Data       :", binary_data)
print("Number of Bits    :", N)

# 2. INPUT BINARY WAVEFORM
samples_per_bit = 100

# Repeat each bit to form a digital waveform
input_waveform = np.repeat(bits, samples_per_bit)

# Time axis in bit periods
t = np.arange(N * samples_per_bit) / samples_per_bit

# 3. BPSK MODULATION
# Bit 0 -> -1 V, Bit 1 -> +1 V
bpsk_symbols = 2 * bits - 1

# Create continuous transmitted waveform
tx_signal = np.repeat(bpsk_symbols, samples_per_bit)

# 4. AWGN COMMUNICATION CHANNEL
snr_db = 7

# Calculate signal power
signal_power = np.mean(tx_signal ** 2)

# Calculate noise power
noise_power = signal_power / (10 ** (snr_db / 10))

# Fixed seed for repeatable results
np.random.seed(42)

# Generate Gaussian noise
noise = np.sqrt(noise_power) * np.random.randn(len(tx_signal))

# Received signal = transmitted signal + noise
rx_signal = tx_signal + noise

# 5. BPSK DEMODULATION
# Divide received signal into individual bit periods
rx_samples = rx_signal.reshape(N, samples_per_bit)

# Take average value of each bit period
average_received = np.mean(rx_samples, axis=1)

# Decision threshold = 0
received_bits = (average_received >= 0).astype(int)

# Create received binary waveform
received_waveform = np.repeat(received_bits, samples_per_bit)

# 6. CONVERT RECEIVED BITS TO STRING
received_binary = ""

for bit in received_bits:
    received_binary += str(bit)

received_message = ""

for i in range(0, len(received_binary), 8):
    byte = received_binary[i:i + 8]
    character = chr(int(byte, 2))
    received_message += character

# 7. CALCULATE BIT ERRORS
bit_errors = np.sum(bits != received_bits)

# 8. DISPLAY TRANSMISSION RESULT
print()
print("---------------------------------------------")
print("TRANSMISSION RESULT")
print("---------------------------------------------")

print("Sent Message      :", repr(message))
print("Received Message  :", repr(received_message))
print("Transmitted Bits  :", "".join(map(str, bits)))
print("Received Bits     :", "".join(map(str, received_bits)))
print("Bit Errors        :", bit_errors)
print("SNR               :", snr_db, "dB")

# 9. CREATE FOUR GRAPHS
fig, axes = plt.subplots(4, 1, figsize=(12, 8.5))

# Main heading
fig.suptitle(
    f"Sent Message: '{message}'     |    "
    f"Received Message: '{received_message}'",
    fontsize=15,
    fontweight="bold",
    y=0.985
)

# GRAPH 1: INPUT BINARY WAVEFORM
axes[0].step(t, input_waveform, where="post", linewidth=1.2)
axes[0].set_title(f"1. Input Binary Waveform ({N} bits)", fontsize=11)
axes[0].set_ylabel("Bit")
axes[0].set_xlim(0, N)
axes[0].set_ylim(-0.2, 1.2)
axes[0].set_yticks([0, 1])
axes[0].set_xticks(np.arange(0, N + 1, 5))
axes[0].grid(True, alpha=0.4)

# GRAPH 2: BPSK TRANSMITTED WAVEFORM
axes[1].step(t, tx_signal, where="post", linewidth=1.2)
axes[1].set_title("2. BPSK Transmitted Waveform", fontsize=11)
axes[1].set_ylabel("Voltage (V)")
axes[1].set_xlim(0, N)
axes[1].set_ylim(-1.5, 1.5)
axes[1].set_yticks([-1, 0, 1])
axes[1].set_xticks(np.arange(0, N + 1, 5))
axes[1].grid(True, alpha=0.4)

# GRAPH 3: RECEIVED SIGNAL WITH AWGN
axes[2].plot(
    t, rx_signal,
    linewidth=0.8,
    label="Received Signal"
)

# Ideal transmitted signal
axes[2].plot(
    t, tx_signal,
    linewidth=1.0,
    alpha=0.8,
    label="Ideal Tx Signal"
)

axes[2].set_title(
    f"3. Received Signal with AWGN (SNR = {snr_db} dB)",
    fontsize=11
)
axes[2].set_ylabel("Voltage (V)")
axes[2].set_xlim(0, N)
axes[2].set_xticks(np.arange(0, N + 1, 5))
axes[2].legend(loc="upper right")
axes[2].grid(True, alpha=0.4)

# GRAPH 4: SENT VS RECEIVED BIT COMPARISON
# Small offsets make both waveforms visible
sent_display = input_waveform + 0.15
received_display = received_waveform - 0.15

# Sent bits
axes[3].step(
    t, sent_display,
    where="post",
    linewidth=1.5,
    label="Sent Bits"
)

# Received bits
axes[3].step(
    t, received_display,
    where="post",
    linestyle="--",
    linewidth=1.5,
    label="Received Bits"
)

axes[3].set_title("4. Sent vs Received Bit Comparison", fontsize=11)
axes[3].set_xlabel("Time (bit periods)")
axes[3].set_ylabel("Bit Value")
axes[3].set_xlim(0, N)
axes[3].set_ylim(-0.5, 1.5)
axes[3].set_yticks([0, 1])
axes[3].set_xticks(np.arange(0, N + 1, 5))
axes[3].legend(loc="upper right")
axes[3].grid(True, alpha=0.4)

# Final graph layout
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# 10. OBSERVATION TABLE
print()
print("---------------------------------------------")
print("OBSERVATION TABLE")
print("---------------------------------------------")

print(
    "1. Input Binary Waveform      : "
    "40-bit binary representation of 'hello'."
)

print(
    "2. BPSK Transmitted Waveform : "
    "Bit 0 is represented by -1 V and bit 1 by +1 V."
)

print(
    "3. Received Signal            : "
    "AWGN noise is added during transmission."
)

print(
    "4. Sent vs Received           : "
    "Sent bits are compared with the recovered bits."
)

print("---------------------------------------------")

# 11. CONCLUSION
print()
print("CONCLUSION")

if bit_errors == 0:
    print(
        "The message 'hello' was successfully "
        "transmitted and recovered without any bit errors."
    )
else:
    print(
        "The message was recovered with some "
        "bit errors due to channel noise."
    )
