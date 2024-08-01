
![rubbersnake](https://github.com/user-attachments/assets/dbd5e94e-8715-4a7c-8f70-a52b2d041aac)

# Installation
## Installing MiKTeX
- MiKTeX can be installed on Windows, Linux and macOS via the installers available on the MiKTeX download page: https://miktex.org/download
- When running the MiKTeX installer it is reccomended to use default install settings. For Windows, this should set the default target directory to `C:\Users\username\AppData\Local\Programs\MiKTeX\miktex\bin\x64`. By default, rubbersnake expects this path when looking for the compiler.
- When prompted, select the option to allow MiKTeX to install missing TeX packages automatically. By default, this is set to propmt user for permission before installing - This will also work but may cause difficulties when compiling from Python. 
  - If default installation is not used, the target directory path can be found by navigating to Settings > Directories in the MiKTeX Console.
- After installation, open MiKTeX Console and update all installed packages. Failure to do so may result in compile failures. 

# Usage
## Setup
### Source Directory
