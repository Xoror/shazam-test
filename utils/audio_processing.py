import librosa
import numpy as np
import matplotlib.pyplot as plt

y, sr = librosa.load("d:\\Cass Coding\\Repos\\shazam-test\\uploads\\Savant - Redemption.mp3", sr=8192)
S = np.abs(librosa.stft(y))

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

Pxx, freqs, bins, im = ax2.specgram(y, NFFT=1024, Fs=1/0.0005)
# The `specgram` method returns 4 objects. They are:
# - Pxx: the periodogram
# - freqs: the frequency vector
# - bins: the centers of the time bins
# - im: the .image.AxesImage instance representing the data in the plot
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Frequency (Hz)')
ax2.set_xlim(0, 20)

plt.show()