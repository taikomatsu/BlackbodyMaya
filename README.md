BlackbodyMaya
=============

Blackbody radiation tool for Maya

=============

Blackbody tool for Maya


--- Introduction ---

This tool makes ramp that based on blackbody radiation.
You have to input just few parameters, like "Min Temperature", "Max Temperature".

You can select "Expression" or "Node" for make it.

When you select "Node" mode, this tool makes a "blackbody" node written in Python.
This mode is recommend if you want to share the result in some nodes.
(But you have to make connections manually. Now I haven't made some functions for help it yet, sorry.)

Or when if you select "Expression" mode, it's the default mode of the tool,
this tool makes an expression.

Because both mode is almost same usage, you can choose either which you want.



--- Install ---

scripts
 - copy all scripts to your $MAYA_SCRIPT_PATH directory.

plug-ins
 - copy blackbody.py to your $MAYA_PLUG_IN_PATH directory.

python
 - copy blackbody directory to directory that has through a path sys.path.
   if you haven't done setting anymore, you can copy to under your $MAYA_SCRIPT_PATH directory.



--- Usage ---

1. Start Maya

2. Open script editor and types below in MEL tab.

  blackbodyUI();

3. Select ramp or fluid object to attach blackbody node or expression.

4. Press "Set to Selected" button on the window.



--- Parameters ---

- On Window -

[Min, Max Temperature]
Theses parameters are most important ones on this tool.
They decide a color of the ramp.
The unit of these parameters are "K (kelvin)".

[Samples]
Number of control point on the ramp.
Default is 20, but if you want more finely, you can increase it.


- Attribute -

After the making it, you can control the colors by some attributes.


[Enrgy Exp]
This value is based on Magnus Wrenninge's Siggraph paper.
http://magnuswrenninge.com/content/pubs/ProductionVolumeRenderingSystems2011.pdf
(from p.37, 4.5 Blackbody radiation.)

Default is 4 and it's phisically correct value.

[Energy Mult]
Decide final brightness.
Deafult is 5.0.

[Energy Offset]
If you felt too dark in lower side, increase this value.
Default is 0.

[Min, Max Temperatures]
Same as the parameters on the window.
You can change it in runtime.


- Contact -
If you have some ideas, or found bugs, please tell me it.

mail: taikomatsu__at__gmail.com
(Please replace __at__ to @)

