# Kubos SDK
[![Build Status](https://travis-ci.org/kubostech/kubos-sdk.svg?branch=master)](https://travis-ci.org/kubostech/kubos-sdk) [![Coverage Status](https://coveralls.io/repos/github/kyleparrott/kubos-sdk/badge.svg?branch=master)](https://coveralls.io/github/kyleparrott/kubos-sdk?branch=master)
### Installation:

Install the kubos sdk

```
$ pip install kubos-sdk
```

Pull the latest kubos-sdk docker container

```
$ kubos update
```

### Usage:

#### Create a new KubOS project:

```
$ kubos init  <project name>
```


#### Set target device:

```
$ kubos target <target>
```
The current supported targets are: 

STM32F407 Discovery Board - `stm32f407-disco-gcc@openkosmosorg/target-stm32f407-disco-gcc`

MSP430F5529 Launchpad - `msp430f5529-gcc@openkosmosorg/target-msp430f5529-gcc`

#### Build your project:

```
$ kubos build
$ kubos build -v #for verbose builds
```

#### Flash your target device:

```
$ kubos flash
```

#### Debug your project

A gdb server must be started to allow your gdb instance to connect and debug directly on your hardware device.
After building your project with `kubos build` kubos can manage a gdb server and gdb instance for you.

Start a gdb server and instance for you:
Note: this may need to run as root depending on your usb device permissions
```
$ kubos debug
```


Additionally you can interact directly with the gdb server:

```
$ kubos server <start, stop, restart, status>
```

