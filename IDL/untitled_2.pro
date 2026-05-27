pro untitled_2
  ; 启动ENVI 5.1
  e = ENVI()
 
  ; 选择多个文件
  files = DIALOG_PICKFILE(/MULTIPLE, $
    TITLE = 'Select input scenes')
  scenes = !NULL
  ; 将每一个Raster放在一个Scenes中
  FOR i=0, N_ELEMENTS(files)-1 DO BEGIN
    print,files[i]
    raster = e.OpenRaster(files[i],EXTERNAL_TYPE='eos_modis')
    scenes = [scenes, raster]
  ENDFOR
  
  FOR i=0,1 DO BEGIN
    scenes[i].close
  ENDFOR

END


