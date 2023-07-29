# 为英文WIN镜像添加中文语言包


- 问: 已有精简版的windows镜像，镜像中不含简体中文语言包，我要怎么样将中文语言包添加进去，再封装成ISO

- ChatGPT
为了将简体中文语言包添加到精简版的Windows镜像中，并将其重新封装为ISO文件，请按照以下步骤操作： 
1. 准备工具和文件：

a. 下载 Windows ADK（Windows Assessment and Deployment Kit）工具包，它包含用于自定义和部署Windows映像的工具。下载地址：[https://docs.microsoft.com/en-us/windows-hardware/get-started/adk-install](https://docs.microsoft.com/en-us/windows-hardware/get-started/adk-install) 

b. 下载简体中文语言包（请注意，选择与镜像相匹配的Windows版本）。语言包可以从以下链接下载：[https://www.microsoft.com/en-us/language](https://www.microsoft.com/en-us/language) 

c. 准备一个精简版的Windows镜像。 
2. 安装Windows ADK并选择Deployment Tools组件进行安装。 
3. 以管理员身份运行“部署和映像工具环境”。 
4. 将Windows镜像文件（install.wim）从原始ISO文件中提取出来。如果已有精简版的镜像文件，请跳过此步骤。 
5. 创建一个新的文件夹，用于存放提取出的Windows映像文件和语言包文件。 
6. 使用DISM（Deployment Image Servicing and Management）工具将Windows映像挂载到新创建的文件夹中：

```python
dism /Mount-Image /ImageFile:"<WIM文件路径>\install.wim" /Index:1 /MountDir:"<挂载目录路径>"
```



请将`<WIM文件路径>`替换为实际的WIM文件路径，将`<挂载目录路径>`替换为实际的挂载目录路径。 
7. 将简体中文语言包添加到挂载的Windows映像中：

```bash
dism /Image:"<挂载目录路径>" /Add-Package /PackagePath:"<语言包文件路径>"
```



请将`<挂载目录路径>`替换为实际的挂载目录路径，将`<语言包文件路径>`替换为实际的简体中文语言包文件路径。 
8. 等待操作完成后，卸载Windows映像并提交更改：

```bash
dism /Unmount-Image /MountDir:"<挂载目录路径>" /Commit
```



请将`<挂载目录路径>`替换为实际的挂载目录路径。 
9. 用新生成的install.wim文件替换原始ISO中的install.wim文件。可以使用任何支持编辑ISO文件的工具，例如PowerISO、UltraISO等。 
10. 保存修改后的ISO文件。

现在你已经成功地将简体中文语言包添加到了精简版的Windows镜像中，并重新封装成了ISO文件。在安装时，可以选择简体中文作为系统语言。

- 问: 完成以上步骤，系统默认设置是不是中文语言，默认“当前系统区域设置”是不是中文

- ChatGPT
完成以上步骤后，虽然已经将简体中文语言包添加到了Windows镜像中，但系统默认设置和“当前系统区域设置”仍然可能不是中文。要将默认设置更改为中文，您需要在安装过程中进行设置，或在系统安装完成后手动更改。

如果您希望在安装过程中将默认设置更改为中文，可以创建一个自动应答文件（autounattend.xml），并将其放置在安装媒体（如U盘、ISO文件）的根目录中。以下是一个简化的autounattend.xml示例，用于设置系统默认语言为简体中文：

```xml
<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
    <settings pass="oobeSystem">
        <component name="Microsoft-Windows-International-Core" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State">
            <InputLocale>zh-CN</InputLocale>
            <SystemLocale>zh-CN</SystemLocale>
            <UILanguage>zh-CN</UILanguage>
            <UserLocale>zh-CN</UserLocale>
        </component>
    </settings>
</unattend>
```



这个文件会在Windows安装过程中自动应用，将系统默认设置更改为简体中文。


- 问: 能不能在封装前设置好？

- ChatGPT
在封装前设置好默认语言为简体中文，需要修改Windows镜像中的注册表。以下是在封装前将默认设置更改为中文的方法： 
1. 在完成添加简体中文语言包的步骤之后，但在卸载Windows映像并提交更改之前，请执行以下命令，将注册表加载到一个临时位置：
```bash
reg load HKLM\TempHive "<挂载目录路径>\Windows\System32\config\SYSTEM"
```

请将`<挂载目录路径>`替换为实际的挂载目录路径。 
2. 使用以下命令更改默认输入法、系统语言、界面语言和用户区域设置：
```bash
reg add "HKLM\TempHive\ControlSet001\Control\Nls\Language" /v InstallLanguage /t REG_SZ /d 0804 /f
reg add "HKLM\TempHive\ControlSet001\Control\Nls\Locale" /v Default /t REG_SZ /d 00000804 /f
reg add "HKLM\TempHive\ControlSet001\Control\Nls\Locale" /v InstallLanguage /t REG_SZ /d 00000804 /f
reg add "HKLM\TempHive\ControlSet001\Control\Nls\Locale" /v SystemDefaultUILanguage /t REG_SZ /d 0804 /f
reg add "HKLM\TempHive\ControlSet001\Control\Nls\Locale" /v SystemLocale /t REG_SZ /d 00000804 /f
reg add "HKLM\TempHive\ControlSet001\Control\Nls\Locale" /v UserDefaultUILanguage /t REG_SZ /d 0804 /f
reg add "HKLM\TempHive\ControlSet001\Control\Nls\Locale" /v UserLocale /t REG_SZ /d 00000804 /f
```

3. 卸载临时位置的注册表：
```bash
reg unload HKLM\TempHive
```

4. 继续执行卸载Windows映像并提交更改的步骤：
```bash
dism /Unmount-Image /MountDir:"<挂载目录路径>" /Commit
```

请将`<挂载目录路径>`替换为实际的挂载目录路径。 
5. 用新生成的install.wim文件替换原始ISO中的install.wim文件，然后保存修改后的ISO文件。

完成这些步骤后，新生成的ISO文件将具有预先设置为简体中文的默认设置。在安装此镜像时，系统默认设置和“当前系统区域设置”将为简体中文。
