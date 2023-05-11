import helper
import subprocess

def plot_compare(samplings, max_freq, microlog_lines, to_plot, fft_amplitude_unit = helper.FftUnit.ACE):

    signals = []

    for sample in samplings:

        # Read data
        sampling = []

        if sample["acquisition_source"] == helper.AcquisitionDevice.MODULE_ADS127:
            sampling = helper.read_ads127_sampling(sample["sampling_path"], sample["pga"], True)

        elif sample["acquisition_source"] == helper.AcquisitionDevice.MICROLOG:
            sampling = helper.read_csv_data(sample["sampling_path"], ";", True)

        # Filter and downsampling
        sampling_vars = helper.SamplingVariables(max_freq, microlog_lines)

        if "oversampling_freq" in sample:
            sampling_vars = helper.SamplingVariables(max_freq, microlog_lines, sample["oversampling_freq"])
            sampling = helper.downsampling_conditioning(sampling, sampling_vars)

        # Calculate fft and global value
        fft = helper.generate_fft(sampling, sampling_vars, fft_amplitude_unit)
        global_value = helper.calculate_global_value(fft)
        print("the Global Vaule is =", global_value)
 

##### FIELD MEASUREMENT PARAMETERS #####
maquina = "p1"
microlog_punto = "3"
ads127_punto = "1"
freq =500
microlog_lines = 1600
CH="CH1"
on="ons"
comp="st4"
 
###### PATH #######

ads127_path_0=f"/home/pi/python_script_GV/p1_CH0_500hz.csv"
ads127_path_1=f"/home/pi/python_script_GV/p1_CH0_1000hz.csv"

#### HOME TEST #####

ads127_rpi4_0 = {
    "label": f"{maquina}{CH}, fuente interna off mux",
    "sampling_path": ads127_path_0,
    "acquisition_source": helper.AcquisitionDevice.MODULE_ADS127,
    "pga": helper.PgaAds127.M_3DB,        # M_3DB, P_6DB ,P_13DB
    "oversampling_freq": 128000
}

ads127_rpi4_1= {
    "label": f"{maquina}{CH}, fuente interna off mux",
    "sampling_path": ads127_path_1,
    "acquisition_source": helper.AcquisitionDevice.MODULE_ADS127,
    "pga": helper.PgaAds127.M_3DB,        # M_3DB, P_6DB ,P_13DB
    "oversampling_freq": 128000
}



##### HOME TEST ######
subprocess.run("./cpp_program")
to_compare = [ads127_rpi4_0]
plot_compare(to_compare,500, microlog_lines, helper.Plot.FFT)
to_compare = [ads127_rpi4_1]
plot_compare(to_compare,1000, microlog_lines, helper.Plot.FFT)