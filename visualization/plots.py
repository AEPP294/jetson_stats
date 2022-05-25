import pandas as pd
import matplotlib.pyplot as plt
import argparse
from matplotlib.font_manager import FontProperties
import numpy as np


def main():
    pd.set_option("display.max_rows", 10, "display.max_columns", None)
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_data_file_path", type=str, help="enter path to raw data as argument")
    args = parser.parse_args()
    print('file to plot: ', args.raw_data_file_path)
    df = pd.read_csv(args.raw_data_file_path)

    # -- data preprocessing --
    # add sample column
    df['sample'] = df.index + 1
    df['sample'] = df['sample'] * 0.5

    #log2 transform gpu freq and gpu max freq
    df['LOG_GPU_FREQ'] = np.log2(df['GPU_FREQ'])
    df['LOG_GPU_MAX_FREQ'] = np.log2(df['GPU_MAX_FREQ'])
    nvp_model = df['nvp model'][0].split('_')
    mode, max_power, num_cores = [nvp_model[i] for i in range(len(nvp_model))]

    print('nvp_mode: ', mode, max_power, num_cores)
    # convert freq from kHz to MHz
    df.loc[:, 'CPU1freq'] = df.loc[:, 'CPU1freq'] / 1000
    df.loc[:, 'CPU2freq'] = df.loc[:, 'CPU2freq'] / 1000
    df.loc[:, 'CPU3freq'] = df.loc[:, 'CPU3freq'] / 1000
    df.loc[:, 'CPU4freq'] = df.loc[:, 'CPU4freq'] / 1000
    df.loc[:, 'CPU5freq'] = df.loc[:, 'CPU5freq'] / 1000
    df.loc[:, 'CPU6freq'] = df.loc[:, 'CPU6freq'] / 1000
    df.loc[:, 'GPU_FREQ'] = df.loc[:, 'GPU_FREQ'] / 1000
    df.loc[:, 'CPU6max_freq'] = df.loc[:, 'CPU6max_freq'] / 1000
    df.loc[:, 'GPU_MAX_FREQ'] = df.loc[:, 'GPU_MAX_FREQ'] / 1000000
    df.loc[:, 'power cur'] = df.loc[:, 'power cur'] / 1000
    df.loc[:, 'soc'] = df.loc[:, 'soc'] / 1000
    df.loc[:, 'cpu_gpu_cv'] = df.loc[:, 'cpu_gpu_cv'] / 1000

    max_gpu_freq = df['GPU_MAX_FREQ'][0]

    # map false values to 0 for engine enc/dec stats
    df["NVENC"].replace({"OFF": 0}, inplace=True)
    df["NVDEC"].replace({"OFF": 0}, inplace=True)
    # df["NVJPG"].replace({"OFF": 0}, inplace=True) if df['NVJPG']


    cols_to_drop = ['MTS FG', 'MTS BG', 'RAM', 'EMC', 'SWAP', 'APE', 'fan',
                    'jetson_clocks', 'power avg', 'uptime']

    df.drop(columns=cols_to_drop, inplace=True)

    # print columns
    # print("columns: ", df.columns)

    # graphs
    font1 = {'family': 'serif', 'color': 'black', 'size': 9}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}

    fig = plt.figure()
    fig.set_figheight(12)
    fig.set_figwidth(18)
    ax1 = plt.subplot2grid(shape=(7, 3), loc=(0, 0), colspan=3)
    ax2 = plt.subplot2grid(shape=(7, 3), loc=(1, 0), colspan=3)
    ax3 = plt.subplot2grid(shape=(7, 3), loc=(2, 0), colspan=3)
    ax4 = plt.subplot2grid(shape=(7, 3), loc=(3, 0), colspan=3)
    ax5 = plt.subplot2grid(shape=(7, 3), loc=(4, 0), colspan=3)
    ax6 = plt.subplot2grid(shape=(7, 3), loc=(5, 0), colspan=3)
    ax7 = plt.subplot2grid(shape=(7, 3), loc=(6, 0), colspan=3)

    # core temp graphs
    ax1.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'Temp AO'].astype(float), label='AO')
    ax1.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'Temp AUX'].astype(float), label='AUX')
    ax1.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'Temp CPU'].astype(float), label='CPU')
    ax1.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'Temp GPU'].astype(float), label='GPU')
    ax1.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'Temp thermal'].astype(float), label='thermal')
    fontP = FontProperties()
    fontP.set_size('xx-small')
    ax1.legend(loc=1, ncol=1, bbox_to_anchor=(0, 0, 1, 1),
               prop=fontP, fancybox=True, shadow=False, title=None)
    ax1.set_title('Temperature(˚C) vs time', fontdict=font1)
    ax1.set_ylabel('temp (˚C)')

    ax1.grid(color='green', linestyle='--', linewidth=0.5)
    ax1.set_ylim([-1, 101])
    ax1.set_yticks([0, 25, 50, 75, 100])
    ax1.axes.get_xaxis().set_ticklabels([])

    # cpu usage vs time graph
    ax2.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU1'].astype(float), label='core1')
    ax2.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU2'].astype(float), label='core2')
    ax2.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU3'].astype(float), label='core3')
    ax2.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU4'].astype(float), label='core4')
    ax2.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU5'].astype(float), label='core5')
    ax2.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU6'].astype(float), label='core6')
    ax2.legend(loc=1, ncol=1, bbox_to_anchor=(0, 0, 1, 1),
               prop=fontP, fancybox=True, shadow=False, title=None)
    ax2.set_title('CPU-core(% used) vs time', fontdict=font1)
    ax2.set_ylabel('CPU-core(% used)')

    ax2.grid(color='green', linestyle='--', linewidth=0.5)
    ax2.set_ylim([-1, 109])
    ax2.set_yticks([0,25, 50, 75, 100])
    ax2.axes.get_xaxis().set_ticklabels([])

    # CPU core freq vs sample
    ax3.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU1freq'].astype(float), label='core1')
    ax3.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU2freq'].astype(float), label='core2')
    ax3.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU3freq'].astype(float), label='core3')
    ax3.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU4freq'].astype(float), label='core4')
    ax3.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU5freq'].astype(float), label='core5')
    ax3.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU6freq'].astype(float), label='core6')
    ax3.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'CPU6max_freq'].astype(float), label='cpu_max_freq')
    ax3.legend(loc=1, ncol=1, bbox_to_anchor=(0, 0, 1, 1),
               prop=fontP, fancybox=True, shadow=False, title=None)
    ax3.set_title('CPU-core freq vs time', fontdict=font1)
    ax3.set_ylim([0, df.loc[:, 'CPU6max_freq'][0].astype(float)+100])
    ax3.set_yticks([0, 500, 1000, 1500])
    ax3.set_ylabel('CPU-freq(MHz)')

    ax3.grid(color='green', linestyle='--', linewidth=0.5)
    ax3.axes.get_xaxis().set_ticklabels([])

    # GPU (% used) vs sample
    ax4.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'GPU'].astype(float), label='GPU')
    ax4.legend(loc=1, ncol=1, bbox_to_anchor=(0, 0, 1, 1),
               prop=fontP, fancybox=True, shadow=False, title=None)
    ax4.set_title('GPU (% used) vs time', fontdict=font1)
    ax4.set_ylabel('GPU (% used)')
    ax4.grid(color='green', linestyle='--', linewidth=0.5)
    ax4.set_ylim([-1, 109])
    ax4.set_yticks([0,25, 50, 75, 100])
    ax4.axes.get_xaxis().set_ticklabels([])

    # GPU freq
    ax5.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'GPU_FREQ'].astype(float), label='GPU_FREQ')
    ax5.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'GPU_MAX_FREQ'].astype(float), label='GPU_MAX_FREQ')
    ax5.legend(loc=1, ncol=1, bbox_to_anchor=(0, 0, 1, 1),
               prop=fontP, fancybox=True, shadow=False, title=None)
    ax5.set_title('GPU freq(MHz) vs time', fontdict=font1)
    ax5.set_ylabel('GPU freq (MHz)')
    ax5.set_ylim([-1, max_gpu_freq+100])
    ax5.grid(color='green', linestyle='--', linewidth=0.5)
    ax5.axes.get_xaxis().set_ticklabels([])

    ax6.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'power cur'].astype(float), label='power_curr_all')
    ax6.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'soc'].astype(float), label='power_curr_soc')
    ax6.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'cpu_gpu_cv'].astype(float), label='power_curr_cpu_gpu_cv')
    ax6.set_title('Power(W) vs time', fontdict=font1)
    ax6.legend(loc=1, ncol=1, bbox_to_anchor=(0, 0, 1, 1),
               prop=fontP, fancybox=True, shadow=False, title=None)
    ax6.set_ylabel('power (W)')
    ax6.grid(color='green', linestyle='--', linewidth=0.5)
    ax6.set_ylim([-1, float(max_power[0:2])+1])
    ax6.set_yticks([0,5, 10, 15])
    ax6.axes.get_xaxis().set_ticklabels([])

    # graph 7
    ax7.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'NVENC'].astype(float), label='NVENC')
    ax7.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'NVDEC'].astype(float), label='NVDEC')
    # ax7.plot(df.loc[:, 'sample'].astype(float), df.loc[:, 'NVJPG'].astype(float), label='NVJPG')
    ax7.set_title('HW Engine Freq(MHz) vs time', fontdict=font1)
    ax7.legend(loc=1, ncol=1, bbox_to_anchor=(0, 0, 1, 1),
               prop=fontP, fancybox=True, shadow=False, title=None)
    ax7.set_ylabel('freq (MHz)')
    ax7.set_xlabel('time(s)')
    ax7.grid(color='green', linestyle='--', linewidth=0.5)
    ax7.set_yticks([0,250, 500, 750, 1000])
    ax7.set_ylim([-50, 1000+50])

    temp = args.raw_data_file_path.split('/')[-1].replace('.csv', '')
    # display plots
    plt.suptitle("Jtop Plots - Thermal Chamber at {0}\n{1}{2}{3}".format(temp, mode+':', max_power+'-', num_cores), fontdict=font2)
    path = args.raw_data_file_path
    new = path.split('/')
    new_path = new[0:len(new)-1]
    file_name = new[-1].split('.')[0]
    # print('filename', file_name)
    # print(new_path)
    final = '/'.join(new_path)
    # print(final)
    # print(final+file_name, 'final+filename')
    # plt.show()
    plt.savefig(final+'/'+file_name+'.png', format='png')
    print('Plot saved in directory: ' + final + '/')


if __name__ == "__main__":
    main()
