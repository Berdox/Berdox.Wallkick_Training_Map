global function TeleportInitThread

void function TeleportInitThread()
{
    thread InitTeleportTriggers()
}

void function InitTeleportTriggers()
{
    // Wait a few frames for entities to initialize
    WaitFrame()
    WaitFrame()
	
    print("teleport init started\n")
	
    array<entity> triggers = GetEntArrayByClass_Expensive("trigger_multiple")

    foreach (entity trigger in triggers)
    {
        if (!IsValid(trigger))
            continue

        string triggerName = trigger.GetValueForKey("targetname")

        if (triggerName != "" && triggerName.find("teleport_trigger_") == 0)
        {
            print("Found teleport trigger: " + triggerName + "\n")
            trigger.ConnectOutput("OnStartTouch", TeleportPlayer)
        }
    }
}

void function TeleportPlayer(entity trigger, entity activator, entity caller, var value)
{
    print("Entered TeleportPlayer callback\n")

    if (!IsValid(activator) || !activator.IsPlayer())
    {
        print("Activator is not a player\n")
        return
    }

    string destinationName = trigger.GetValueForKey("target")

    if (destinationName == "")
    {
        print("Trigger has no 'target' key!\n")
        return
    }

    array<entity> destinations = GetEntArrayByClass_Expensive("info_target")
    entity destination = null

    foreach (entity ent in destinations)
    {
        if (!IsValid(ent))
            continue

        string destName = ent.GetValueForKey("targetname")
        if (destName == destinationName)
        {
            destination = ent
            break
        }
    }

    if (!IsValid(destination))
    {
        print("Destination '" + destinationName + "' not found!\n")
        return
    }

    print("Teleporting to: " + destinationName + "\n")
	vector pos = activator.GetOrigin()
	vector destinationPosition = destination.GetOrigin()
	destinationPosition.z = pos.z
    activator.SetOrigin(destinationPosition)
	
    activator.SetAngles(activator.GetAngles())
}
