import numpy as np
from constants import SAMPLING_FREQ
from scipy.signal import butter, filtfilt


def eeg_data_convert(data, eeg_data_len):
    EEG_data = np.zeros((8, eeg_data_len))
    for j in range(eeg_data_len):
        data1 = data[58 * j : 58 * j + 58]
        head1 = data1[0:2]
        head2 = data1[4:6]
        head3 = data1[6:8]

        if head1 == "55" and head2 == "01" and head3 == "18":
            for i in range(8):
                L_16 = data1[8 + 6 * i : 10 + 6 * i]
                M_16 = data1[10 + 6 * i : 12 + 6 * i]
                H_16 = data1[12 + 6 * i : 14 + 6 * i]
                L_10 = int(L_16, 16)
                M_10 = int(M_16, 16)
                H_10 = int(H_16, 16)
                one_data = float(
                    (np.int32(H_10) & 127) * 65536
                    + (np.int32(M_10) & 255) * 256
                    + (np.int32(L_10) & 255)
                )
                if H_10 > 127:
                    one_data = one_data - 8388608
                EEG_data[i, j] = one_data / 8388608 * 7487.27
    return EEG_data


def band_filter(data, low_freq, high_freq):
    f_order = 4
    npy = 0.5 * SAMPLING_FREQ
    low = low_freq / npy
    high = high_freq / npy
    b, a = butter(f_order, [low, high], btype="band")
    data = filtfilt(b, a, data)

    return data
