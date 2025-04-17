
--ADC_Data file path
info = debug.getinfo(1,'S');
file_path = (info.source);
file_path = string.gsub(file_path, "@","");
file_path = string.gsub(file_path, "DataCaptureDemo_xWR.lua","");
data_path     = file_path.."..\\PostProc"
adc_data_path = data_path.."\\adc_datatest2.bin"
partId = 1843


-- Define the Python script you want to run
local pythonScript = "python C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\ultrasuite_script.py"
-- Function to run the Python script
local function runPythonScript(testscript)
    local result = os.execute(testscript)

	if result == 0 then
		print("Python script executed successfully")
	else
		print("Error executing Python script" .. result)
	end

end


if (ar1.ChanNAdcConfig(1, 1, 0, 1, 1, 1, 1, 2, 1, 0) == 0) then
    WriteToLog("ChanNAdcConfig Success\n", "green")
else
    WriteToLog("ChanNAdcConfig failure\n", "red")
end

if (partId == 1642) then
    if (ar1.LPModConfig(0, 1) == 0) then
        WriteToLog("LPModConfig Success\n", "green")
    else
        WriteToLog("LPModConfig failure\n", "red")
    end
else
    if (ar1.LPModConfig(0, 0) == 0) then
        WriteToLog("Regualar mode Cfg Success\n", "green")
    else
        WriteToLog("Regualar mode Cfg failure\n", "red")
    end
end

if (ar1.RfInit() == 0) then
    WriteToLog("RfInit Success\n", "green")
else
    WriteToLog("RfInit failure\n", "red")
end

RSTD.Sleep(1000)

if (ar1.DataPathConfig(1, 1, 0) == 0) then
    WriteToLog("DataPathConfig Success\n", "green")
else
    WriteToLog("DataPathConfig failure\n", "red")
end

if (ar1.LvdsClkConfig(1, 1) == 0) then
    WriteToLog("LvdsClkConfig Success\n", "green")
else
    WriteToLog("LvdsClkConfig failure\n", "red")
end

if((partId == 1642) or (partId == 1843) or (partId == 6843)) then
    if (ar1.LVDSLaneConfig(0, 1, 1, 0, 0, 1, 0, 0) == 0) then
        WriteToLog("LVDSLaneConfig Success\n", "green")
    else
        WriteToLog("LVDSLaneConfig failure\n", "red")
    end
elseif ((partId == 1243) or (partId == 1443)) then
    if (ar1.LVDSLaneConfig(0, 1, 1, 1, 1, 1, 0, 0) == 0) then
        WriteToLog("LVDSLaneConfig Success\n", "green")
    else
        WriteToLog("LVDSLaneConfig failure\n", "red")
    end
end



if((partId == 1642) or (partId == 1843)) then
    if(ar1.ProfileConfig(0, 77, 100, 6, 60, 0, 0, 0, 0, 0, 0, 29.982, 0, 256, 10000, 0, 0, 30) == 0) then
        WriteToLog("ProfileConfig Success\n", "green")
    else
        WriteToLog("ProfileConfig failure\n", "red")
    end
elseif((partId == 1243) or (partId == 1443)) then
    if(ar1.ProfileConfig(0, 77, 100, 6, 60, 0, 0, 0, 0, 0, 0, 29.982, 0, 256, 10000, 0, 0, 30) == 0) then
        WriteToLog("ProfileConfig Success\n", "green")
    else
        WriteToLog("ProfileConfig failure\n", "red")
    end
elseif(partId == 6843) then
    if(ar1.ProfileConfig(0, 60.25, 100, 6, 60, 0, 0, 0, 0, 0, 0, 29.982, 0, 256, 10000, 0, 131072, 30) == 0) then
		WriteToLog("ProfileConfig Success\n", "green")
    else
        WriteToLog("ProfileConfig failure\n", "red")
    end
end

if (ar1.ChirpConfig(0, 0, 0, 0, 0, 0, 0, 1, 1, 0) == 0) then
    WriteToLog("ChirpConfig Success\n", "green")
else
    WriteToLog("ChirpConfig failure\n", "red")
end


--3. frame sayısı
--4. chirp sayısı
--5. periodicity in ms
-- ((0, 0, 100, 1, 1, 0, 0, 0)) produces 100 ms frame as total.
if (ar1.FrameConfig(0, 0, 100, 1, 1, 0, 0, 0) == 0) then
    WriteToLog("FrameConfig Success\n", "green")
else
    WriteToLog("FrameConfig failure\n", "red")
end

-- select Device type
if (ar1.SelectCaptureDevice("DCA1000") == 0) then
    WriteToLog("SelectCaptureDevice Success\n", "green")
else
    WriteToLog("SelectCaptureDevice failure\n", "red")
end

--DATA CAPTURE CARD API
if (ar1.CaptureCardConfig_EthInit("192.168.33.30", "192.168.33.180", "12:34:56:78:90:12", 4096, 4098) == 0) then
    WriteToLog("CaptureCardConfig_EthInit Success\n", "green")
else
    WriteToLog("CaptureCardConfig_EthInit failure\n", "red")
end

--AWR12xx or xWR14xx-1, xWR16xx or xWR18xx or xWR68xx- 2 (second parameter indicates the device type)
if ((partId == 1642) or (partId == 1843) or (partId == 6843)) then
    if (ar1.CaptureCardConfig_Mode(1, 2, 1, 2, 3, 30) == 0) then
        WriteToLog("CaptureCardConfig_Mode Success\n", "green")
    else
        WriteToLog("CaptureCardConfig_Mode failure\n", "red")
    end
elseif ((partId == 1243) or (partId == 1443)) then
    if (ar1.CaptureCardConfig_Mode(1, 1, 1, 2, 3, 30) == 0) then
        WriteToLog("CaptureCardConfig_Mode Success\n", "green")
    else
        WriteToLog("CaptureCardConfig_Mode failure\n", "red")
    end
end

if (ar1.CaptureCardConfig_PacketDelay(25) == 0) then
    WriteToLog("CaptureCardConfig_PacketDelay Success\n", "green")
else
    WriteToLog("CaptureCardConfig_PacketDelay failure\n", "red")
end

for i = 10,1,-1 
do 	
  print("-----------------------------------------------------")
  
end



-- Define the list
consonants = {'b'}
-- {'a', 'e', 'i','o', 'y'}


-- Loop 20 times
for count = 1, 2 do
    -- Iterate through the list using ipairs
    for _, consonant in ipairs(consonants) do
       
		RSTD.Sleep(3000)
		adc_data_path = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\PostProc\\consonants_correct\\" ..consonant.. "\\adc_data_" ..count.. ".bin" 
		--adc_data_path = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\PostProc\\vowels_correct\\" ..vowel.. "\\T4\\adc_data_" ..count.. ".bin" 

		--Start Record ADC data
		ar1.CaptureCardConfig_StartRecord(adc_data_path, 1)
		RSTD.Sleep(1000)
        ar1.StartFrame()
        runPythonScript(pythonScript)
		

		print("-----------------------------------------------------")
		print("------------------------------3 SECONDS TO GET STARTED DOSYA " ..count.. "-----------------------")
		RSTD.Sleep(2500)
		
		RSTD.Sleep(100)
		--RSTD.Sleep(4000)
		--RSTD.Sleep(20000)
    end
end

-- for i = 1,3,1 
-- do 

  -- RSTD.Sleep(3000)
  -- adc_data_path = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\PostProc\\vowels_correct\\test\\S1\\adc_data_" ..i.. ".bin" 
  -- --Start Record ADC data
  -- ar1.CaptureCardConfig_StartRecord(adc_data_path, 1)
  -- RSTD.Sleep(1000)

  -- print("-----------------------------------------------------")
  -- print("------------------------------3 SECONDS TO GET STARTED DOSYA " ..i.. "-----------------------")
  -- RSTD.Sleep(3000)
  -- runPythonScript(pythonScript)

  -- ar1.StartFrame()
  -- RSTD.Sleep(4000)

-- end




--Start Record ADC data
-- ar1.CaptureCardConfig_StartRecord(adc_data_path, 1)
-- RSTD.Sleep(1000)

-- --Trigger frame
-- ar1.StartFrame()
-- RSTD.Sleep(5000)

--Post process the Capture RAW ADC data
-- ar1.StartMatlabPostProc(adc_data_path)
-- WriteToLog("Please wait for a few seconds for matlab post processing .....!!!! \n", "green")
-- RSTD.Sleep(10000)
