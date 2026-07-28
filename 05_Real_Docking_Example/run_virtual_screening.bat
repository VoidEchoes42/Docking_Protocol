@echo off
echo ==================================================
echo   AutoDock Vina Virtual Screening Script
echo ==================================================
echo.

:: Note to student: This script assumes you have prepared the protein and 
:: all 10 ligands into PDBQT format inside a folder called 'prepared_files'

set PROTEIN=prepared_files\1HSG_receptor.pdbqt
set CONFIG=config.txt
set LIGAND_DIR=prepared_files\ligands
set OUTPUT_DIR=docking_results

:: Create output directory if it doesn't exist
if not exist %OUTPUT_DIR% mkdir %OUTPUT_DIR%

:: Clear the summary log file
set SUMMARY_LOG=screening_summary.txt
echo Docking Summary Results > %SUMMARY_LOG%
echo ======================= >> %SUMMARY_LOG%

:: Loop through every PDBQT ligand file in the ligand directory
for %%f in (%LIGAND_DIR%\*.pdbqt) do (
    echo Docking ligand: %%~nf
    
    :: Run Vina
    vina --receptor %PROTEIN% --ligand "%%f" --config %CONFIG% --out "%OUTPUT_DIR%\%%~nf_out.pdbqt" > "%OUTPUT_DIR%\%%~nf_log.txt"
    
    :: Optional: Extract the top score from the log file and save it to the summary
    echo Finished %%~nf. Check %OUTPUT_DIR%\%%~nf_log.txt for score. >> %SUMMARY_LOG%
    echo --------------------------------------------------
)

echo.
echo All docking runs complete! Check the '%OUTPUT_DIR%' folder for results.
pause
