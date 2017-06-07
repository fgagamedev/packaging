function Component()
{
    component.addOperation("AppendFile", "@TargetDir@/$project_name", "#!/bin/bash\ncd @TargetDir@ && export LD_LIBRARY_PATH=bin/linux/lib && ./bin/linux/$project_name");
    component.addOperation("Execute", "chmod", "u+x", "@TargetDir@/$project_name");
}

