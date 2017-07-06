# ToolBox

In the repo various scripts or codesnippet are stored that are not attributed to a single project. To access them in your projects the easiest way is to add the path to this repo to the $PYTHONPATH on your machine.

    export PYTHONPATH=$PYTHONPATH:/path/to/Toolbox
    
Alternatively this can only be one in the beginnning of the python script where the modules are need:

    import sys
    sys.path.append("path/to/ToolBox")
    
  
    
After this the modules (the subdirectories) can be accessed in your code with:

    from ToolBox import Module as m
