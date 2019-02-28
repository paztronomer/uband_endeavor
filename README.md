# Skytemplates for u-band

## 1) For selection of exposures
I selected public data from NOAO, which combined with DES data is the dataset I'm working with. Data range is 20170102 to 20190116.

All the exposures where processed under **reqnum=4083**

I used number of objects vs exposure time as an indicator. Using the script `plot_nobjects.py`, 536 exposures were selected, as plotted on `nobj_exptime_r4083.png`. There is a SQL script to query for number of objects per exposure (`query_nobjects_exptime_r4083.sql`). As this selection had many exposures with issues, I made sub-selections, as listed on different files under `skypca/`:

| filename | N exposures | source of exposures | comments |
| :------- | :---------: |:------------------- | :------- |
| explist_all_536.csv | 536 | raw initial selection | many bad exposures |
| explist_sel1.csv | 454 | removed exposures from above set | contains good and bad exposures |
| explist_sel2.csv | 237 | removed exposures having artifacts and gas-regions | much more restricted set |  
| explist_sel4.csv | 127 | hand picked exposures with `exptime >= 360 s` | not widely representative |

### 1.1) Local copy of binned_fp files
Under `skypca/binned_fp/` there is a copy of the "sel2" and "sel4" sets.

## 2) Running creation of PCA
First, setup the proper stack (Y2Nstack 1.0.6+14). Use the script `y2n_fermi.sourceme`

To run the code `sky_pca`, a text file containing the paths to the files is needed, besides the directories `config/` and `log/`. For my runs I used the files `skypca/bleedmask_binned_fp_*`, coantaining the paths to the local copies of the binned focal plane images.

A typical run of the code is 
```
sky_pca -i explist_sel4.csv -o pca_Y2stack_u_RMS0p03_n04.fits -n 4 --reject_rms 0.03 -s config/u_Y2stack_RMS0p03_n04.config -l log/u_Y2stack_RMS0p03_n04.log -v
````
Or you can use the bash script `run_setRMS_skypca_local.sh` which runs over a set of different RMS values.

### 2.1) Results: PCA files
Fora all the above datasets I tried Y2 and Y5 stacks (Y2Nstack 1.0.6+12, Y2Nstack 1.0.6+14, Y5A1dev+12), with a set of different RMS values: (0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08). For a set I also tried to expand to 8 principal components, but it still gave the binned feature on the full-size solution.

The RMS showing the *less bad* solution was 0.03, but still produced the binned 128x128 pix blocks on the full-size sky template solution.

The results (FITS files) for the sets "sel2" and "sel4" (see above table) are stored under `skypca/pca_{sel2, sel4}/`. The naming is **pca_{used stack}\_{selection}\_u\_{RMS value}\_n{number of PCA components}.fits**

Note that a healthy PCA solution should look like `OPS/cal/skytemp/20140801t1130-r1635/p02/binned-fp/Y2A1_20140801t1130_u_r1635p02_skypca-binned-fp.fits` Where each of the 4 components has its own defined soft gradient behavior.

## 3) Fix to run sky_template
As `sky_template` code performs a check to make sure all the exposures to be used have the same set of calibrations, then a hack needs to be done to overcome it. The reason is our time range spans more than one epoch.

On a local copy of `sky_template.py` change the following lines inside the call of class SkyTemplate(PixCorrectDriver):
```
try:
    items_must_match(hdr, usehdr, 'BAND','CCDNUM','FLATFIL')
except:
    return 1
```
for the following
```
try:
    items_must_match(hdr, usehdr, 'BAND','CCDNUM','FLATFIL')
except:
    t_e = 'Mismatch: '
    if (hdr['BAND'] != usehdr['BAND']):
        t_e += 'Band. ref:{0}'.format(hdr['BAND'])
        t_e += ' vs '
        t_e += 'current:{0}'.format(usehdr['BAND'])
    elif (hdr['CCDNUM'] != usehdr['CCDNUM']):
        t_e += 'CCD. ref:{0}'.format(hdr['CCDNUM'])
        t_e += ' vs current:'
        t_e += '{0}'.format(usehdr['CCDNUM'])
    elif (hdr['FLATFIL'] != usehdr['FLATFIL']):
        t_e += 'Flat.'
        t_e += ' ref:{0}'.format(hdr['FLATFIL'])
        t_e += ' vs current:'
        t_e += '{0}'.format(usehdr['FLATFIL'])
    else:
        t_e = 'Unknown mismatch error.'
    logger.error(t_e)
```

This should take care of the issue.

### Directories
* `ingredients_processing/`: scripts and files for processing ingredients to be used
* `skypca`: files for creating PCA solutions, results having issues, and binned images to be used as ingredients.
