PRO test3
  COMPILE_OPT IDL2
  ; 启动ENVI 5.1
  e = ENVI()

  ; 选择多个文件
  files = DIALOG_PICKFILE(/MULTIPLE, $
    TITLE = 'Select input scenes')
    
    raster = e.OpenRaster(files[0],EXTERNAL_TYPE='landsat_hdf')
    
END

