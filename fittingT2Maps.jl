using MAT
using NIfTI
using LsqFit
using Statistics
using Plots
using NaturalSort

T = Float64

## This script uses NIFTI files created from the DICOMs using dcm2niix.

## Data folder: points to the folder with the NIFTI files
# Check if a command-line argument was provided
if length(ARGS) < 1
    println("Please provide the data directory.")
    exit(1)
end


# Check if a command-line argument was provided
if length(ARGS) < 2
    println("Please provide the db.")
    exit(1)
end


# Check if a command-line argument was provided
if length(ARGS) < 3
    println("Please provide the nifit dir, db and mapdir.")
    exit(1)
end

# Use the first command-line argument as the data directory
datadir = ARGS[1]


# Use the second command-line argument as the file path
filepath = ARGS[2]

db = matread(filepath)


## Create output folders
mapdir = ARGS[3]
if !isdir(mapdir)
    mkdir(mapdir)
end

filedir = readdir(datadir)
filedir = sort(filedir, lt=natural)

## Concatenate T2 images
catfiles = Vector{Array{T, 3}}(undef, 7)
ni_header = []
global i = 1
for file in filedir
    if occursin(".nii", file) && !occursin("._", file)
        catfiles[i] = collect(niread(joinpath(datadir,file)))
        ni_header = niread(joinpath(datadir,file), mmap=true)
        ni_header = ni_header.header
        i += 1
    end
end

catfiles = cat(catfiles...,dims=4)

## Write recon matrix to nii
function img2nii(Volume, header, FileName)
    # initialize NIfTI structure
    NiVolume = NIVolume(Volume)

    # Set header
    NiVolume.header.pixdim = header.pixdim
    NiVolume.header.srow_x = header.srow_x
    NiVolume.header.srow_y = header.srow_y
    NiVolume.header.srow_z = header.srow_z
    NiVolume.header.sform_code = header.sform_code
    NiVolume.header.qform_code = header.qform_code
    NiVolume.header.qoffset_x = header.qoffset_x
    NiVolume.header.qoffset_y = header.qoffset_y
    NiVolume.header.qoffset_z = header.qoffset_z
    NiVolume.header.quatern_b = header.quatern_b
    NiVolume.header.quatern_c = header.quatern_c
    NiVolume.header.quatern_d = header.quatern_d

    # write file
    niwrite(FileName, NiVolume)
end

# -------------------------------------------------------
## Mono-exp fitting 
TE = collect(10e-3:10e-3:70e-3)

@. model(TE, p) = p[1] * exp(-TE / p[2])
M0 = similar(catfiles[:,:,:,1])
T2 = similar(M0)
Threads.@threads for vox in CartesianIndices(catfiles[:,:,:,1])
    fit = curve_fit(model, TE, catfiles[vox,:], [catfiles[vox,1], 0.1])
    M0[vox] = fit.param[1]
    T2[vox] = fit.param[2]
end

heatmap(T2[:,:,15]', clims=(0,0.2))
img2nii(T2, ni_header, "$mapdir/T2_MAPS_MONOEXP.nii")

# -------------------------------------------------------
## Mono-exp fitting without the first echo
@. model(TE, p) = p[1] * exp(-TE / p[2])
M0 = similar(catfiles[:,:,:,1])
T2 = similar(M0)
Threads.@threads for vox in CartesianIndices(catfiles[:,:,:,1])
    fit = curve_fit(model, TE[2:end], catfiles[vox,:][2:end], [catfiles[vox,1], 0.1])
    M0[vox] = fit.param[1]
    T2[vox] = fit.param[2]
end

heatmap(T2[:,:,15]', clims=(0,0.2))

img2nii(T2, ni_header, "$mapdir/T2_MAPS_MONOEXP_W1ECHO.nii")

# -------------------------------------------------------
## Fitting EMC
## T2 maps and B1 maps are calculated as fitting to the EMC dictionary.

## Load the db

expEMC = reshape(catfiles, :, 7) 

simEMC = T.(reshape(db["echo_train_modulation"], :, Int(db["ETL"]))')
simEMC ./= sqrt.(sum(simEMC.^2, dims=1))

## Find the max correlation for each row
function max_mul!(pos, expEMC, simEMC)
    Threads.@threads for i ∈ axes(expEMC, 1)
        pos[i] = argmax(transpose(expEMC[i,:]) * simEMC)
    end
    return pos
end

pos = Vector{CartesianIndex}(undef,size(expEMC,1))
max_mul!(pos, expEMC, simEMC)

pos = [pos[i][2] for i in axes(expEMC,1)]

## Convert linear indices to cartesian
function ind2subv(shape, indices)
    CI = CartesianIndices(shape)
    return getindex.(Ref(CI), indices)
end

maps_idx = ind2subv((length(db["B1_scaling_arr"]), length(db["T2_tse_arr"])),pos)
b1ind = [maps_idx[i][1] for i in axes(maps_idx,1)]
t2ind = [maps_idx[i][2] for i in axes(maps_idx,1)]

T2 = reshape(db["T2_tse_arr"][t2ind], size(catfiles)[1:3])

heatmap(T2[:,:,15]', clims=(0,0.2))

B1 = reshape(db["B1_scaling_arr"][b1ind], size(catfiles)[1:3])
R2 = 1 ./ T2

img2nii(T2, ni_header, "$mapdir/T2_MAPS_EMC.nii")
img2nii(B1, ni_header, "$mapdir/B1_MAPS.nii")
img2nii(R2, ni_header, "$mapdir/R2_MAPS_EMC.nii")

