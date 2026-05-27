PRO MOSAICBATCH
  COMPILE_OPT IDL2
  ; 启动ENVI 5.1
  e = ENVI()
 
  ; 选择多个文件
  files = DIALOG_PICKFILE(/MULTIPLE, $
    TITLE = 'Select input scenes')


  FOR i=0, N_ELEMENTS(files)-1 DO BEGIN
    IF i MOD 4 EQ 0 THEN scenes = !NULL
    raster = e.OpenRaster(files[i],EXTERNAL_TYPE='eos_modis')
    scenes = [scenes, raster]

    
    IF i MOD 4 EQ 3 THEN BEGIN
      mosaicRaster = ENVIMosaicRaster(scenes,           $
        ;background = 0,                                       $
        ;feathering_distance = 20,                           $
        ;feathering_method = 'edge',                      $
        resampling = 'Cubic')

      newFile = "D:/paddy/MOD09A1/2017/"+STRMID(files[i], 9, 7)+"_"+STRMID(files[i], 31, 7);+".tif"
      mosaicRaster.Export, newFile, 'ENVI'
      print , newFile
      
      FOR j=0, 3 DO BEGIN
        scenes[j].close
      ENDFOR
      
    ENDIF
  ENDFOR
  
END