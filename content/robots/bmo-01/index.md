+++
title = "bmo-01"
+++

I'm building a robot. It uses a [custom PCB](@/robots/bmo-01/robot-board.md) running [embedded software](@/robots/bmo-01/motor-control.md)

I am building a mobile robot with three omnidirectional wheels to enable it to drive in any direction, and two USB cameras for binocular computer vision. The plan is to use this robot to learn more about computer vision, localization, and mapping.

### First Revision

My first version consisted of a Raspberry Pi 4 communicating with a Raspberry Pi Pico through UART, which in turn controlled the speed of three brushed DC motors using the [Cytron MD10C motor drivers](https://www.cytron.io/p-10amp-5v-30v-dc-motor-driver) in sign-magnitude PWM mode. I designed a PCB to help with routing the connections between the Pico, motor drivers, motors, and encoders. More details on that can be found [here](@/robots/bmo-01/pico-board.md)

{{ image(path="/images/robot-rev1-cad.png", scale=0.5, title="3D CAD model of the robot") }}
