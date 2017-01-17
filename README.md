# Kubos CLI

## NOTE: This module is primarily meant to run inside of a provisioned Vagrant Box.
## ALMOST ALL USERS WILL WANT TO USE THIS IN THE VAGRANT CONTEXT SEE [THE KUBOS DOCS](http://docs.kubos.co) FOR THE VAGRANT INSTALLATION DOCS

#### Advanced users may want to use this natively on their machines. Below are the instructions for manual installation

### Installation:

Install the kubos-cli

```
$ pip install kubos-cli
```
### Update:
Kubos projects are small modules built against a number of Kubos "source" modules. Before working on your project you will
need to specify and activate a released version of the Kubos source modules.

Fetch all of the kubos source releases, without activating any of them:
```
$ sudo kubos update
```

Display a list of all the available release versions `kubos versions` - Note: The versions available to you may be different than the following example
```
$ kubos versions

Available versions are:
v0.0.0
v0.0.1
v0.0.2
The most recent release is: v0.0.2
```

Activate a specific version `kubos update <version>`:
```
kubos update v0.0.2

...
Activating Kubos source version v0.0.2
```

Display the active versions of the kubos-cli and kubos source at anytime with `kubos version`:

```
kubos version

Kubos-CLI version    : v0.1.2
Kubos Source version : v0.0.0
```


### Usage:

#### Create a new KubOS project:

```
$ kubos init  <project name>
```


By default, this will create a new KubOS project with example code to run on KubOS RT.  If you
would like to create a project with example code to run on KubOS Linux, add the '--linux' 
(or '-l') option.


```
$ kubos init --linux <project name>
```


#### Setting a Target Board
Kubos Projects automatically set and use predefined build, flash and debug configurations based on the hardware platform you are working on.

##### List available targets:

```
$ kubos target --list
Available targets are:

kubos-arm-none-eabi-gcc
pyboard-gcc
stm32f405-gcc
stm32f407-disco-gcc
msp430f5529-gcc
...
```
##### Set target device:

```
$ kubos target <target>
```


#### Build your project:

```
$ kubos build
$ kubos build -- -v #for verbose builds
```

#### Flash your target device:

```
$ kubos flash
```

#### Debug your project

A gdb server must be started to allow your gdb instance to connect and debug directly on your hardware device.
After building your project with `kubos build` kubos can start a gdb server and gdb instance for you.

Start a gdb server and instance for you:
Note: this may need to run as root depending on your usb device permissions
```
$ kubos debug
```


