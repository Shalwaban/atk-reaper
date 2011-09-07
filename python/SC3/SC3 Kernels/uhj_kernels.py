# ****************************************************************************
# UHJ decoder kernels
# 
# Generate a set of kernels suitable for decoding b-format
# to UHJ stereo.
#
# Kernels are classified by kernel size, N, and stored in directory: 
#
#       'ATK_kernels/FOA/decoders/UHJ/SR_00None/N_[kernel_size]/'
#
# Within, three [W,X,Y] two channel [L,R] kernels are found, named:
#
#       'UHJ_W', 'UHJ_X', 'UHJ_Y'
#
# A resulting UHJ decode can be generated from these kernels as follows:
#
#       uhj = 'UHJ_W' * W + 'UHJ_X' * X + 'UHJ_Y' * Y
#
#   where * is convolution, + is sum.
#
# ****************************************************************************

from muse import *
import os

# params
srs         = array([None])                     # sample rates (UHJ = none!)
Ns          = array([512, 1024, 2048, 4096, 8192])    # kernel lengths


file_type   = 'wav'         # write file...
#encoding    = 'pcm24'
encoding    = 'pcm32'
endianness  = 'file'


target_dir  = '/Volumes/Audio/test'      #temp write dir
file_dir    = '/ATK_kernels/FOA/decoders/UHJ'

file_names  = ['UHJ_W', 'UHJ_X', 'UHJ_Y']

subject_ids = ['0000']                  # only one subject


# ----- loop
for sr in srs:                          # SR
    for N in Ns:                        # kernel sizes

        for subject_id in subject_ids:

            # ----- generate decoder kernels
            decoder_kernels = uhj_decoder_kernel(N)

            # ----- generate file names
            write_files = []
            for name in file_names:
                write_files += [
                    target_dir + file_dir + \
                    '/SR_' + str(sr).zfill(6) + '/N_' + str(N).zfill(4) + '/' + \
                     subject_id + '/' + name + '.' + file_type[:3]
                    ]

            # ----- write out decoder kernels
            for i in range(len(write_files)):

                # ************************************************************
                # Set up sndfiles for writing:

                if not os.path.exists(os.path.dirname(write_files[i])):
                    os.makedirs(os.path.dirname(write_files[i]))
                
                write_sndfile = Sndfile(
                    write_files[i],
                    'w',
                    Format(file_type, encoding, endianness),
                    nchannels(decoder_kernels[i]),
                    int(sr or 44100)                    # sr defaults to 44100
                    )                                   # if none is supplied

                # ----- write out!
                write_sndfile.write_frames(decoder_kernels[i])

                # ----- close file
                write_sndfile.close()
