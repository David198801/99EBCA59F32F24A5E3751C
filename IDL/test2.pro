pro test2
  COMPILE_OPT IDL2
  ; 启动ENVI 5.1
  e = ENVI()
 
  ; 选择多个文件
  files = DIALOG_PICKFILE(/MULTIPLE, $
    TITLE = 'Select input scenes')

;scenes = !NULL
  FOR i=0, N_ELEMENTS(files)-1 DO BEGIN
    IF i MOD 4 EQ 0 THEN scenes = !NULL
    raster = e.OpenRaster(files[i],EXTERNAL_TYPE='eos_modis')
    scenes = [scenes, raster]

    
    IF i MOD 4 EQ 3 THEN BEGIN

      newFile = "D:/paddy/MOD09A1/2017/"+STRMID(files[i], 9, 7)+"_"+STRMID(files[i], 31, 7)

      print , newFile
      
      FOR j=0, 3 DO BEGIN
        scenes[j].close
        ;scenes[i-3+j].close scenes赋空在外面
        ;print , "close"
      ENDFOR
      
    ENDIF
  ENDFOR
  

end