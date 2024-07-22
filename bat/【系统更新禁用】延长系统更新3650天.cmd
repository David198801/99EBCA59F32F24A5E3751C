@echo off
chcp 65001 
echo ------------------------------------------------------------------------------------------------------------
echo 通过延长Windows暂停更新的时间上限，长时间禁用Windows更新，不影响微软商店和其他系统设置正常使用
echo -----------------------------------------------------------
echo 【按下任意键】开始创建"FlightSettingsMaxPauseDays"值
echo -----------------------------------------------------------
pause

echo -------------------------------------
echo 正在更改自动更新暂停上限为3650天
echo -------------------------------------
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" /v "FlightSettingsMaxPauseDays" /t REG_DWORD /d "3650" /f
echo ------------------------------------------------------------------------------------
echo 已在“计算机/HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings”目录创建并修改"FlightSettingsMaxPauseDays"值为3650，请【按下任意键】打开Windows更新设置开启暂停更新
echo ------------------------------------------------------------------------------------
echo 【Win10系统】在设置“更新与安全”中进入“高级选项”把“暂停选项”调整至上限日期
echo 【Win11系统】在设置“Windows更新”中把“暂停更新”延长至上限周期
echo BiliBili：墨竹Maxim
pause

chcp 936
start ms-settings:windowsupdate
