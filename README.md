# project_01: LED Music Visualizer
Project proposal in docs directory
Link to Hackster.io page with build and operation instructions: https://www.hackster.io/juliana-wang/pocketbeagle-led-music-visualizer-3e6c7c

## Part 1. Record a WAV file, test with playback.
Record a WAV file. The 20 after -d in the arecord command indicates duration - change this to the duration desired. Also, change test.wav to YOUR_DESIRED_FILE_NAME.wav.
```
sudo apt-get install alsa-utils
arecord -f cd -D plughw:1,0 -d 20 test.wav
```
There should now be a test.wav (or your renamed .wav file) in your directory. Play the WAV file back with:
```
aplay -f cd test.wav
```
Installing alsa-utils will also allow you to use alsamixer. Typing alsamixer into terminal will allow you to control speaker and microphone volume, as well as volume gain.

### Part 1 Notes
If you're having trouble with setting your default soundcard (e.g. alsa-utils wants to read card 0 but your audio adapter is card 1), this is the solution: https://www.alsa-project.org/wiki/Setting_the_default_device

Although this did not happen to me, many users in Stack Exchange needed to unmute amixer to actually record audio: https://askubuntu.com/questions/77522/command-to-unmute-and-maximize-volume

## Part 2. Connecting the LED strip to the Pocketbeagle
First, edit the boot file to use UIO following these instructions: https://markayoder.github.io/PRUCookbook/06io/io.html#io_uio

Then, edit the uEnv.txt:
```
cd /boot
grep pru uEnv.txt
sudo nano uEnv.txt

#Edit uEnv.txt to look like:
###pru_rproc (4.4.x-ti kernel)
#uboot_overlay_pru=/lib/firmware/AM335X-PRU-RPROC-4-4-TI-00A0.dtbo
###pru_rproc (4.14.x-ti kernel)
#uboot_overlay_pru=/lib/firmware/AM335X-PRU-RPROC-4-14-TI-00A0.dtbo
###pru_uio (4.4.x-ti, 4.14.x-ti & mainline/bone kernel)
uboot_overlay_pru=/lib/firmware/AM335X-PRU-UIO-00A0.dtbo
```
Using Part 1.3 in this guide (https://markayoder.github.io/PRUCookbook/01case/case.html#_neopixels_5050_rgb_leds_with_integrated_drivers_ledscape) was then able to help connect my LED to the Pocketbeagle. *Use P1_08 where it says P9_22!* The guide uses a Beagleboard, and its P9_22 pin is analogous to P1_08 on the Pocketbeagle.

### Part 2 Notes
Using Neopixel (https://learn.adafruit.com/adafruit-neopixel-uberguide) did not work for me - after attempting to connect, it stated that the Pocketbeagle is not compatible. Thus, the above steps can be followed specifically for the Pocketbeagle.

## Autoboot
Create a text file in a logs directory called cronlog. Add a shell script to your home with the script in chronlauncher.sh (docs directory). Change the initial cd command to the directectory specific to your project files. After, access crontab with:
```
sudo crontab -e
```
Add in this line to crontab to complete autoboot:
```
@reboot sleep 30 && sh /var/lib/cloud9/project_01/chronlauncher.sh > /var/lib/cloud9/project_01/logs/cronlog 2>&1
```
Boot problems will be logged in cronlog.
